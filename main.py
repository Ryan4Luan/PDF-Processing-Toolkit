import os
import sys
from pdf_processing import extract_text_from_images, clean_text_advanced, extract_and_save_images, convert_pdf_to_images_in_memory

def save_text(file_path, text):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

def ensure_dir(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

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
    extract_and_save_images(pdf_path, embedded_images_dir)

    print("\nConverting PDF pages to images and extracting text...")
    converted_images = convert_pdf_to_images_in_memory(pdf_path)

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