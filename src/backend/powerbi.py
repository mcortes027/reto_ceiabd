import csv
import os
import mysql.connector
import time
import datetime
import localizacion
import Usuario as user

class PowerBI:
    def __init__(self, fecha=None, hora=None, latitud=None, longitud=None, pregunta=None, uso_usuario=None, localidad_usuario=None, cp_usuario=None, edad_usuario=None):
       
        self.fecha = fecha
        self.hora = hora
        self.latitud = latitud
        self.longitud = longitud
        self.pregunta = pregunta
        self.uso_usuario = uso_usuario
        self.localidad_usuario = localidad_usuario
        self.cp_usuario = cp_usuario
        self.edad_usuario = edad_usuario

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

    @staticmethod
    def generar_csv():
        csv_filename=""
        # Conectar a la base de datos MySQL
        db_config = {
            'host': '10.0.72.132',
            'user': 'root',
            'password': 'test_pass',
            'database': 'ChatBOC'
        } 
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
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
        
        # Cerrar la conexión a la base de datos
        cursor.close()
        conn.close()

    @staticmethod
    def añadir_a_bd(pwb):
        try:
            # Conectar a la base de datos MySQL
            connection = mysql.connector.connect(
                host='10.0.72.132',   # Cambia esto por la dirección de tu contenedor docker si es diferente
                user='root',  # Cambia esto por tu usuario de MySQL
                password='test_pass',  # Cambia esto por tu contraseña de MySQL
                database='ChatBOC'
            )
            
            cursor = connection.cursor()
            
        
            query = """INSERT INTO powerbi 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            valores = (pwb.fecha, pwb.hora, pwb.latitud,pwb.longitud ,pwb.preguntas ,pwb.uso_usuario ,pwb.Localidad_usuario, pwb.cp_usuario, pwb.edad_usuario )
            
            cursor.execute(query, valores)
            
        
            connection.commit()
            if cursor.rowcount == 1:
                cursor.close()
                connection.close()
                return True
            
            
            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        
       
    #Esta función guarda un nuevo registro en la base de datos. SOLO tienes que mandar la pregunta y el mail en ese mismo orden
    @staticmethod
    def NuevoRegistro(pregunta, email):
       
       #Sacamos el usuario entero usando el email
        usuario=user.get_usuario(email)
       
       
        fecha=datetime.date.today()
        hora=time.localtime()
        hora_formateada = time.strftime('%H:%M:%S', hora)
        latitud,longitud=localizacion.get_location()
        edad=user.get_edad(usuario)
        uso=user.get_uso(usuario)
        localidad=user.get_localidad(usuario)
        cp=user.get_cp(usuario)
        
        registro=PowerBI(fecha=fecha,hora=hora_formateada,latitud=latitud,longitud=longitud,pregunta=pregunta,uso_usuario=uso,localidad_usuario=localidad,cp_usuario=cp,edad_usuario=edad)
        PowerBI.añadir_a_bd(registro)
        return True
