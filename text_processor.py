import re
from spacy import load

nlp = load('en_core_web_sm')

def clean_text_advanced(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\bhttps?:\/\/\S+\b', '', text)
    text = re.sub(r'[()&]', '', text)
    doc = nlp(text)
    cleaned_parts = [ent.text for ent in doc.ents]
    non_entity_parts = re.sub(r'\b(' + '|'.join(re.escape(ent.text) for ent in doc.ents) + r')\b', '', text)
    non_entity_parts = re.sub(r'[^\w\s,.]', '', non_entity_parts)
    final_text = ' '.join(cleaned_parts + [non_entity_parts]).strip()
    return final_text