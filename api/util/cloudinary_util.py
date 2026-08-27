import cloudinary
import cloudinary.uploader
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def upload_to_cloudinary(local_path, folder="portfolio_uploads", resource_type=None):
    """
    Uploads a local file to Cloudinary and deletes the local file after success.
    
    Args:
        local_path (str/file): The file or path to upload.
        folder (str): The folder in Cloudinary to store the file. Defaults to "portfolio_uploads".
        resource_type (str): "auto", "raw", or "image". Auto-detected for PDFs if omitted.
        
    Returns:
        dict: The Cloudinary upload result dictionary.
    """
    try:
        # Auto-detect raw resource_type for PDF files to avoid Cloudinary 401 ACL errors
        if not resource_type:
            filename = getattr(local_path, 'name', str(local_path)).lower()
            if filename.endswith('.pdf') or 'pdf' in folder.lower() or 'resume' in folder.lower():
                resource_type = "raw"
            else:
                resource_type = "auto"

        # Check if settings are configured
        if hasattr(settings, 'CLOUDINARY_STORAGE'):
             # Configure cloudinary with settings
            cloudinary.config(
                cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
                api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
                api_secret=settings.CLOUDINARY_STORAGE['API_SECRET']
            )

        # Upload the file
        logger.info(f"Uploading file: {local_path} to folder: {folder} (resource_type: {resource_type})")
        result = cloudinary.uploader.upload(
            local_path,
            folder=folder,
            resource_type=resource_type
        )

        # Delete local file after upload ONLY if it's a path string
        if isinstance(local_path, str) and os.path.exists(local_path):
            os.remove(local_path)
            logger.info(f"Deleted local file: {local_path}")

        logger.info(f"File uploaded successfully to Cloudinary: {result.get('secure_url')}")

        return result

    except Exception as error:
        logger.error(f"Error uploading to Cloudinary: {error}")
        raise error
