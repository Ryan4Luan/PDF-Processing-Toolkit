import pytesseract
from PIL import Image
import io

def extract_text_from_images(images):
    text_outputs = []
    for image in images:
        text = pytesseract.image_to_string(image)
        text_outputs.append(text)
    return text_outputs