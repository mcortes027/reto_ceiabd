from storage.ChromaVectorStore import ChromaVectorStore
from loadpdf.LoadPDF import LoadPDF
from colorama import Fore, Style
from tqdm import tqdm
import os

#------ CONTANTES PARA DESPLIEGUE EN PRODUCCIÓN ------
CHROMA_HOST = os.environ["CHROMA_HOST"] # "localhost" 
OLLAMA_HOST = os.environ["OLLAMA_HOST"] # "localhost"


def menu():
    print(Fore.RED + r" ____  ____  _____          __     __        _             ")
    print(Fore.RED + r"|  _ \|  _ \|  ___|   __ _  \ \   / /__  ___| |_ ___  _ __ ")
    print(Fore.RED + r"| |_) | | | | |_     / _` |  \ \ / / _ \/ __| __/ _ \| '__|")
    print(Fore.RED + r"|  __/| |_| |  _|   | (_| |   \ V /  __/ (__| || (_) | |   ")
    print(Fore.RED + r"|_|   |____/|_|      \__,_|    \_/ \___|\___|\__\___/|_|   ")
    print(Fore.MAGENTA + r"-----------------------------------------------------------")
    print(Fore.RED + "                                                   Equipo A ")
    print(Fore.GREEN + "1. Cargar los PDFs en la base de datos ChromaDB")
    print(Fore.GREEN + "2. Continuar donde se quedó la carga de los PDF")
    print(Fore.GREEN + "3. Salir")
    print(Style.RESET_ALL)
    opcion = input("Seleccione una opción: ")
    return opcion



def main():
    loaderPDF = LoadPDF(carpeta_pdf='../data', bloque_datos=1000)
    vectorBD = ChromaVectorStore(host=CHROMA_HOST, host_Ollama=OLLAMA_HOST)
    
    while True:
        opcion = menu()
        if opcion == "1":
            print("Cargando PDFs en la base de datos ChromaDB...")
            bloque_pdfs = loaderPDF.load_bloque()
            print(f"Embedding de {len(bloque_pdfs)} PDFs...")
            for pdf in tqdm(bloque_pdfs):
                vectorBD.add_documento(pdf)
           
        elif opcion == "2":
            print("continuando con la carga de PDFs...")
            bloque_pdfs = loaderPDF.load_bloque()
            print(f"Embedding de {len(bloque_pdfs)} PDFs...")
            for pdf in tqdm(bloque_pdfs):
                vectorBD.add_documento(pdf)
            
        elif opcion == "3":
            break
        else:
            print("Opción no válida.")
            continue
    print("¡Hasta luego!\b")

if __name__ == "__main__":
    main()
