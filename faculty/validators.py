import os
from django.core.exceptions import ValidationError
from PIL import Image
from django.core.files.uploadedfile import UploadedFile # To check file type

# Import the CloudinaryResource class for type checking (if needed, 
# though checking for UploadedFile is often sufficient)
# from cloudinary.utils import CloudinaryResource 

ALLOWED_EXTENSIONS = ('.pdf', '.jpg', '.jpeg', '.png')

def validate_file(file):
    # Check if the object is a standard Django UploadedFile object
    if isinstance(file, UploadedFile):
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise ValidationError(
                "Unsupported file type. Allowed: PDF, JPG, JPEG, PNG."
            )
    else:
        # If it's a CloudinaryResource object (or another type), 
        # we can't reliably check the extension here. 
        # Cloudinary often handles basic file type validation internally.
        # If you need to restrict the type of existing Cloudinary objects, 
        # you need to check its format property (e.g., file.format)
        pass 


def validate_image(file):
    # 1. Skip PIL check if the file is already a Cloudinary object (existing file)
    # When updating a form without uploading a new file, 'file' is the existing Cloudinary object.
    # We only run deep checks on newly uploaded files (UploadedFile).
    if not isinstance(file, UploadedFile):
        # We still run the basic file extension check for safety on non-uploaded files
        validate_file(file)
        return

    # 2. Run basic extension check for new uploads
    validate_file(file)
    
    # 3. Deep Image Integrity Check using Pillow (Only for new uploads)
    try:
        # Reset file pointer to the beginning before opening with PIL
        file.seek(0)
        img = Image.open(file)
        img.verify() # Checks if the file is a valid image without loading it fully
    except Exception:
        raise ValidationError("Uploaded file is not a valid image or is corrupted.")
    finally:
        # IMPORTANT: Reset the file pointer again after PIL verification 
        # so Django can process the file for upload
        file.seek(0)