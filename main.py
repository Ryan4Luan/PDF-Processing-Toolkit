import sys
import os
from pdf_manager import extract_images_from_pdf, convert_pdf_to_images
from image_processor import extract_text_from_images
from text_processor import clean_text_advanced
from utilities import ensure_dir, save_text

def main():
    print("Please enter the full path to the PDF file:")
    pdf_path = input().strip()
    if not pdf_path:
        print("No path entered. Exiting.")
        sys.exit()

    if not os.path.exists(pdf_path):
        print("File does not exist. Please check the path and try again.")
        sys.exit()

    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_dir = os.path.join('output', base_name)
    text_dir = os.path.join(output_dir, 'text')
    ensure_dir(text_dir)

    print("\nExtracting embedded images...")
    embedded_images_dir = os.path.join(output_dir, 'embedded_images')
    ensure_dir(embedded_images_dir)
    extract_images_from_pdf(pdf_path, embedded_images_dir)

    print("\nConverting PDF pages to images and extracting text...")
    converted_images = convert_pdf_to_images(pdf_path)

    print("\nExtracting text from images...")
    texts = extract_text_from_images(converted_images)  # Pass the image objects directly

    print("\nApplying advanced text cleaning...")
    advanced_cleaned_texts = [clean_text_advanced(text) for text in texts]

    # Saving advanced cleaned texts to files
    for i, text in enumerate(advanced_cleaned_texts):
        text_file_path = os.path.join(text_dir, f"advanced_cleaned_text_{i}.txt")
        save_text(text_file_path, text)

    print(f"\nAdvanced cleaned texts saved to files in {text_dir}.")

if __name__ == '__main__':
    main()