import os

def ensure_dir(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

def save_text(file_path, text):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)