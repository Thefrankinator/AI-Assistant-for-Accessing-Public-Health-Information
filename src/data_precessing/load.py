import pytesseract # pyright: ignore[reportMissingImports]
from pdf2image import convert_from_path # pyright: ignore[reportMissingImports]
from pathlib import Path 
from langchain_community.document_loaders import PyPDFLoader # pyright: ignore[reportMissingImports]
from langchain_core.documents import Document   # pyright: ignore[reportMissingImports]
import pdfplumber # pyright: ignore[reportMissingImports]


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\School\Autres\NLP\AAFAPHI\Release-25.12.0-0\poppler-25.12.0\Library\bin"

def load_pdf_with_ocr(pdf_path: str, lang: str = "fra") -> list:
    """
    Extract text from a scanned PDF using OCR.
    """
    
    documents = []
    # Convert each PDF page to an image
    pages = convert_from_path(pdf_path, dpi=300,poppler_path=POPPLER_PATH)

    
    for i, page_image in enumerate(pages):
        
        document = Document(
            page_content = pytesseract.image_to_string(page_image, lang=lang),
            metadata={
                "source":     None,
                "institution": None,
                "type":       None,
                "langue":     lang,
                "annee":      None,
                "theme":      None,
                "region":     None,
                "page_number": i + 1
            }
        )
        
        documents.append(document)
    
    return documents
    


def load_pdf_with_langchain(pdf_path: str) ->list:
    loader = PyPDFLoader(pdf_path)
    pages = loader.load() 
    
    return pages


def load_pdf_with_pdfplumber(pdf_path: str):
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            print(page.extract_text())     
           



def load_source_1() -> list:
    """Load and process the "Calendrier Vaccinal 2025" PDF using Langchain's PyPDFLoader.

        Args:
            None
            
        returns:
            list: A list of Document objects with enriched metadata for each page.
    """
    source_1 = load_pdf_with_langchain(r"../../data/raw/Calendrier-vaccinal-2025.pdf")

    for page in source_1:
        
        page.metadata = {
            "source":     "Calendrier Vaccinal 2025",
            "institution":"Société Marocaine d'Infectiologie et de Vaccinologie (SOMIPEV)",
            "type":       "guide_recommandations",
            "langue":     "fr",
            "annee":      2025,
            "theme":      "vaccination",
            "region":     "national",
            "page_number": page.metadata.get("page", None)
    }    
    
    doc = source_1.pop(0)
    return source_1




def load_source_2() -> list:
    """Load and process the "Fiches Descriptives des maladies infectieuses en milieu scolaire - Edition 2023-8-24" PDF using Langchain's PyPDFLoader.
    
        Args:
            None
            
        returns:
            list: A list of Document objects with enriched metadata for each page.
    """
    source_2 = load_pdf_with_langchain(r"../../data/raw/Fiches-Descriptives-des-maladies-infectieuses-en-milieu-scolaire-Edition-2023-8-24.pdf")

    for page in source_2:
        
        page.metadata ={
        "source":     "Fiches Descriptives des maladies infectieuses en milieu scolaire",
        "institution":"Comité d'experts marocains (SOMIPEV / Ministère de la Santé)",
        "type":       "guide_recommandations",
        "langue":     "fr",
        "annee":      2023,
        "theme":      "maladies_infectieuses_milieu_scolaire",
        "region":     "national",
        "page_number": page.metadata.get("page", None)
    }
        
    return source_2



def load_source_3() -> list:
    """Load and process the "Guide Marocain de Vaccinologie" PDF using Langchain's PyPDFLoader.
    
        Args:
            None
            
        returns:
            list: A list of Document objects with enriched metadata for each page.
    """
    
    source_3 = load_pdf_with_langchain(r"../../data/raw/Guide-Marocain-de-Vaccinologie-143-158.pdf")
    for page in source_3:
        
        page.metadata = {
        "source":     "Guide Marocain de Vaccinologie",
        "institution":"Société Marocaine d'Infectiologie et de Vaccinologie (SOMIPEV)",
        "type":       "guide_recommandations",
        "langue":     "fr",
        "annee":      2023,
        "theme":      "vaccinologie",
        "region":     "national",
        'page_number': page.metadata.get("page", None)
    }
        
    return source_3



def load_source_4() -> list:
    """Load and process the "L'hépatite A au Maroc: Aspects épidémiologique, facteurs de risque et prévention" PDF using OCR.
    
        Args:
            None
            
        returns:
            list: A list of Document objects with enriched metadata for each page.
    """
    
    source_4  =load_pdf_with_ocr(r"../../data/raw/Lhepatite-A-au-Maroc-Aspects-epidemiologique-facteurs-de-risque-et-prevention-2017-38-55.pdf")

    for page in source_4:
        page.metadata = {
        "source":     "L’hépatite A au Maroc : Aspects épidémiologiques, facteurs de risque et prévention",
        "institution":"Société Marocaine d'Infectiologie et de Vaccinologie (SOMIPEV)",
        "type":       "guide_recommandations",
        "langue":     "fr",
        "annee":      2017,
        "theme":      "hepatite_A",
        "region":     "national",
        "page_number": page.metadata.get("page_number",None)
}
        
    doc = source_4.pop(14)    
    return source_4





def load_source_5() ->list:
    """Load and process the "loi_98-15_amo_independants_francais" PDF using OCR.
    
        Args:
            None
            
        returns:
            list: A list of Document objects with enriched metadata for each page.
    """
    
    source_5 = load_pdf_with_ocr(r"../../data/raw/loi_98-15_amo_independants_francais.pdf")

    for page in source_5:
        
        page.metadata = {
        "source":     "Loi n° 98-15 relative au régime de l'assurance maladie obligatoire de base pour les catégories des professionnels, des travailleurs indépendants et des personnes non salariées exerçant une activité libérale",
        "institution":"Secrétariat Général du Gouvernement (Bulletin Officiel)",
        "type":       "loi_reglementaire",
        "langue":     "fr",
        "annee":      2018,
        "theme":      "assurance_maladie_independants",
        "region":     "national"
    }
        
    return source_5




def load_source_6() ->list:
    """Load and process the "loi_98-15_amo_independants_francais" PDF using OCR.
    
        Args:
            None
            
        returns:
            list: A list of Document objects with enriched metadata for each page.
    """
    
    source_6 = load_pdf_with_ocr(r"../../data/raw/Loi_n_116-12.pdf")

    for page in source_6:
        
        page.metadata = {
        "source":     "Loi n° 116-12 relative au régime de l'assurance maladie obligatoire de base des étudiants",
        "institution":"Secrétariat Général du Gouvernement (Bulletin Officiel)",
        "type":       "loi_reglementaire",
        "langue":     "fr",
        "annee":      2015,
        "theme":      "assurance_maladie_etudiants",
        "region":     "national"
}
        
    return source_6

