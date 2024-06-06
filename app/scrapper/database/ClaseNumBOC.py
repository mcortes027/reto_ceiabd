import mysql.connector
import logging, os

class ClaseNumBOC:
    
    
    def __init__(self, host='localhost', user='root', password='test_pass', database='ChatBOC'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = self._connect()
        self.cursor = self.connection.cursor()
        self._inicia_logs()

    def _connect(self):
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return connection
        except mysql.connector.Error as err:
            self.logger.error(f"Error de conexión: {err}")
            raise

    def insert_numero(self, numeroBOC):
        if numeroBOC == 0:
            return False
        if self.is_numero_existe(numeroBOC):
            return False
        try:
            query = "INSERT INTO NumBOC(NumeroBOC) VALUES (%s)"
            self.cursor.execute(query, (numeroBOC,))
            self.connection.commit()
            return self.cursor.rowcount == 1
        except mysql.connector.Error as err:
            self.logger.error(f"Error: {err}")
            return False

    def get_ultimo_numero(self):
        try:
            query = "SELECT NumeroBOC FROM NumBOC ORDER BY IdNum DESC LIMIT 1;"
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result if result else -1
        except mysql.connector.Error as err:
            self.logger.error(f"Error: {err}")            
            return -2

    def is_numero_existe(self, numero):
        if numero < 0:
            return False
        try:
            query = "SELECT 1 FROM NumBOC WHERE NumeroBOC = %s LIMIT 1"
            self.cursor.execute(query, (numero,))
            result = self.cursor.fetchone()
            return result is not None
        except mysql.connector.Error as err:
            self.logger.error(f"Error: {err}")
            return -2

    def close(self):
        self.cursor.close()
        self.connection.close()

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

# #Ejemplo de uso
# if __name__ == "__main__":

#     clase_numboc = ClaseNumBOC()

#     print(clase_numboc.insert_numero(12345))

#     print(clase_numboc.get_ultimo_numero())

#     print(clase_numboc.numero_existe(12345))

#     clase_numboc.close()
