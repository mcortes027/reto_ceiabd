import mysql.connector

import re
import Usuario


def check_login(email, password):
    #En función del resultado, devolverá un número
    #Si devuelve 2, el usuario requerido no existe
    #Si devuelve 1, la contraseña es incorrecta
    #Si devuelve 0, el login es correcto. 
    
    
    try:
        # Conectar a la base de datos MySQL
        connection = mysql.connector.connect(
            host='10.0.72.132',   # Cambia esto por la dirección de tu contenedor docker si es diferente
            user='root',  # Cambia esto por tu usuario de MySQL
            password='test_pass',  # Cambia esto por tu contraseña de MySQL
            database='ChatBOC'
        )
       
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
        
        cursor.close()
        connection.close()
        
        if result:
            return 0
        else:
            return 1

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    
def registrar_usuario(username, password, email, direccion, localidad, telefono, cp, uso):
    # Validar la contraseña
    # if len(password) < 8:
    #     raise ValueError("La contraseña debe tener al menos 8 caracteres.")
    # if not re.search(r"[A-Za-z]", password) or not re.search(r"[0-9]", password):
    #     raise ValueError("La contraseña debe contener al menos letras y números.")
    
    # Validar el email
    # if "@" not in email or email != email.lower():
    #     raise ValueError("El email debe contener el carácter '@' y estar en minúsculas.")

    # Crear el objeto Usuario
    # usuario = usuario.usuario(username, password, email, direccion, localidad, telefono, cp, uso)
    try:
        # Conectar a la base de datos MySQL
        connection = mysql.connector.connect(
            host='10.0.72.132',   # Cambia esto por la dirección de tu contenedor docker si es diferente
            user='root',  # Cambia esto por tu usuario de MySQL
            password='test_pass',  # Cambia esto por tu contraseña de MySQL
            database='ChatBOC'
        )
        
        cursor = connection.cursor()
        
     
        query = """INSERT INTO usuarios (username, password, email, direccion, localidad, telefono, cp, uso)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        valores = (username, password, email, direccion, localidad, telefono, cp, uso)
        
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
def get_usuario(email):
    try:
        # Conectar a la base de datos MySQL
        connection = mysql.connector.connect(
            host='10.0.72.132',   # Cambia esto por la dirección de tu contenedor docker si es diferente
            user='root',  # Cambia esto por tu usuario de MySQL
            password='test_pass',  # Cambia esto por tu contraseña de MySQL
            database='ChatBOC'
        )
        
        cursor = connection.cursor()
        
     
        query = "SELECT * FROM usuarios WHERE email =%s"
        
        
        cursor.execute(query,(email,))
        
        # Si se encuentra al menos un resultado, las credenciales son correctas
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if result:
            return Usuario.usuario(*result)
        else:
            return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

# user=get_usuario("test@test.com")
# print(user.email)