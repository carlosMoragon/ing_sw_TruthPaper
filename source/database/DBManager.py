from PIL import Image
from io import BytesIO
import base64

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# def transform_images_to_base64(photo_bytes):
#     pil_image = Image.open(BytesIO(photo_bytes))
#     if pil_image.mode == 'RGBA':
#         pil_image = pil_image.convert('RGB')
#     base64_image = base64.b64encode(photo_bytes).decode('utf-8')
#     return base64_image

