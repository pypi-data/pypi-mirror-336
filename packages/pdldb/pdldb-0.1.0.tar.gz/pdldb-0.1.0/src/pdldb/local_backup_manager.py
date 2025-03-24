import os
import tarfile
import shutil
import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional, Union, Set
from pydantic import BaseModel, Field, DirectoryPath, field_validator


class BackupInfo(BaseModel):
    name: str
    type: str
    created_at: str
    source_directory: Optional[str] = None


class FileInfo(BaseModel):
    hash: str
    mtime: float


class ManifestModel(BaseModel):
    files: Dict[str, FileInfo] = {}
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    type: Optional[str] = None
    source_directory: Optional[str] = None


class FullBackupParams(BaseModel):
    source_path: Union[str, os.PathLike]
    backup_name: Optional[str] = None


class MirrorBackupParams(BaseModel):
    source_path: Union[str, os.PathLike]


class RestoreParams(BaseModel):
    backup_name: str
    destination_path: Union[str, os.PathLike]
    specific_files: Optional[Set[str]] = None


class LocalBackupManager:
    class Config(BaseModel):
        backup_directory: DirectoryPath
        prefix: str = "pdldb_backups/"

    def __init__(
        self, backup_directory: Union[str, os.PathLike], prefix: str = "pdldb_backups/"
    ):
        config = self.Config(
            backup_directory=os.path.abspath(backup_directory), prefix=prefix
        )
        self.backup_directory = config.backup_directory
        self.prefix = config.prefix
        self.full_prefix = os.path.join(self.backup_directory, f"{prefix}full_backups/")
        self.mir_prefix = os.path.join(self.backup_directory, f"{prefix}mirror_backup/")
        os.makedirs(self.full_prefix, exist_ok=True)
        os.makedirs(self.mir_prefix, exist_ok=True)

    def _get_file_hash(self, filepath: Union[str, os.PathLike]) -> Optional[str]:
        if not os.path.isfile(filepath):
            return None
        hasher = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def _get_manifest_path(self, backup_name: str) -> str:
        return os.path.join(self.full_prefix, backup_name, "manifest.json")

    def _get_mir_manifest_path(self) -> str:
        return os.path.join(self.mir_prefix, "manifest.json")

    def _load_manifest(self, backup_name: Optional[str] = None) -> ManifestModel:
        if backup_name:
            manifest_path = self._get_manifest_path(backup_name)
        else:
            manifest_path = self._get_mir_manifest_path()

        if os.path.exists(manifest_path):
            with open(manifest_path, "r") as f:
                data = json.load(f)
                return ManifestModel(**data)
        return ManifestModel(files={}, created_at=datetime.now().isoformat())

    def _save_manifest(
        self, manifest: ManifestModel, backup_name: Optional[str] = None
    ) -> None:
        if backup_name:
            manifest_path = self._get_manifest_path(backup_name)
            os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
        else:
            manifest_path = self._get_mir_manifest_path()

        with open(manifest_path, "w") as f:
            json.dump(manifest.model_dump(), f, indent=2)

    def full_backup(
        self, source_path: Union[str, os.PathLike], backup_name: Optional[str] = None
    ) -> str:
        params = FullBackupParams(source_path=source_path, backup_name=backup_name)

        source_path = os.path.abspath(params.source_path)
        source_dir = os.path.basename(source_path)

        if not params.backup_name:
            date_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{source_dir}_{date_suffix}"
        else:
            backup_name = params.backup_name

        backup_dir = os.path.join(self.full_prefix, backup_name)
        os.makedirs(backup_dir, exist_ok=True)
        archive_path = os.path.join(backup_dir, "full_backup.tar.gz")

        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(source_path, arcname=os.path.basename(source_path))

        manifest = ManifestModel(
            files={}, created_at=datetime.now().isoformat(), type="full"
        )

        for root, _, files in os.walk(source_path):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, source_path)
                manifest.files[rel_path] = FileInfo(
                    hash=self._get_file_hash(file_path) or "",
                    mtime=os.path.getmtime(file_path),
                )

        self._save_manifest(manifest, backup_name)
        return backup_name

    def mirror_backup(self, source_path: Union[str, os.PathLike]) -> str:
        params = MirrorBackupParams(source_path=source_path)
        source_path = os.path.abspath(params.source_path)
        source_dir = os.path.basename(source_path)

        os.makedirs(self.mir_prefix, exist_ok=True)
        current_mir_manifest = self._load_manifest()

        local_stored_files = {}
        for root, _, files in os.walk(self.mir_prefix):
            for file in files:
                if file == "manifest.json":
                    continue
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, self.mir_prefix)
                local_stored_files[rel_path] = file_path

        local_files = {}
        for root, _, files in os.walk(source_path):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, source_path)
                file_hash = self._get_file_hash(file_path) or ""
                local_files[rel_path] = {
                    "path": file_path,
                    "hash": file_hash,
                    "mtime": os.path.getmtime(file_path),
                }

        to_upload = []
        to_delete = []

        for rel_path, file_info in local_files.items():
            if (
                rel_path not in current_mir_manifest.files
                or file_info["hash"]
                != current_mir_manifest.files.get(
                    rel_path, FileInfo(hash="", mtime=0)
                ).hash
            ):
                to_upload.append((file_info["path"], rel_path))

        for rel_path in local_stored_files:
            if rel_path not in local_files:
                to_delete.append(local_stored_files[rel_path])

        new_manifest = ManifestModel(
            files={},
            created_at=datetime.now().isoformat(),
            type="mirror",
            source_directory=source_dir,
        )

        for rel_path, file_info in local_files.items():
            new_manifest.files[rel_path] = FileInfo(
                hash=file_info["hash"], mtime=file_info["mtime"]
            )

        for file_path, rel_path in to_upload:
            target_path = os.path.join(self.mir_prefix, rel_path)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            try:
                shutil.copy2(file_path, target_path)
            except Exception as e:
                print(f"Error copying {file_path}: {e}")

        for file_path in to_delete:
            try:
                os.remove(file_path)
                dir_path = os.path.dirname(file_path)
                while dir_path != self.mir_prefix:
                    if not os.listdir(dir_path):
                        os.rmdir(dir_path)
                        dir_path = os.path.dirname(dir_path)
                    else:
                        break
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

        self._save_manifest(new_manifest)
        return "mirror_backup"

    def restore(
        self,
        backup_name: str,
        destination_path: Union[str, os.PathLike],
        specific_files: Optional[List[str]] = None,
    ) -> bool:
        params = RestoreParams(
            backup_name=backup_name,
            destination_path=destination_path,
            specific_files=set(specific_files) if specific_files else None,
        )

        os.makedirs(params.destination_path, exist_ok=True)

        if params.backup_name == "mirror_backup":
            manifest = self._load_manifest()
            source_dir = manifest.source_directory or ""

            if source_dir:
                target_path = os.path.join(params.destination_path, source_dir)
                os.makedirs(target_path, exist_ok=True)
            else:
                target_path = params.destination_path

            try:
                for root, _, files in os.walk(self.mir_prefix):
                    for file in files:
                        if file == "manifest.json":
                            continue
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, self.mir_prefix)

                        if (
                            params.specific_files
                            and rel_path not in params.specific_files
                        ):
                            continue

                        if source_dir:
                            local_path = os.path.join(target_path, rel_path)
                        else:
                            local_path = os.path.join(params.destination_path, rel_path)

                        os.makedirs(os.path.dirname(local_path), exist_ok=True)
                        shutil.copy2(file_path, local_path)
                return True
            except Exception as e:
                print(f"Error during mirror restore: {e}")
                return False

        backup_dir = os.path.join(self.full_prefix, params.backup_name)
        archive_path = os.path.join(backup_dir, "full_backup.tar.gz")

        if not os.path.exists(archive_path):
            print(f"Backup archive not found: {archive_path}")
            return False

        try:
            with tarfile.open(archive_path, "r:gz") as tar:
                if params.specific_files:
                    for member in tar.getmembers():
                        if member.name in params.specific_files:
                            tar.extractall(path=params.destination_path, filter="data")
                else:
                    tar.extractall(path=params.destination_path, filter="data")
            return True
        except Exception as e:
            print(f"Error during full backup restore: {e}")
            return False

    def list_backups(self) -> List[BackupInfo]:
        backups = []
        try:
            for item in os.listdir(self.full_prefix):
                item_path = os.path.join(self.full_prefix, item)
                if os.path.isdir(item_path):
                    manifest_path = os.path.join(item_path, "manifest.json")
                    if os.path.exists(manifest_path):
                        try:
                            with open(manifest_path, "r") as f:
                                manifest = json.load(f)
                                backups.append(
                                    BackupInfo(
                                        name=item,
                                        type="full",
                                        created_at=manifest.get(
                                            "created_at", "unknown"
                                        ),
                                    )
                                )
                        except Exception as e:
                            print(f"Error reading manifest for {item}: {e}")
        except Exception as e:
            print(f"Error listing full backups: {e}")

        mir_manifest_path = self._get_mir_manifest_path()
        if os.path.exists(mir_manifest_path):
            try:
                with open(mir_manifest_path, "r") as f:
                    manifest = json.load(f)
                    if manifest.get("files"):
                        backups.append(
                            BackupInfo(
                                name="mirror_backup",
                                type="mirror",
                                created_at=manifest.get("created_at", "unknown"),
                                source_directory=manifest.get(
                                    "source_directory", "unknown"
                                ),
                            )
                        )
            except Exception as e:
                print(f"Error reading mirror backup manifest: {e}")

        return backups
