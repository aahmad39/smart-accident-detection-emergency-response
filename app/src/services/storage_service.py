# Tier 2: Storage Service (Azure Blob Storage with Local Fallback)
import os
import uuid
from flask import current_app

class StorageService:
    """Manages secure storage of crash evidence, dashcam captures, and telemetry dumps."""

    @classmethod
    def get_blob_client(cls):
        """Returns Azure Blob Service Client if connection string is configured."""
        conn_str = current_app.config.get("AZURE_STORAGE_CONNECTION_STRING")
        if conn_str:
            try:
                from azure.storage.blob import BlobServiceClient
                return BlobServiceClient.from_connection_string(conn_str)
            except ImportError:
                return None
        return None

    @classmethod
    def upload_crash_evidence(cls, file_bytes: bytes, filename: str, content_type: str = "image/jpeg") -> str:
        """
        Uploads crash evidence to Azure Blob Storage container 'crash-evidence'.
        Falls back to local file system if Azure connection string is absent (e.g. local dev).
        """
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        blob_service = cls.get_blob_client()

        if blob_service:
            container_name = current_app.config.get("AZURE_STORAGE_CONTAINER_NAME", "crash-evidence")
            container_client = blob_service.get_container_client(container_name)
            
            # Ensure container exists
            try:
                container_client.create_container()
            except Exception:
                pass

            blob_client = container_client.get_blob_client(unique_name)
            blob_client.upload_blob(file_bytes, overwrite=True, content_type=content_type)
            return blob_client.url
        else:
            # Fallback to local storage
            local_dir = current_app.config.get("LOCAL_STORAGE_PATH")
            os.makedirs(local_dir, exist_ok=True)
            local_filepath = os.path.join(local_dir, unique_name)
            with open(local_filepath, "wb") as f:
                f.write(file_bytes)
            # Return relative path for local serving
            return f"/static/uploads/{unique_name}"
