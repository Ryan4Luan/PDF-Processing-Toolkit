import fitz  
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from pdf2image import convert_from_path
import PIL.Image as Image
import re
from spacy import load
import os
import io

def convert_pdf_to_images_in_memory(pdf_path, dpi=300):
    doc = fitz.open(pdf_path)
    images = []
    zoom = dpi / 72  # 默认DPI为72，调整到所需的DPI
    matrix = fitz.Matrix(zoom, zoom)  # 创建转换矩阵

    for page_number in range(len(doc)):
        page = doc.load_page(page_number)
        pix = page.get_pixmap(matrix=matrix)  # 应用转换矩阵
        img_bytes = pix.tobytes("ppm")  # 将图像数据转换为PPM格式
        image = Image.open(io.BytesIO(img_bytes))  # 使用Pillow从内存数据创建图像
        images.append(image)
    doc.close()
    return images

def extract_text_from_images(images):
    text_outputs = []
    for image in images:
        text = pytesseract.image_to_string(image)  # Directly use the image object
        text_outputs.append(text)
    return text_outputs

def extract_and_save_images(pdf_path, output_folder):
    doc = fitz.open(pdf_path)
    for i in range(len(doc)):
        for img_index, img in enumerate(doc[i].get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_path = f"{output_folder}/extracted_image_{i}_{img_index}.{image_ext}"
            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)
            print(f"Saved: {image_path}")
    doc.close()

def clean_text_advanced(text):
    nlp = load('en_core_web_sm')
    text = re.sub(r'\\s+', ' ', text)
    text = re.sub(r'\\bhttps?:\\/\\/\\S+\\b', '', text)
    text = re.sub(r'[()&]', '', text)
    doc = nlp(text)
    cleaned_parts = [ent.text for ent in doc.ents]
    non_entity_parts = re.sub(r'\\b(' + '|'.join(re.escape(ent.text) for ent in doc.ents) + r')\\b', '', text)
    non_entity_parts = re.sub(r'[^\w\s,.]', '', non_entity_parts)
    final_text = ' '.join(cleaned_parts + [non_entity_parts]).strip()
    return final_text
    