import logging
import os
import shutil
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from google.cloud import storage
from google.cloud.exceptions import GoogleCloudError


def upload(filename: Path, target: str):
    if target.startswith(("gs://", "s3://")):
        service, _, target = str(target).partition("://")
        parts = target.split("/")
        bucket = parts.pop(0)
        object_name = "/".join(parts)
        if service == "s3":
            upload_to_s3(filename, bucket, object_name)
        elif service == "gs":
            upload_to_storage(filename, bucket, object_name)
        else:
            logging.error(f"Unknown upload service '{service}'")

    else:
        shutil.copy(filename, target)


def upload_to_s3(filename, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    if object_name is None:
        object_name = os.path.basename(filename)

    s3_client = boto3.client("s3")

    try:
        s3_client.upload_file(filename, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False

    return True


def upload_to_storage(filename, bucket, object_name=None):
    """Upload a file to a Cloud Storage bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    if object_name is None:
        object_name = os.path.basename(filename)

    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)

    try:
        blob.upload_from_filename(filename)
    except GoogleCloudError as e:
        logging.error(e)
        return False

    return True
