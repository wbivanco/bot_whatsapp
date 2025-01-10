import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
from typing import List, Tuple

from base.load_env import load_env

from apps.chatbot.routes import create_embeddings

load_env()
upload_directory = os.getenv("PATH_TO_UPLOAD_FOLDER")

router = APIRouter()

class PDFRequest(BaseModel):
    files: List[dict]  # Lista de diccionarios con "filename", "title", "subtitle" y "url"

def scrape_page_grado(url: str) -> List[Tuple[str, List[str]]]:
    """
    Extrae las secciones y sus elementos de una página web.

    Args:
        url (str): URL de la página a analizar.

    Returns:
        List[Tuple[str, List[str]]]: Lista de secciones con títulos y sus respectivos elementos.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')

        # Extraer el contenido entre <p><strong> y </strong></p> y sus correspondientes listados de carreras
        sections = []
        for p in soup.find_all('p'):
            strong_tag = p.find('strong')
            if strong_tag:
                section_title = strong_tag.get_text()
                next_sibling = p.find_next_sibling()
                if next_sibling and next_sibling.name == 'ul':
                    list_items = [li.get_text() for li in next_sibling.find_all('li')]
                    sections.append((section_title, list_items))
        return sections
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error al procesar la URL {url}: {str(e)}")

def scrape_page_posgrado(url: str) -> List[Tuple[str, List[str]]]:
    """
    Extrae las secciones "Carreras" y "Especializaciones" de una página de postgrado.

    Args:
        url (str): URL de la página a analizar.

    Returns:
        List[Tuple[str, List[str]]]: Lista de secciones "Carreras" y "Especializaciones" con sus elementos.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')

        # Buscar el contenedor principal
        main_container = soup.find('div', id='maininner')
        if not main_container:
            raise Exception("No se encontró el contenedor principal con id 'maininner'")

        sections = []
        current_section_title = None
        current_section_items = []

        for child in main_container.find_all(['p', 'ul'], recursive=True):
            # Detectar títulos de secciones en negrita
            strong_tag = child.find('strong')
            if strong_tag:
                # Guardar la sección anterior si aplica
                if current_section_title in ["Carreras:", "Especializaciones"] and current_section_items:
                    sections.append((current_section_title, current_section_items))
                current_section_title = strong_tag.get_text(strip=True)
                current_section_items = []

            # Detectar listas <ul> y extraer elementos
            if child.name == 'ul' and current_section_title in ["Carreras:", "Especializaciones"]:
                for li in child.find_all('li'):
                    link = li.find('a')
                    if link:
                        current_section_items.append(link.get_text(strip=True))

        # Agregar la última sección si corresponde
        if current_section_title in ["Carreras", "Especializaciones"] and current_section_items:
            sections.append((current_section_title, current_section_items))

        return sections
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error al procesar la URL {url}: {str(e)}")

def scrape_page_diplomatura(url: str) -> List[Tuple[str, List[str]]]:
    """
    Extrae las secciones y sus elementos de una página web.

    Args:
        url (str): URL de la página a analizar.

    Returns:
        List[Tuple[str, List[str]]]: Lista de secciones con títulos y sus respectivos elementos.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')

        # Buscar el contenedor principal
        main_container = soup.find('div', id='maininner')
        if not main_container:
            raise Exception("No se encontró el contenedor principal con id 'maininner'")

        # Buscar el contenido dentro de la lista <ul>
        ul_element = main_container.find('ul')
        if not ul_element:
            raise Exception("No se encontró la lista <ul> en el contenedor principal")

        # Extraer los elementos de la lista <li>
        sections = []
        section_title = "Diplomaturas"  # Título fijo, ya que no hay múltiples secciones claras
        list_items = []

        for li in ul_element.find_all('li'):
            link = li.find('a')
            if link:
                list_items.append(link.get_text(strip=True))
            else:
                list_items.append(li.get_text(strip=True))

        sections.append((section_title, list_items))
        return sections

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error al procesar la URL {url}: {str(e)}")

def generate_pdf(filename: str, title: str, subtitle: str, sections: List[Tuple[str, List[str]]], output_dir: str = upload_directory):
    """
    Genera un archivo PDF con el contenido proporcionado.

    Args:
        filename (str): Nombre del archivo PDF.
        title (str): Título del PDF.
        subtitle (str): Subtítulo del PDF.
        sections (List[Tuple[str, List[str]]]): Contenido del PDF, con títulos y elementos.
        output_dir (str): Directorio de salida para guardar el PDF.
    """
    # Crear directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, title, ln=True, align='C')
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(0, 10, subtitle, ln=True, align='C')
    pdf.ln(10)

    for section_title, list_items in sections:
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, section_title, ln=True)
        pdf.set_font("Arial", size=12)
        for item in list_items:
            pdf.multi_cell(0, 10, f"- {item}")
    
    filepath = os.path.join(output_dir, f"{filename}.pdf")
    pdf.output(filepath)
    return filepath

@router.post("/generate_pdfs/")
async def generate_pdfs(request: PDFRequest):
    """
    Genera archivos PDF para cada entrada en la lista proporcionada.
    """
    try:
        output_files = []
        for file_info in request.files:
            filename = file_info["filename"]
            title = file_info["title"]
            subtitle = file_info["subtitle"]
            url = file_info["url"]

            if filename == 'Grado':
                sections = scrape_page_grado(url)
            elif filename == 'Posgrado':
                sections = scrape_page_posgrado(url) 
            elif filename == 'Diplomaturas':
                sections = scrape_page_diplomatura(url)
            
            pdf_path = generate_pdf(filename, title, subtitle, sections)
            output_files.append(pdf_path)
            create_embeddings()
        
        return {"message": "Archivos PDF generados correctamente. Base de conocimiento generada exitosamente.", "files": output_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
