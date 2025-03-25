import os
from .lib.aws import aws_download, aws_upload, delete_s3_object, get_s3_presigned_url, stream_s3_file
from .lib.gcp import gcp_download, gcp_upload, delete_gcs_object, get_gcs_presigned_url, stream_gcp_file
from .lib.azure import azure_download, azure_upload, delete_azure_blob, get_azure_blob_presigned_url, stream_azure_file
from typing import Generator, Optional

cloudProvider = os.environ.get('CLOUD_PROVIDER')


def upload_file(file_path, data, config=None):
    """
    Uploads a file to a cloud storage provider.

    Args:
        file_path (str): The path to the file to upload.
        data (str): The data to upload.
        config (dict): The configuration object (optional).

    Returns:
        The upload result.

    Raises:
        ValueError: If an invalid cloud provider is specified.
    """
    if config is None:
        config = {}
    if cloudProvider.lower() == "aws":
        return aws_upload(file_path, data, config)
    elif cloudProvider.lower() == "gcp":
        return gcp_upload(file_path, data, config)
    elif cloudProvider.lower() == "azure":
        return azure_upload(file_path, data, config)
    else:
        raise ValueError("Invalid cloud provider specified.")


def download_file(file_path, config=None):
    """
    Downloads a file from a cloud provider.

    Args:
        file_path (str): The path to the file to download.
        config (dict): The configuration object (optional).

    Returns:
        The downloaded file.

    Raises:
        ValueError: If an invalid cloud provider is specified.
    """
    if config is None:
        config = {}
    if cloudProvider.lower() == "aws":
        return aws_download(file_path, config)
    elif cloudProvider.lower() == "gcp":
        return gcp_download(file_path, config)
    elif cloudProvider.lower() == "azure":
        return azure_download(file_path, config)
    else:
        raise ValueError("Invalid cloud provider specified.")


def delete_file(config=None):
    """
    Deletes a file from a cloud provider.

    Args:
        config (dict): The configuration object (optional).

    Returns:
        None

    Raises:
        ValueError: If an invalid cloud provider is specified.
    """
    if cloudProvider.lower() == "aws":
        return delete_s3_object(config)
    elif cloudProvider.lower() == "gcp":
        return delete_gcs_object(config)
    elif cloudProvider.lower() == "azure":
        return delete_azure_blob(config)
    else:
        raise ValueError("Invalid cloud provider specified.")


def get_presigned_download_url(config=None):
    """
    Generate a presigned download URL based on the cloud provider specified in the environment variable.

    Args:
        config (dict): An object containing the filePath and expiryTime.
            filePath (str): The path of the file to generate a presigned download URL for.
            expirationTime (int): The expiration time of the presigned URL in seconds. Defaults to 3600 seconds.

    Returns:
        The presigned download URL.

    Raises:
        ValueError: If an invalid cloud provider is specified.
    """
    if cloudProvider.lower() == "aws":
        return get_s3_presigned_url(config)
    elif cloudProvider.lower() == "gcp":
        return get_gcs_presigned_url(config)
    elif cloudProvider.lower() == "azure":
        return get_azure_blob_presigned_url(config)
    else:
        raise ValueError("Invalid cloud provider specified.")
    

def stream_file(config: dict, chunk_size: int = 1048576) -> Generator[bytes, None, None]:
    """
    Streams a file from the appropriate cloud provider (AWS, GCP, or Azure) in chunks.

    Args:
        config (dict): A configuration object containing:
            - 'filePath' (str): The path to the file.
            - 'bucketName' (str): The bucket/container name.
            - Additional required parameters for the respective cloud provider.
        chunk_size (int): Size of each chunk in bytes (default: 1MB).

    Yields:
        Generator[bytes, None, None]: File content in chunks.

    Raises:
        ValueError: If an invalid cloud provider is specified.
    """
    cloud_provider = config.get("cloudProvider", "").lower()
    if cloud_provider == "aws":
        yield from stream_s3_file(config["filePath"], config, chunk_size=chunk_size)
    elif cloud_provider == "gcp":
        yield from stream_gcp_file(config["filePath"], config, chunk_size=chunk_size)
    elif cloud_provider == "azure":
        yield from stream_azure_file(config["filePath"], config, chunk_size=chunk_size)
    else:
        raise ValueError("Invalid cloud provider specified.")
