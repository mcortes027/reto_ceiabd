# Este archivo contempla los distintos entornos en los que permitimos despliegues, para añadir un nuevlo entorno copie la templeta.
# Y edítela según necesite. 

# ENTORNO PARA DESPLIEGUE EN CLASE. 
#"volumen_mysql":r'C:\Users\JRBlanco\Dev\reto_server\mysql_data'


entornos ={
      'clase':{
            "volumen_chromadb":"/SSD1/home/ciabd12/volumenes_produccion/chromadb-data",
            "volumen_ollama":"/reto_ceiabda_produccion/ollama-data",
            "volumen_mysql":"/reto_ceiabda_produccion/mysql-data",
            "volumen_backups":"/reto_ceiabda_produccion/backups"
      },
      'joseramon':{
            "volumen_chromadb":'C:\\Users\\JRBlanco\\Dev\\reto_server\\chromadb-data',
            "volumen_ollama":'C:\\Users\\JRBlanco\\Dev\\reto_server\\ollama-data',
            "volumen_mysql":'C:\\Users\\JRBlanco\\Dev\\reto_server\\mysql_data',
            "volumen_backups":'C:\\Users\\JRBlanco\\Dev\\reto_server\\backups'
      },
      'manolo':{
            "volumen_chromadb":'C:\\Users\\m_cor\\Dev\\reto_server\\chromadb-data',
            "volumen_ollama":'C:\\Users\\m_cor\\Dev\\reto_server\\ollama-data',
            "volumen_mysql":'C:\\Users\\m_cor\\Dev\\reto_server\\mysql_data',
            "volumen_backups":'C:\\Users\\m_cor\\Dev\\reto_server\\backups'
      }         
} 


