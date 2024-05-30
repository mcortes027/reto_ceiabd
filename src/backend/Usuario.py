import mysql.connector

import re

class usuario():

        def __init__(self, id, username, password, email, direccion, localidad, telefono, uso, cp,edad):
            self.id= id
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
                                host='10.0.72.132',
                                user='root',
                                password='test_pass',
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

        def actualizar_direccion(self, nueva_direccion):
                self.direccion = nueva_direccion

        def actualizar_localidad(self, nueva_localidad):
                self.localidad = nueva_localidad

        def actualizar_telefono(self, nuevo_telefono):
                self.telefono = nuevo_telefono

        def actualizar_email(self, nuevo_email):
                self.email = nuevo_email

        def cambiar_password(self, nueva_password):
                self.password = nueva_password

        def actualizar_uso(self, nuevo_uso):
                self.uso = nuevo_uso

        def get_localidad(usuario):
                return usuario.localidad
        def get_uso(usuario):
                return usuario.uso
        def get_edad(usuario):
                return usuario.edad
        def get_cp(usuario):
                return usuario.cp
        def check_login(self,email, password):
        #En función del resultado, devolverá un número
        #Si devuelve 2, el usuario requerido no existe
        #Si devuelve 1, la contraseña es incorrecta
        #Si devuelve 0, el login es correcto.  
                try:
                        # Conectar a la base de datos MySQL
                        connection=self._connect()
                        cursor = connection.cursor()
                        query = f"SELECT * FROM usuarios WHERE email = '{email}'"
                        
                        cursor.execute(query)
                        if cursor.fetchone() is False:
                                return 2      
                        # Consulta para verificar las credenciales
                        query = "SELECT * FROM usuarios WHERE email = %s AND password = %s"
                        cursor.execute(query, (email, password))
                        # Si se encuentra al menos un resultado, las credenciales son correctas
                        result = cursor.fetchone() 
                        # cursor.close()
                        # connection.close()    
                        if result:
                                return 0
                        else:
                                return 1
                except mysql.connector.Error as err:
                        print(f"Error: {err}")
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
                        print(f"Error: {err}")
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
                                return usuario(*result)
                        else:
                                return None
                except mysql.connector.Error as err:
                        print(f"Error: {err}")
                        return False