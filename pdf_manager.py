import fitz
import os
import PIL.Image as PILImage
import io

def extract_images_from_pdf(pdf_path, output_folder):
    try:
        doc = fitz.open(pdf_path)
        for i in range(len(doc)):
            for img_index, img in enumerate(doc[i].get_images(full=True)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image['image']
                image_ext = base_image['ext']
                image_path = os.path.join(output_folder, f"extracted_image_{i}_{img_index}.{image_ext}")
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)
                print(f"Saved: {image_path}")
        doc.close()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def convert_pdf_to_images(pdf_path, dpi=300):
    try:
        doc = fitz.open(pdf_path)
        images = []
        zoom = dpi / 72
        matrix = fitz.Matrix(zoom, zoom)
        for page_number in range(len(doc)):
            page = doc.load_page(page_number)
            pix = page.get_pixmap(matrix=matrix)
            img_bytes = pix.tobytes("ppm")
            image = PILImage.open(io.BytesIO(img_bytes))
            images.append(image)
        doc.close()
        return images
    except Exception as e:
        print(f"Error converting PDF pages to images: {str(e)}")
        return []