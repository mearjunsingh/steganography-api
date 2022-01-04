import aiofiles
import uuid
from fastapi import FastAPI, UploadFile, File, Form
from starlette.responses import FileResponse, Response
from steganography import encode_text_in_image, decode_text_in_image, encode_image_in_image, decode_image_in_image
from fastapi.staticfiles import StaticFiles
import base64


app = FastAPI(
    title="Steganography API",
    description="Hide text in image or even image in image itself.",
    version="1.0",
)
app.mount("/images", StaticFiles(directory="images"), name="images")


@app.post("/encode-text/", tags=["Hide Text In Image"])
async def encode_text(text: str = Form(...), password: str = Form(...), image : UploadFile = File(...)):
    filename = 'images/' + str(uuid.uuid4()) + '.png'
    async with aiofiles.open(filename, 'wb') as out_file:
        while content := await image.read(1024):
            await out_file.write(content)
        encoded_image = encode_text_in_image(text, password, filename)
    with open(encoded_image, "rb") as image_file:
        encoded_image_string = base64.b64encode(image_file.read())
    return {"encoded_image" : encoded_image_string}


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
        return {'status' : 'error', 'message' : 'either password mistake or invalid image'}


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
    return FileResponse(encoded_image)
    

@app.post("/decode-image/", tags=["Hide Image In Image"])
async def decode_image(password: str = Form(...), image : UploadFile = File(...)):
    filename = 'images/' + str(uuid.uuid4()) + '.png'
    async with aiofiles.open(filename, 'wb') as out_file:
        while content := await image.read(1024):
            await out_file.write(content)
        decoded_image = decode_image_in_image(password, filename)
    if decoded_image:
        return FileResponse(decoded_image)
    else:
        return Response('either password mistake or invalid image')