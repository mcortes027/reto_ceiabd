import mysql.connector

import re
import usuario as usuario
def check_login(username, password):
    try:
        # Conectar a la base de datos MySQL
        connection = mysql.connector.connect(
            host='10.0.72.132',   # Cambia esto por la dirección de tu contenedor docker si es diferente
            user='root',  # Cambia esto por tu usuario de MySQL
            password='test_pass',  # Cambia esto por tu contraseña de MySQL
            database='ChatBOC'
        )
        
        cursor = connection.cursor()
        
        # Consulta para verificar las credenciales
        query = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        
        # Si se encuentra al menos un resultado, las credenciales son correctas
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if result:
            return True
        else:
            return False

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    
def registrar_usuario(username, password, email, direccion, localidad, telefono, cp, uso):
    # Validar la contraseña
    if len(password) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres.")
    if not re.search(r"[A-Za-z]", password) or not re.search(r"[0-9]", password):
        raise ValueError("La contraseña debe contener al menos letras y números.")
    
    # Validar el email
    if "@" not in email or email != email.lower():
        raise ValueError("El email debe contener el carácter '@' y estar en minúsculas.")

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
                print("Usuario insertado correctamente en la base de datos.")
        else:
                print("Error al insertar usuario.")

        
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

