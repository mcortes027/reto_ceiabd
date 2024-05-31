from scrappers.Scrapper import ScrapperBOC
from colorama import Fore, Style

ULTIMO_DOCUMENTO = 500000

def menu():
    print(Fore.RED + r" ____                                       ____   ___   ____ ")
    print(Fore.RED + r"/ ___|  ___ _ __ __ _ _ __  _ __   ___ _ __| __ ) / _ \ / ___|")
    print(Fore.RED + r"\___ \ / __| '__/ _` | '_ \| '_ \ / _ \ '__|  _ \| | | | |    ")
    print(Fore.RED + r" ___) | (__| | | (_| | |_) | |_) |  __/ |  | |_) | |_| | |___ ")
    print(Fore.RED + r"|____/ \___|_|  \__,_| .__/| .__/ \___|_|  |____/ \___/ \____|")
    print(Fore.RED + r"                     |_|   |_|                                ")
  
    print(Fore.MAGENTA + r"---------------------------------------------------------------")
    print(Fore.RED + "                                                      Equipo A ")
    print(Fore.GREEN + "1. Descargar desde cero los documentos del BOC")
    print(Fore.GREEN + "2. Continuar descarga desde el último documento descargado")
    print(Fore.GREEN + "3. Salir")
    print(Style.RESET_ALL)
    opcion = input("Seleccione una opción: ")
    return opcion

def main():
    url_base_boc = "https://boc.cantabria.es/boces/verAnuncioAction.do?idAnuBlob="
    bocdown = ScrapperBOC(url_base_boc,procesos=20, carpeta='../data', start=1, end=ULTIMO_DOCUMENTO, paciencia=-12)
    
    while True:
        opcion = menu()
        if opcion == "1":
            bocdown.run()
            tiempo, unidad = bocdown.tiempo_de_descargar()
            print(f"Tiempo total: {tiempo} {unidad} y se han descargado {bocdown.last_download()} documentos.") 
        elif opcion == "2":
            bocdown.continua_download(bocdown.last_download())
            tiempo, unidad = bocdown.tiempo_de_descargar()
            print(f"Tiempo total: {tiempo} {unidad} y se han descargado {bocdown.last_download()} documentos.") 
        elif opcion == "3":
            break
        else:
            print("Opción no válida.")
            continue
    print("¡Hasta luego!\b")
    

if __name__ == "__main__":
    main()
    