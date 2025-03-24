import os
import tarfile
import tempfile
import boto3
import hashlib
import json
from datetime import datetime
from botocore.exceptions import ClientError
from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class S3BackupConfig(BaseModel):
    bucket_name: Optional[str] = None
    aws_region: Optional[str] = None
    prefix: str = "pdldb_backups/"
    endpoint_url: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None


class FullBackupRequest(BaseModel):
    source_path: str
    backup_name: Optional[str] = None


class MirrorBackupRequest(BaseModel):
    source_path: str


class RestoreRequest(BaseModel):
    backup_name: str
    destination_path: str
    specific_files: Optional[List[str]] = None


class S3BackupManager:
    def __init__(
        self,
        bucket_name=None,
        aws_region=None,
        prefix="pdldb_backups/",
        endpoint_url=None,
        aws_access_key_id=None,
        aws_secret_access_key=None,
    ):
        config = S3BackupConfig(
            bucket_name=bucket_name,
            aws_region=aws_region,
            prefix=prefix,
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

        self.s3_client = boto3.client(
            "s3",
            region_name=config.aws_region
            or os.environ.get("AWS_REGION")
            or os.environ.get("AWS_DEFAULT_REGION"),
            endpoint_url=config.endpoint_url,
            aws_access_key_id=config.aws_access_key_id
            or os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=config.aws_secret_access_key
            or os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )
        self.bucket = config.bucket_name or os.environ.get("S3_BUCKET_NAME")
        self.prefix = config.prefix
        self.full_prefix = f"{config.prefix}full_backups/"
        self.mir_prefix = f"{config.prefix}mirror_backup/"

        if not self.bucket:
            raise ValueError(
                "S3 bucket name is required. Provide it as a parameter or set S3_BUCKET_NAME environment variable."
            )

    def _get_file_hash(self, filepath):
        if not os.path.isfile(filepath):
            return None

        hasher = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def _get_manifest_key(self, backup_name):
        return f"{self.full_prefix}{backup_name}/manifest.json"

    def _get_mir_manifest_key(self):
        return f"{self.mir_prefix}manifest.json"

    def _load_manifest(self, backup_name=None):
        if backup_name:
            try:
                response = self.s3_client.get_object(
                    Bucket=self.bucket, Key=self._get_manifest_key(backup_name)
                )
                return json.loads(response["Body"].read().decode("utf-8"))
            except ClientError:
                return {"files": {}, "created_at": datetime.now().isoformat()}
        else:
            try:
                response = self.s3_client.get_object(
                    Bucket=self.bucket, Key=self._get_mir_manifest_key()
                )
                return json.loads(response["Body"].read().decode("utf-8"))
            except ClientError:
                return {"files": {}, "created_at": datetime.now().isoformat()}

    def _save_manifest(self, manifest, backup_name=None):
        manifest_data = json.dumps(manifest).encode("utf-8")
        if backup_name:
            self.s3_client.put_object(
                Bucket=self.bucket,
                Key=self._get_manifest_key(backup_name),
                Body=manifest_data,
            )
        else:
            self.s3_client.put_object(
                Bucket=self.bucket, Key=self._get_mir_manifest_key(), Body=manifest_data
            )

    def full_backup(self, source_path: str, backup_name: Optional[str] = None) -> str:
        params = FullBackupRequest(source_path=source_path, backup_name=backup_name)

        source_path = os.path.abspath(params.source_path)
        source_dir = os.path.basename(source_path)

        if not os.path.exists(source_path):
            raise ValueError(f"Source path does not exist: {source_path}")

        if not params.backup_name:
            date_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{source_dir}_{date_suffix}"
        else:
            backup_name = params.backup_name

        with tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False) as tmp_file:
            archive_path = tmp_file.name

        try:
            with tarfile.open(archive_path, "w:gz") as tar:
                tar.add(source_path, arcname=os.path.basename(source_path))

            backup_key = f"{self.full_prefix}{backup_name}/full_backup.tar.gz"
            self.s3_client.upload_file(
                archive_path,
                self.bucket,
                backup_key,
                ExtraArgs={"StorageClass": "STANDARD"},
            )

            created_at = datetime.now().isoformat()

            manifest = {
                "files": {},
                "created_at": created_at,
                "type": "full",
            }

            file_count = 0
            for root, _, files in os.walk(source_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, source_path)
                    manifest["files"][rel_path] = {
                        "hash": self._get_file_hash(file_path),
                        "mtime": os.path.getmtime(file_path),
                    }
                    file_count += 1

            self._save_manifest(manifest, backup_name)

            return backup_name

        finally:
            if os.path.exists(archive_path):
                os.unlink(archive_path)

    def mirror_backup(self, source_path: str) -> str:
        params = MirrorBackupRequest(source_path=source_path)
        source_path = os.path.abspath(params.source_path)

        if not os.path.exists(source_path):
            raise ValueError(f"Source path does not exist: {source_path}")

        source_dir = os.path.basename(source_path)

        try:
            current_mir_manifest = self._load_manifest()
        except ClientError:
            current_mir_manifest = {
                "files": {},
                "created_at": datetime.now().isoformat(),
            }

        s3_files = {}
        try:
            paginator = self.s3_client.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=self.bucket, Prefix=self.mir_prefix)

            for page in pages:
                for obj in page.get("Contents", []):
                    key = obj["Key"]
                    if not key.endswith("manifest.json"):
                        rel_path = key[len(self.mir_prefix) :]
                        s3_files[rel_path] = key
        except ClientError:
            pass

        local_files = {}
        for root, _, files in os.walk(source_path):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, source_path)
                local_files[rel_path] = {
                    "path": file_path,
                    "hash": self._get_file_hash(file_path),
                    "mtime": os.path.getmtime(file_path),
                }

        to_upload = []
        to_delete = []

        for rel_path, file_info in local_files.items():
            if rel_path not in current_mir_manifest.get("files", {}) or file_info[
                "hash"
            ] != current_mir_manifest["files"].get(rel_path, {}).get("hash"):
                to_upload.append((file_info["path"], rel_path))

        for rel_path in s3_files:
            if rel_path not in local_files:
                to_delete.append({"Key": s3_files[rel_path]})

        new_manifest = {
            "files": {},
            "created_at": datetime.now().isoformat(),
            "type": "mirror",
            "source_directory": source_dir,
        }

        for rel_path, file_info in local_files.items():
            new_manifest["files"][rel_path] = {
                "hash": file_info["hash"],
                "mtime": file_info["mtime"],
            }

        for file_path, rel_path in to_upload:
            target_key = f"{self.mir_prefix}{rel_path}"
            try:
                self.s3_client.upload_file(
                    file_path,
                    self.bucket,
                    target_key,
                    ExtraArgs={"StorageClass": "STANDARD"},
                )
            except Exception as e:
                print(f"Error uploading {file_path}: {e}")

        if to_delete:
            try:
                for i in range(0, len(to_delete), 1000):
                    batch = to_delete[i : i + 1000]
                    self.s3_client.delete_objects(
                        Bucket=self.bucket, Delete={"Objects": batch, "Quiet": True}
                    )
            except Exception as e:
                print(f"Error deleting objects: {e}")

        self._save_manifest(new_manifest)

        return "mirror_backup"

    def restore(
        self,
        backup_name: str,
        destination_path: str,
        specific_files: Optional[List[str]] = None,
    ) -> bool:
        params = RestoreRequest(
            backup_name=backup_name,
            destination_path=destination_path,
            specific_files=specific_files,
        )

        destination_path = params.destination_path
        backup_name = params.backup_name
        specific_files = params.specific_files

        os.makedirs(destination_path, exist_ok=True)

        if backup_name == "mirror_backup":
            manifest = self._load_manifest()
            files_prefix = self.mir_prefix

            source_dir = manifest.get("source_directory", "")

            if source_dir:
                target_path = os.path.join(destination_path, source_dir)
                os.makedirs(target_path, exist_ok=True)
            else:
                target_path = destination_path

            try:
                paginator = self.s3_client.get_paginator("list_objects_v2")
                pages = paginator.paginate(Bucket=self.bucket, Prefix=files_prefix)

                for page in pages:
                    for obj in page.get("Contents", []):
                        file_key = obj["Key"]
                        if file_key.endswith("manifest.json"):
                            continue

                        rel_path = file_key[len(files_prefix) :]

                        if specific_files and rel_path not in specific_files:
                            continue

                        if source_dir:
                            local_path = os.path.join(target_path, rel_path)
                        else:
                            local_path = os.path.join(destination_path, rel_path)

                        os.makedirs(os.path.dirname(local_path), exist_ok=True)

                        self.s3_client.download_file(self.bucket, file_key, local_path)

                return True
            except ClientError as e:
                print(f"Error during mirror restore: {e}")
                return False

        manifest = self._load_manifest(backup_name)

        with tempfile.TemporaryDirectory() as temp_dir:
            archive_key = f"{self.full_prefix}{backup_name}/full_backup.tar.gz"
            archive_path = os.path.join(temp_dir, f"{backup_name}.tar.gz")

            try:
                self.s3_client.download_file(self.bucket, archive_key, archive_path)

                with tarfile.open(archive_path, "r:gz") as tar:
                    if specific_files:
                        for member in tar.getmembers():
                            if member.name in specific_files:
                                tar.extract(member, path=destination_path)
                    else:
                        tar.extractall(path=destination_path)

                return True

            except ClientError:
                return False

        return False

    def list_backups(self) -> List[Dict[str, Any]]:
        backups = []

        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket, Prefix=self.full_prefix, Delimiter="/"
            )

            for prefix in response.get("CommonPrefixes", []):
                backup_name = prefix["Prefix"].split("/")[-2]
                try:
                    manifest = self._load_manifest(backup_name)
                    backups.append(
                        {
                            "name": backup_name,
                            "type": "full",
                            "created_at": manifest.get("created_at", "unknown"),
                        }
                    )
                except ClientError as e:
                    print(f"Error loading manifest for {backup_name}: {e}")
                except Exception as e:
                    print(f"Unexpected error processing backup {backup_name}: {e}")

        except ClientError as e:
            print(f"Error listing full backups: {e}")

        try:
            manifest = self._load_manifest()
            if manifest.get("files"):
                backups.append(
                    {
                        "name": "mirror_backup",
                        "type": "mirror",
                        "created_at": manifest.get("created_at", "unknown"),
                        "source_directory": manifest.get("source_directory", "unknown"),
                    }
                )
        except ClientError as e:
            print(f"Error loading mirror backup manifest: {e}")
        except Exception as e:
            print(f"Unexpected error processing mirror backup: {e}")

        return backups
