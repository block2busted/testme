from testme import app
import secrets
import os
from PIL import Image


def save_photo(form_picture):
    random_hex = secrets.token_hex(8)
    file_name, file_ext = os.path.splitext(form_picture.filename)
    photo_filename = random_hex + file_ext
    photo_path = os.path.join(app.root_path, 'static/profile_pics', photo_filename)
    output_size = (125, 125)
    resized_photo = Image.open(form_picture)
    resized_photo.thumbnail(output_size)
    resized_photo.save(photo_path)
    return photo_filename
