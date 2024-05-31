import mysql.connector
import logging
import re
import os

class Usuario():
        

        def __init__(self,id, username, password, email, direccion, localidad, telefono, uso, cp,edad):
            self._inicia_logs()
            self.id=id
            self.username = username
            self.password = password
            self.email = email
            self.direccion = direccion
            self.localidad = localidad
            self.telefono = telefono
            self.cp = cp
            self.uso = uso
            self.edad=edad
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

        def __str__(self):
                return (f"Usuario(username={self.username}, email={self.email}, "
                        f"direccion={self.direccion}, localidad={self.localidad}, "
                        f"telefono={self.telefono}, CP={self.cp}, uso={self.uso}), edad={self.edad}")

        def get_localidad(self):
                return self.localidad
        def get_uso(self):
                return self.uso
        def get_edad(self):
                return self.edad
        def get_cp(self):
                return self.cp
        def check_login(self,email, password):
        #En función del resultado, devolverá un número
        #Si devuelve 2, el usuario requerido no existe
        #Si devuelve 1, la contraseña es incorrecta
        #Si devuelve 0, el login es correcto.  
                try:
                        # Conectar a la base de datos MySQL
                        connection=self._connect()
                        cursor = connection.cursor()
                        query = "SELECT * FROM usuarios WHERE email = %s"
                        
                        cursor.execute(query,(email,))
                        if cursor.fetchone() is False:
                                self.logger.info("Error de login: usuario inexistente")
                                return 2      
                        # Consulta para verificar las credenciales
                        query = "SELECT * FROM usuarios WHERE email = %s AND password = %s"
                        cursor.execute(query, (email, password))
                        # Si se encuentra al menos un resultado, las credenciales son correctas
                        result = cursor.fetchone() 
                        # cursor.close()
                        # connection.close()    
                        if result:
                                self.logger.info("Login correcto")
                                return 0
                        else:
                                self.logger.info("Error de login: contraseña incorrecta")
                                return 1
                except mysql.connector.Error as err:
                        self.logger.error(f"Error: {err}")
                        return False
        
        def registrar_usuario(self,username, password, email, direccion, localidad, telefono, cp, uso):

                try:
                        # Conectar a la base de datos MySQL
                        connection=self._connect()
                        cursor = connection.cursor()
                        query = """INSERT INTO usuarios (username, password, email, direccion, localidad, telefono, cp, uso)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                        valores = (username, password, email, direccion, localidad, telefono, cp, uso)
                        cursor.execute(query, valores)
                        connection.commit()
                        if cursor.rowcount == 1:
                                # cursor.close()
                                # connection.close()
                                return True
                        # cursor.close()
                        # connection.close() 
                except mysql.connector.Error as err:
                        self.logger.error(f"Error: {err}")
                        return False
                
        def get_usuario(self,email):
                try:
                        # Conectar a la base de datos MySQL
                        connection=self._connect()
                        cursor = connection.cursor()
                        query = "SELECT * FROM usuarios WHERE email =%s"
                        cursor.execute(query,(email,))
                        # Si se encuentra al menos un resultado, las credenciales son correctas
                        result = cursor.fetchone()
                        cursor.close()
                        connection.close()
                        if result:
                                print(result)
                                return Usuario(*result)
                        else:
                                return None
                except mysql.connector.Error as err:
                        self.logger.error(f"Error: {err}")
                        
                        return False
                
        def _inicia_logs(self):
                """
                Inicializa los registros de log.

                Crea un directorio de registros llamado "Log_System" si no existe.
                Configura el registro de eventos en un archivo llamado "chroma.log" dentro del directorio de registros.
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