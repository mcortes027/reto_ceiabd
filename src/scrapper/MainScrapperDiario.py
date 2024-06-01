#import os, sys
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scrappers.Scrapper import ScrapperBOC
from storage.ChromaVectorStore import ChromaVectorStore
from loadpdf.LoadPDF import LoadPDF

from tqdm import tqdm
from colorama import Fore, Style
from datetime import datetime
import os

import basura.chatbot.NumBOC as NumBOC





def cabecera():
    print(Fore.RED + r" ____                                       ____              ")
    print(Fore.RED + r"/ ___|  ___ _ __ __ _ _ __  _ __   ___ _ __|  _ \  __ _ _   _ ") 
    print(Fore.RED + r"\___ \ / __| '__/ _` | '_ \| '_ \ / _ \ '__| | | |/ _` | | | |")
    print(Fore.RED + r" ___) | (__| | | (_| | |_) | |_) |  __/ |  | |_| | (_| | |_| |")
    print(Fore.RED + r"|____/ \___|_|  \__,_| .__/| .__/ \___|_|  |____/ \__,_|\__, |")
    print(Fore.RED + r"                     |_|   |_|                          |___/ ")
    print(Fore.MAGENTA + r"--------------------------------------------------------------")
    print(Fore.RED + "                                                      Equipo A\n")
    print(Style.RESET_ALL)

def obtener_ultimo_documento():
   
    result = NumBOC.get_ultimo_numero() #<-------------------- TODO
    
    if result == -1:
        return 0
    elif result == -2:
        raise Exception("Error al conectar con la base de datos")
    else:
        return result[0]
    


def main():
    date = datetime.now().date()
    carpeta = f'../data/dia{date}'
    
    url_base_boc = "https://boc.cantabria.es/boces/verAnuncioAction.do?idAnuBlob="
    inicio_scrapper = obtener_ultimo_documento() + 1
    ultimo_scrapper = inicio_scrapper + 500
    
    print(f"Ultimo documento descargado: {inicio_scrapper-1}")
    print(f"Descargando documentos desde {inicio_scrapper} hasta {ultimo_scrapper-1}...")
    
    bocday = ScrapperBOC(url_base_boc,procesos=20, carpeta=carpeta, start=inicio_scrapper, end=ultimo_scrapper, paciencia=-1)
    bocday.run()
    tiempo, unidad = bocday.tiempo_de_descargar()
    
    print(f"Tiempo total: {tiempo} {unidad} en la descarga de los documentos del día {date}") 
    
    loaderPDF = LoadPDF(carpeta_pdf=carpeta)
    vectorBD = ChromaVectorStore() #<---- Para despliegue en producción añadir host os.environ["CHROMA_HOST"] y port os.environ["OLLAMA_HOST"]
    
    print("Cargando PDFs en la base de datos ChromaDB...")
    bloque_pdfs = loaderPDF.load_bloque()
    print(f"Embedding de {len(bloque_pdfs)} PDFs...")
    for pdf in tqdm(bloque_pdfs):
        vectorBD.add_documento(pdf)

    


if __name__ == "__main__":
    cabecera()
   # main()
