import boto3
from django.conf import settings
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)

class R2Storage:
    """Handler untuk upload/delete file ke Cloudflare R2"""
    
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=settings.R2_ENDPOINT_URL,
            aws_access_key_id=settings.R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
            region_name='auto'
        )
        self.bucket_name = settings.R2_BUCKET_NAME
    
    def upload_file(self, file_obj, filename):
        """
        Upload file ke R2
        Args:
            file_obj: File object dari request.FILES
            filename: Nama file yang akan disimpan di R2
        Returns:
            dict: {'success': bool, 'filename': str, 'url': str, 'error': str}
        """
        try:
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                filename,
                ExtraArgs={
                    'ContentType': file_obj.content_type,
                }
            )
            
            file_url = f"{settings.R2_PUBLIC_URL}/{filename}"
            logger.info(f"File uploaded successfully: {filename}")
            
            return {
                'success': True,
                'filename': filename,
                'url': file_url,
                'error': None
            }
        except ClientError as e:
            error_msg = f"Failed to upload file: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'filename': None,
                'url': None,
                'error': error_msg
            }
    
    def delete_file(self, filename):
        """
        Delete file dari R2
        Args:
            filename: Nama file yang akan dihapus
        Returns:
            dict: {'success': bool, 'error': str}
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=filename
            )
            logger.info(f"File deleted successfully: {filename}")
            return {'success': True, 'error': None}
        except ClientError as e:
            error_msg = f"Failed to delete file: {str(e)}"
            logger.error(error_msg)
            return {'success': False, 'error': error_msg}
    
    def file_exists(self, filename):
        """Check apakah file exists di R2"""
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=filename)
            return True
        except ClientError:
            return False
