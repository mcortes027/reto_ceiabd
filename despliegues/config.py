# Este archivo contempla los distintos entornos en los que permitimos despliegues, para añadir un nuevlo entorno copie la templeta.
# Y edítela según necesite. 

# ENTORNO PARA DESPLIEGUE EN CLASE. 
entornos ={
      'clase':{
            "volumen_chromadb":"/SSD1/home/ciabd12/volumenes_produccion/chromadb-data",
            "volumen_ollama":"/reto_ceiabda_produccion/ollama-data",
            "volumen_mysql":"/reto_ceiabda_produccion/mysql-data"
      },
      'joseramon':{
            "volumen_chromadb":'C:\Users\JRBlanco\Dev\reto_server\chromadb-data',
            "volumen_ollama":'C:\Users\JRBlanco\Dev\reto_server\ollama-data',
            "volumen_mysql":'C:\Users\JRBlanco\Dev\reto_server\mysql_data'
      }       
} 


