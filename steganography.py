import uuid
from cryptosteganography import CryptoSteganography


def encode_text_in_image(text, password, image_name):
    crypto_steganography = CryptoSteganography(password)
    filename = 'images/' + str(uuid.uuid4()) + '.png'
    crypto_steganography.hide(image_name, filename, text)
    return filename


def decode_text_in_image(password, input_image):
    crypto_steganography = CryptoSteganography(password)
    decoded_text = crypto_steganography.retrieve(input_image)
    return decoded_text


def encode_image_in_image(password, source, destination):
    message = None
    with open(source, "rb") as f:
        message = f.read()
    crypto_steganography = CryptoSteganography(password)
    filename = 'images/' + str(uuid.uuid4()) + '.png'
    crypto_steganography.hide(destination, filename, message)
    return filename


def decode_image_in_image(password, image):
    crypto_steganography = CryptoSteganography(password)
    decrypted_bin = crypto_steganography.retrieve(image)
    filename = 'images/' + str(uuid.uuid4()) + '.png'
    with open(filename, 'wb') as f:
        f.write(decrypted_bin)
    return filename