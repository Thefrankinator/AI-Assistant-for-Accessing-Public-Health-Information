from load import *
import re
import json


def clean_source_1() -> list:

    source_1 = load_source_1()
    
    text = source_1[0].page_content
    
    text = re.sub(r"\d-\d mois \d..+\n..+\n..+\n..+", " ", text)
    
     # Use re.UNICODE to handle accented uppercase letters 
        # Logic: join line if:
        #   - current line does NOT end with punctuation
        #   - next line does NOT start with uppercase (including accented)
        
    text = re.sub(
            r'(?<![.,:;?!\d])\n(?![A-ZÀÂÉÈÊËÎÏÔÙÛÜÇ0-9\-])',
            ' ',
            text,
            flags=re.UNICODE
        )
    
    
    text = text.replace(
    "BCG","CALENDRIER VACCINAL REFLEXIONS ET PROPOSITION D'UNE HARMONISATION \n 0-6 mois ").replace(
    "Rougeole (R) Oreillons (O) "," 6-12 mois  Rougeole (R) Oreillons (O) " ).replace(
    "DTCa VPI Hib", " 12-18 mois DTCa VPI Hib").replace(
    "DTCe , VPOb ou VPI","5-6 ans DTCe , VPOb ou VPI")
    
    text = re.sub(r"DTCa VPI \n"," 9-15 ans DTCa VPI ",text)
    text = re.sub(r"Grippe saisonnière : \n1",">65 ans Grippe saisonnière :\n1",text)
    
    # Rejoin lines that end mid-word (no punctuation at end)
    text = re.sub(r'(?<![.,:;?!])\n(?![A-Z0-9\-])', ' ', text)

    lines = [line.strip() for line in text.splitlines()]

    text = re.sub(r'\n{3,}', '\n\n', '\n'.join(lines))
    
    age_groups = [
        "0-6 mois", "6-12 mois", "12-18 mois", "5-6 ans", "9-15 ans", ">65 ans"]

    for age in age_groups:
        text = re.sub(
            rf'({re.escape(age)})\s+(?!:)',
            rf'\n\1:\n ',
            text
        )

    text = re.sub(r'  +', ' ', text)
    text = re.sub(r'^\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    source_1[0].page_content = text
    
    for pg in source_1[1:]:
        
        text = pg.page_content
        
        text = re.sub(
            r'(?<![.,:;?!\d])\n(?![A-ZÀÂÉÈÊËÎÏÔÙÛÜÇ0-9\-])',
            ' ',
            text,
            flags=re.UNICODE
        )
    
        text = re.sub(r'  +', ' ', text)
        text = re.sub(r'^\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
    
    return source_1



def clean_source_2() -> list:
    
    def fiches_descriptives_preprocessing(text):
        
        # "céphalo-\nrachidien" → "céphalo-rachidien"
        text = re.sub(r'-\n(\w)', r'-\1', text)

        text = re.sub(
            r'(?<![.,:;?!\d])\n(?![A-ZÀÂÉÈÊËÎÏÔÙÛÜÇ0-9\-])',
            ' ',
            text,
            flags=re.UNICODE
        )

        #Extract page number, year and organization from the header line of a SOMIPEV document.
        text = re.sub(r'^\d+\s+((?:19|20)\d{2})\s+([A-Z]+)\s*', '', text)
        text = re.sub(r'  +', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r"Maladies infectieuses en milieu scolaire",' ',text)
        
        
        field_names = [
            "Définition", "Réservoir", "Période d'incubation",
            "Période de contagiosité", "Période de contagiosité", "Durée de la maladie",
            "Mode de transmission", "Tableau clinique",
            "Complications", "Particularité de la femme enceinte",
            "Diagnostic", "Traitement", "Pronostic","Prévention","Recommandation (éviction)"
        ]
        for field in field_names:
            # Add colon if field name is not already followed by ":"
            text = re.sub(
                rf'({re.escape(field)})\s+(?!:)',
                rf'\1: ',
                text
            )

        # Put each field on its own line for clean chunking
        for field in field_names:
            text = text.replace(field, f"\n{field}")

        
        
        
        return text.strip()
    
    source_2 = load_source_2()
    for doc in source_2:
        doc.page_content = fiches_descriptives_preprocessing(doc.page_content)
       
    return source_2




def clean_source_3() -> list:
    
    source_3 = load_source_3()
    for doc in source_3:
        
        text = doc.page_content
        text = re.sub(r'^\d+\s',' ',text)
        text = re.sub(
            r'(?<![.,:;?!\d])\n(?![A-ZÀÂÉÈÊËÎÏÔÙÛÜÇ0-9\-])',
            ' ',
            text,
            flags=re.UNICODE
        )
        text = re.sub(r'  +', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        doc.page_content = text
        
    
    return source_3





def clean_source_4() -> list:
    
    source_4 = load_source_4()
    
    for doc in source_4:
        text = doc.page_content
        text = re.sub(r'^\d+$', '', text, flags=re.MULTILINE)
        
        text = re.sub(r'  +', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(
            r'(?<![.,:;?!\d])\n(?![A-ZÀÂÉÈÊËÎÏÔÙÛÜÇ0-9\-])',
            ' ',
            text,
            flags=re.UNICODE    
        )
        
        doc.page_content = text
    
    return source_4
        


def clean_source_5() -> list:
    
    source_5 = load_source_5()
    
    for doc in source_5:
        text = doc.page_content
        
        text = re.sub(
        r'N°\s6662\s—\s18\srejeb\s1439\s.+',
        '',text)
        
        text = re.sub(
        r'BULLETIN\s+OFFICIEL\s+\d+|^\d+\sBULLETIN\sOFFICIEL',
        '',text,flags=re.UNICODE)
        
        text = re.sub(r'  +', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(
            r'(?<![.,:;?!\d])\n(?![A-ZÀÂÉÈÊËÎÏÔÙÛÜÇ0-9\-])',
            ' ',
            text,
            flags=re.UNICODE    
        )
        
        doc.page_content = text
        
    return source_5




def clean_source_6() -> list:
    
    source_6 = load_source_6()
    
    for doc in source_6:
        text = doc.page_content
        
        text = re.sub(
        r'N°\s6400\s-\s17\shija\s1436\s.+|N°\s6400\s17\shija\s1436\s.+',
        '',text)
        
        text = re.sub(
        r'BULLETIN\s+OFFICIEL\s+\d+|^\d+\sBULLETIN\sOFFICIEL',
        '',text,flags=re.UNICODE)
        
        text = re.sub(r'  +', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(
            r'(?<![.,:;?!\d])\n(?![A-ZÀÂÉÈÊËÎÏÔÙÛÜÇ0-9\-])',
            ' ',
            text,
            flags=re.UNICODE    
        )
        
        doc.page_content = text
        
    return source_6






# save cleaned documents in the folder \data\preprossed\cleaned

with open(r"../../data/preprossed/cleaned/cleaned_source_1.txt", "w",encoding="utf-8") as f:
    for doc in clean_source_1():
        f.write(doc.page_content + "\n")
        

with open(r"../../data/preprossed/cleaned/cleaned_source_2.txt", "w",encoding="utf-8") as f:
    for doc in clean_source_2():
        f.write(doc.page_content + "\n")

with open(r"../../data/preprossed/cleaned/cleaned_source_3.txt", "w",encoding="utf-8") as f:
    for doc in clean_source_3():
        f.write(doc.page_content + "\n")
        
with open(r"../../data/preprossed/cleaned/cleaned_source_4.txt", "w",encoding="utf-8") as f:
    for doc in clean_source_4():
        f.write(doc.page_content + "\n")
        
with open(r"../../data/preprossed/cleaned/cleaned_source_5.txt", "w",encoding="utf-8") as f:
    for doc in clean_source_5():
        f.write(doc.page_content + "\n")

with open(r"../../data/preprossed/cleaned/cleaned_source_6.txt", "w",encoding="utf-8") as f:
    for doc in clean_source_6():
        f.write(doc.page_content + "\n")

# save the metatdata of each source in a json file

with open(r"../../data/preprossed/cleaned/metadata_source_1.json", "w", encoding="utf-8") as f:
    json.dump([clean_source_1()[0].metadata], f)

with open(r"../../data/preprossed/cleaned/metadata_source_2.json", "w", encoding="utf-8") as f:
    json.dump([clean_source_2()[0].metadata], f)

with open(r"../../data/preprossed/cleaned/metadata_source_3.json", "w", encoding="utf-8") as f:
    json.dump([clean_source_3()[0].metadata], f)

with open(r"../../data/preprossed/cleaned/metadata_source_4.json", "w", encoding="utf-8") as f:
    json.dump([clean_source_4()[0].metadata], f)

with open(r"../../data/preprossed/cleaned/metadata_source_5.json", "w", encoding="utf-8") as f:
    json.dump([clean_source_5()[0].metadata], f)

with open(r"../../data/preprossed/cleaned/metadata_source_6.json", "w", encoding="utf-8") as f:
    json.dump([clean_source_6()[0].metadata], f)
