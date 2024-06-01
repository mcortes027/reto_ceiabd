import csv
import os
import mysql.connector
import time
import datetime
import Usuario
import requests
import logging

class PowerBI:
    
    def __init__(self, fecha=None, hora=None, latitud=None, longitud=None, pregunta=None, uso_usuario=None, localidad_usuario=None, cp_usuario=None, edad_usuario=None):
        self._inicia_logs()
        self.fecha = fecha
        self.hora = hora
        self.latitud = latitud
        self.longitud = longitud
        self.pregunta = pregunta
        self.uso_usuario = uso_usuario
        self.localidad_usuario = localidad_usuario
        self.cp_usuario = cp_usuario
        self.edad_usuario = edad_usuario

    def _connect(self):
        try:
            connection = mysql.connector.connect(
                    host=os.environ['MYSQL_HOST'],
                    user=os.environ['MYSQL_USER'],
                    password=os.environ['MYSQL_PASS'],
                    database='ChatBOC'
            )
            return connection
        except mysql.connector.Error as err:
                self.logger.error(f"Error de conexión: {err}")
                raise

    def get_location(self):
        try:
            response = requests.get('http://ip-api.com/json/')
            data = response.json()
            if data['status'] == 'success':
                latitude = data['lat']
                longitude = data['lon']
                return latitude, longitude
            else:
                return None, None
        except Exception as e:
            
            return None, None

    def set_fecha(self, fecha):
        self.fecha = fecha

    def get_fecha(self):
        return self.fecha

    def set_hora(self, hora):
        self.hora = hora

    def get_hora(self):
        return self.hora

    def set_latitud(self, latitud):
        self.latitud = latitud

    def get_latitud(self):
        return self.latitud

    def set_longitud(self, longitud):
        self.longitud = longitud

    def get_longitud(self):
        return self.longitud

    def set_pregunta(self, pregunta):
        self.pregunta = pregunta

    def get_pregunta(self):
        return self.pregunta

    def set_uso_usuario(self, uso_usuario):
        self.uso_usuario = uso_usuario

    def get_uso_usuario(self):
        return self.uso_usuario

    def set_localidad_usuario(self, localidad_usuario):
        self.localidad_usuario = localidad_usuario

    def get_localidad_usuario(self):
        return self.localidad_usuario

    def set_cp_usuario(self, cp_usuario):
        self.cp_usuario = cp_usuario

    def get_cp_usuario(self):
        return self.cp_usuario

    def set_edad_usuario(self, edad_usuario):
        self.edad_usuario = edad_usuario

    def get_edad_usuario(self):
        return self.edad_usuario

    def __str__(self):
        return f"PowerBI(fecha={self.fecha}, hora={self.hora}, latitud={self.latitud}, longitud={self.longitud}, pregunta={self.pregunta}, uso_usuario={self.uso_usuario}, localidad_usuario={self.localidad_usuario}, cp_usuario={self.cp_usuario}, edad_usuario={self.edad_usuario})"

    
    def generar_csv(self):
        
        fecha = datetime.now().date()
        
        csv_filename="../../"+fecha.__str__()+".csv"
        # Conectar a la base de datos MySQL
        conn=self._connect()
        cursor = conn.cursor()
        
        # Ejecutar la consulta para obtener los datos
        cursor.execute("SELECT * FROM powerbi ORDER BY id")
        rows = cursor.fetchall()
        
        # Escribir los datos en el archivo CSV
        with open(csv_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Escribir encabezados
            writer.writerow(['id', 'fecha', 'hora', 'latitud', 'longitud', 'pregunta', 'uso_usuario', 'localidad_usuario', 'cp_usuario', 'edad_usuario'])
            # Escribir las filas
            writer.writerows(rows)
        self.logger.info("CSV generado correctamente")
        # Cerrar la conexión a la base de datos
        cursor.close()
        

    
    def añadir_a_bd(self):
        try:
            # Conectar a la base de datos MySQL
            connection = self._connect()
            
            cursor = connection.cursor()
            
        
            query = """INSERT INTO powerbi 
                        VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            #No sé por qué, pero REQUIERE que le mandes un id a pesar de ser autoincrement. Sin embargo, al enviarlo, el autoincrement aplica el id correcto sin problemas, así que así va 
            valores = (0,self.fecha, self.hora, self.latitud,self.longitud ,self.pregunta , self.cp_usuario,self.localidad_usuario,self.uso_usuario, self.edad_usuario )
            
            cursor.execute(query, valores)
            
        
            connection.commit()
            if cursor.rowcount == 1:
                cursor.close()
                
                return True
            
            
            cursor.close()
            
        except mysql.connector.Error as err:
            self.logger.error(f"Error: {err}")
            return False
        
       
    # Esta función guarda un nuevo registro en la base de datos. SOLO tienes que mandar la pregunta y el mail en ese mismo orden
    
    def NuevoRegistro(self,pregunta, email):
       
       #Sacamos el usuario entero usando el email
        print("Email: ",email)
        usuario=Usuario.Usuario.get_usuario(self=self,email=email)
        
       
       
        fecha=datetime.date.today()
        hora=time.localtime()
        hora_formateada = time.strftime('%H:%M:%S', hora)
        latitud,longitud=self.get_location()
        edad=usuario.get_edad()
        uso=usuario.get_uso()
        localidad=usuario.get_localidad()
        cp=usuario.get_cp()
        
        registro=PowerBI(fecha=fecha,hora=hora_formateada,latitud=latitud,longitud=longitud,pregunta=pregunta,uso_usuario=uso,localidad_usuario=localidad,cp_usuario=cp,edad_usuario=edad)
        self.logger.info("Registro de POWERBI creado: ",registro.__str__())
        registro.añadir_a_bd()
        return True

    def _inicia_logs(self):
        """
        Inicializa los registros de log.

        Crea un directorio de registros llamado "Log_System" si no existe.
        Configura el registro de eventos en un archivo llamado "system.log" dentro del directorio de registros.
        Establece el nivel de registro en INFO.
        Utiliza el formato de registro: '%(asctime)s %(levelname)s %(name)s %(message)s'.
        Utiliza el formato de fecha: '%m/%d/%Y %I:%M:%S %p'.
        """
        log_dir = "Log_System"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logging.basicConfig(filename=os.path.join(log_dir, 'system.log'), 
                            level=logging.INFO, 
                            format='%(asctime)s %(levelname)s %(name)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
        
        self.logger = logging.getLogger(__name__)
        
#PowerBI.NuevoRegistro("preguntatest","test@test.com")