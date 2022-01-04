import aiofiles
import uuid
from fastapi import FastAPI, UploadFile, File, Form
from steganography import encode_text_in_image, decode_text_in_image, encode_image_in_image, decode_image_in_image
from fastapi.staticfiles import StaticFiles


app = FastAPI(
    title="Steganography API",
    description="Hide text in image or even image in image itself.",
    version="1.0",
)
app.mount("/images", StaticFiles(directory="images"), name="images")

BASE_URL = "http://127.0.0.1:8000/"


@app.post("/encode-text/", tags=["Hide Text In Image"])
async def encode_text(text: str = Form(...), password: str = Form(...), image : UploadFile = File(...)):
    filename = 'images/' + str(uuid.uuid4()) + '.png'
    async with aiofiles.open(filename, 'wb') as out_file:
        while content := await image.read(1024):
            await out_file.write(content)
    encoded_image = encode_text_in_image(text, password, filename)
    encoded_image_url = BASE_URL + encoded_image
    return {"status" : "success", "image_url" : encoded_image_url}


@app.post("/decode-text/", tags=["Hide Text In Image"])
async def decode_text(password: str = Form(...), image : UploadFile = File(...)):
    filename = 'images/' + str(uuid.uuid4()) + '.png'
    async with aiofiles.open(filename, 'wb') as out_file:
        while content := await image.read(1024):
            await out_file.write(content)
    decoded_text = decode_text_in_image(password, filename)
    if decoded_text:
        return {'status' : 'success', 'message' : decoded_text}
    else:
        return {'status' : 'error'}


@app.post("/encode-image/", tags=["Hide Image In Image"])
async def encode_image(password: str = Form(...), source_image : UploadFile = File(...), destination_image : UploadFile = File(...)):
    source_filename = 'images/' + str(uuid.uuid4()) + '.png'
    destination_filename = 'images/' + str(uuid.uuid4()) + '.png'
    async with aiofiles.open(source_filename, 'wb') as out_file:
        while content := await source_image.read(1024):
            await out_file.write(content)
    async with aiofiles.open(destination_filename, 'wb') as out_file:
        while content := await destination_image.read(1024):
            await out_file.write(content)
    encoded_image = encode_image_in_image(password, source_filename, destination_filename)
    encoded_image_url = BASE_URL + encoded_image
    return {"status" : "success", "image_url" : encoded_image_url}
    

@app.post("/decode-image/", tags=["Hide Image In Image"])
async def decode_image(password: str = Form(...), image : UploadFile = File(...)):
    filename = 'images/' + str(uuid.uuid4()) + '.png'
    async with aiofiles.open(filename, 'wb') as out_file:
        while content := await image.read(1024):
            await out_file.write(content)
    decoded_image = decode_image_in_image(password, filename)
    if decoded_image:
        decoded_image_url = BASE_URL + decoded_image
        return {"status" : "success", "image_url" : decoded_image_url}
    else:
        return {'status' : 'error'}