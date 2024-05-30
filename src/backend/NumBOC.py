import mysql.connector

import re

def insert_numero(numeroBOC):
    if(numeroBOC==0):
        return False
    try:
        # Conectar a la base de datos MySQL
        connection = mysql.connector.connect(
            host='10.0.72.132',   # Cambia esto por la dirección de tu contenedor docker si es diferente
            user='root',  # Cambia esto por tu usuario de MySQL
            password='test_pass',  # Cambia esto por tu contraseña de MySQL
            database='ChatBOC'
        )
        
        cursor = connection.cursor()
        
     
        query = f"INSERT INTO NumBOC(NumeroBOC) VALUES ({numeroBOC})"
                       
        
        
        cursor.execute(query)
        
       
        connection.commit()
        if cursor.rowcount == 1:
                cursor.close()
                connection.close()
                return True
        else:
                return False
        
        

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    

def get_ultimo_numero():
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
        query = "SELECT NumeroBOC FROM NumBOC ORDER BY IdNum DESC LIMIT 1;"
        cursor.execute(query)
        
        # Si se encuentra al menos un resultado, las credenciales son correctas
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        return result is not None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return -2
    
def numero_existe(numero):
    if(numero<0):
        return False
    try:
        # Conectar a la base de datos MySQL
        connection = mysql.connector.connect(
            host='10.0.72.132',   # Cambia esto por la dirección de tu contenedor docker si es diferente
            user='root',  # Cambia esto por tu usuario de MySQL
            password='test_pass',  # Cambia esto por tu contraseña de MySQL
            database='ChatBOC'
        )
        
        cursor = connection.cursor()
        
        
        query = "SELECT NumeroBOC FROM NumBOC where NumeroBOC = %s LIMIT 1"
        cursor.execute(query,(numero,))
        
   
    
        # Obtener el resultado de la consulta
        result = cursor.fetchone()
   
        cursor.close()
        connection.close()
        return result is not None
        
       

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return -2
print(insert_numero(2)) 
print(numero_existe(2))