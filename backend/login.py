import mysql.connector

def check_login(username, password):
    try:
        # Conectar a la base de datos MySQL
        connection = mysql.connector.connect(
            host='localhost',   # Cambia esto por la dirección de tu contenedor docker si es diferente
            user='test',  # Cambia esto por tu usuario de MySQL
            password='test',  # Cambia esto por tu contraseña de MySQL
            database='ChatBOC'
        )
        
        cursor = connection.cursor()
        
        # Consulta para verificar las credenciales
        query = "SELECT * FROM usuarios WHERE user = %s AND pass = %s"
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

# Ejemplo de uso
username = input("Introduce tu usuario: ")
password = input("Introduce tu contraseña: ")

if check_login(username, password):
    print("Login correcto")
else:
    print("Usuario o contraseña incorrectos")