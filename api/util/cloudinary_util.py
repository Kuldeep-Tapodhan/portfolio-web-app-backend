import cloudinary
import cloudinary.uploader
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def upload_to_cloudinary(local_path, folder="portfolio_uploads"):
    """
    Uploads a local file to Cloudinary and deletes the local file after success.
    
    Args:
        local_path (str): The absolute path to the local file to upload.
        folder (str): The folder in Cloudinary to store the file. Defaults to "portfolio_uploads".
        
    Returns:
        dict: The Cloudinary upload result dictionary.
        
    Raises:
        Exception: If the upload fails.
    """
    try:
        # Check if settings are configured
        if hasattr(settings, 'CLOUDINARY_STORAGE'):
             # Configure cloudinary with settings
            cloudinary.config(
                cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
                api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
                api_secret=settings.CLOUDINARY_STORAGE['API_SECRET']
            )

        # Upload the file
        logger.info(f"Uploading file: {local_path} to folder: {folder}")
        result = cloudinary.uploader.upload(
            local_path,
            folder=folder,
            resource_type="auto" # Auto detect file type (image, video, raw for pdf etc)
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
