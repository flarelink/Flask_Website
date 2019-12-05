import os
import glob
from PIL import Image
from flask import current_app


# save face privacy image
def save_face_picture(form_picture):
    picture_fn = form_picture.filename
    picture_path = os.path.join(current_app.root_path, 'static/face_image', picture_fn)

    output_size_max = (512, 512)
    maxwidth, maxheight = output_size_max[0], output_size_max[1]

    i = Image.open(form_picture)
    width, height = i.size
    ratio = min(maxwidth / width, maxheight / height)
    new_output_size = (round(width*ratio), round(height * ratio))

    i = i.resize((new_output_size), Image.ANTIALIAS)
    i.save(picture_path)

    return picture_fn


# remove all face image files
def remove_face_images():
    path = (os.path.join(current_app.root_path, 'static/face_image/*'))
    files = glob.glob(path)
    for f in files:
        os.remove(f)
