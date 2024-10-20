from fastapi import UploadFile
import shutil

from pydantic import BaseModel


def load_photo(model: BaseModel , file: UploadFile):
    im_path = f"static/img/{model.__class__.__name__}{model.name}.webp"
    with open(im_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    return im_path