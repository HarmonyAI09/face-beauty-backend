import os
import datetime
import hashlib
from fastapi import UploadFile
from PIL import Image

UPLOAD_DIR = "UPLOADS"
DEFAULT_LENGTH = 800

def storeImage(image:UploadFile):
    # Create a folder if it doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save the uploaded image to the folder
    currentTime = datetime.now()
    imageID = hashlib.md5(str(currentTime).encode()).hexdigest()
    imageFileName = imageID + ".jpg"
    imageStorePath = os.path.join(UPLOAD_DIR, imageFileName)
    imageSrc = Image.open(image.file)
    if imageSrc.width > imageSrc.height:
        width = DEFAULT_LENGTH
        height = int(imageSrc.height*DEFAULT_LENGTH/imageSrc.width)
    else:
        height = DEFAULT_LENGTH
        width = int(imageSrc.width*DEFAULT_LENGTH/imageSrc.height)
    imageResize = imageSrc.resize((width, height))
    imageResize.save(imageStorePath)