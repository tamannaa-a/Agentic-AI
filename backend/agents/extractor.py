# agents/extractor.py
import re
import pdfplumber
import os
from typing import Dict

nlp = None
try:
    import spacy
    nlp = spacy.load('en_core_web_sm')
except Exception:
    nlp = None

def extract_text_from_pdf(path: str) -> str:
    try:
        text = ''
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception:
        return ''

def simple_entity_extraction(text: str) -> Dict:
    res = {}
    m = re.search(r"(CLM|Claim)[-_ ]?(\d{3,})", text, re.IGNORECASE)
    if m:
        res['claim_id'] = m.group(0)
    m2 = re.search(r"\b(?:Rs\.?|INR|USD|EUR|£|\$) ?([0-9,]+(?:\.[0-9]{1,2})?)", text)
    if m2:
        amt = m2.group(1).replace(',', '')
        try:
            res['claim_amount'] = float(amt)
        except:
            pass
    m3 = re.search(r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", text)
    if m3:
        res['date'] = m3.group(0)

    keywords = []
    for kw in ['fraud', 'accident', 'collision', 'hail', 'theft', 'fire', 'flood']:
        if kw.lower() in text.lower():
            keywords.append(kw)
    res['keywords'] = keywords

    return res

def extract_entities_from_file(filepath: str = '', text_override: str = None) -> Dict:
    if text_override:
        text = text_override
    else:
        text = ''
        if filepath and os.path.exists(filepath):
            if filepath.lower().endswith('.pdf'):
                text = extract_text_from_pdf(filepath)
            else:
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        text = f.read()
                except:
                    text = ''

    result = simple_entity_extraction(text)

    if nlp and text:
        try:
            doc = nlp(text[:5000])
            ents = {}
            for ent in doc.ents:
                ents.setdefault(ent.label_, set()).add(ent.text)
            ents = {k: list(v) for k, v in ents.items()}
            result['ner_preview'] = ents
        except Exception:
            pass

    result['raw_text_snippet'] = text[:2000]
    result['full_text_length'] = len(text)
    return result
