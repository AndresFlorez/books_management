import os
from typing import Dict, Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


def to_bool(value):
    """Converts a string to a boolean."""
    return value.lower() in ('true', '1', 't', 'True')


class MongoSettings(BaseSettings):
    """Settings for Django application."""

    db_host: str = os.getenv('DB_HOST')
    db_port: int = os.getenv('DB_PORT')
    db_user: str = os.getenv('DB_USER')
    db_password: str = os.getenv('DB_PASSWORD')
    db_name: str = os.getenv('DB_NAME')


class DjangoSettings(BaseSettings):
    allowed_hosts: str = os.getenv('ALLOWED_HOSTS')
    debug: bool = to_bool(os.getenv('DEBUG'))


class AwsSettings(BaseSettings):
    aws_access_key_id: str = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key: str = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_storage_bucket_name: str = os.getenv('AWS_STORAGE_BUCKET_NAME')
    aws_s3_region_name: str = os.getenv('AWS_S3_REGION_NAME', 'us-east-1')
    aws_s3_custom_domain: str = f'{aws_storage_bucket_name}.s3.{aws_s3_region_name}.amazonaws.com'

    staticfiles_storage: str = os.getenv('STATICFILES_STORAGE', 'storages.backends.s3boto3.S3Boto3Storage')
    static_url: str = f'https://{aws_s3_custom_domain}/static/'

    default_file_storage: str = os.getenv('DEFAULT_FILE_STORAGE', 'storages.backends.s3boto3.S3Boto3Storage')
    media_url: str = f'https://{aws_s3_custom_domain}/media/'

    aws_querystring_auth: bool = True
    aws_default_acl: Optional[str] = None
    aws_s3_object_parameters: Dict = {
        'CacheControl': 'max-age=86400',
    }


mongo_settings = MongoSettings()
django_settings = DjangoSettings()
aws_settings = AwsSettings()
