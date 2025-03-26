from enum import Enum
from typing import Dict

from pydantic import BaseModel


class StorageCategory(str, Enum):
    """Synapse Backend Storage Category Enum."""

    INTERNAL = 'internal'
    EXTERNAL = 'external'


class StorageProvider(str, Enum):
    """Synapse Backend Storage Provider Enum."""

    AMAZON_S3 = 'amazon_s3'
    AZURE = 'azure'
    DIGITAL_OCEAN = 'digital_ocean'
    FILE_SYSTEM = 'file_system'
    FTP = 'ftp'
    SFTP = 'sftp'
    MINIO = 'minio'
    GCP = 'gcp'


class Storage(BaseModel):
    """Synapse Backend Storage Model.

    Attrs:
        id (int): The storage pk.
        name (str): The storage name.
        category (str): The storage category. (ex: internal, external)
        provider (str): The storage provider. (ex: s3, gcp)
        configuration (Dict): The storage configuration.
        is_default (bool): The storage is default for Synapse backend workspace.
    """

    id: int
    name: str
    category: StorageCategory
    provider: StorageProvider
    configuration: Dict
    is_default: bool
