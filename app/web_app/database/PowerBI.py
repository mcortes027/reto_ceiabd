import csv, os, sys, mysql.connector
import time, requests, logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from Usuario import DaoUser, Usuario
from datetime import datetime

class PowerBI:
    
    def __init__(self, host, user, password):
        self._inicia_logs()
        self.host = host
        self.user = user
        self.password = password
        #------ Atributos de la clase PowerBI -----
        self.fecha = None
        self.hora = None
        self.latitud = None
        self.longitud = None
        self.pregunta = None
        self.uso_usuario = None
        self.localidad_usuario = None
        self.cp_usuario = None
        self.edad_usuario = None
    
    def config(self, fecha, hora, latitud, longitud, pregunta, uso_usuario, localidad_usuario, cp_usuario, edad_usuario):
        """
        Configura los parámetros de la instancia de la clase PowerBI.

        Args:
            fecha (str): La fecha de configuración.
            hora (str): La hora de configuración.
            latitud (float): La latitud de configuración.
            longitud (float): La longitud de configuración.
            pregunta (str): La pregunta de configuración.
            uso_usuario (str): El uso del usuario de configuración.
            localidad_usuario (str): La localidad del usuario de configuración.
            cp_usuario (str): El código postal del usuario de configuración.
            edad_usuario (int): La edad del usuario de configuración.
        """
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
                host=self.host,
                user=self.user,
                password=self.password,
                database='ChatBOC'
            )
            return connection
        except mysql.connector.Error as err:
                self.logger.error(f"Error de conexión: {err}")
                raise

    def _location(self):
        """
        Obtiene la ubicación del usuario utilizando la API de ip-api.com.

        Returns:
            Tuple[float, float]: Una tupla con las coordenadas de latitud y longitud de la ubicación del usuario.
            Si no se puede obtener la ubicación, se devuelve (None, None).
        """
        try:
            response = requests.get('http://ip-api.com/json/')
            data = response.json()
            if data['status'] == 'success':
                return data['lat'], data['lon']
            else:
                self.logger.warning("No se pudo obtener la ubicación del usuario.")
                return None, None
        except Exception as e:
            self.logger.error(f"Error al obtener la ubicación: {e}")
            return None, None

    def to_csv(self):    
        """
        Genera un archivo CSV con los datos de la tabla powerbi.

        Returns:
            bool: True si el archivo CSV se generó correctamente, False en caso contrario.
        """
        fecha = datetime.now().date()
        csv_filename = f"../../{fecha}.csv"     
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM powerbi ORDER BY id")
                rows = cursor.fetchall()

                with open(csv_filename, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['id', 'fecha', 'hora', 'latitud', 'longitud', 'pregunta', 'uso_usuario', 'localidad_usuario', 'cp_usuario', 'edad_usuario'])
                    writer.writerows(rows)
                
                self.logger.info("CSV generado correctamente.")
                return True
            
        except (mysql.connector.Error, Exception) as e:
            self.logger.error(f"Error al generar el archivo CSV: {e}")
            return False

    def save_datos(self):
        """
        Guarda los datos en la tabla powerbi de la base de datos.

        Returns:
            bool: True si los datos se insertaron correctamente, False en caso contrario.
        """
        try:
            with self._connect() as connection:
                cursor = connection.cursor()
                query = """INSERT INTO powerbi 
                            (fecha, hora, latitud, longitud, pregunta, uso_usuario, localidad_usuario, cp_usuario, edad_usuario)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                valores = (self.fecha, self.hora, self.latitud, self.longitud, self.pregunta, self.cp_usuario, self.localidad_usuario, self.uso_usuario, self.edad_usuario)
                cursor.execute(query, valores)
                connection.commit()

                if cursor.rowcount == 1:
                    self.logger.info("Datos insertados correctamente en la tabla powerbi.")
                    return True
                else:
                    self.logger.warning("No se pudieron insertar los datos en la tabla powerbi.")
                    return False
        except (mysql.connector.Error, Exception) as e:
            self.logger.error(f"Error durante la inserción de datos en powerbi: {e}")
            return False

        
       
    # Esta función guarda un nuevo registro en la base de datos. SOLO tienes que mandar la pregunta y el email en ese mismo orden.   
    def NuevoRegistro(self, pregunta, email):
        """
        Crea un nuevo registro en powerbi.

        Args:
            pregunta (str): La pregunta asociada al registro.
            email (str): El correo electrónico del usuario.

        Returns:
            bool: True si el registro se ha creado exitosamente, False en caso contrario.
        """
        daouser = DaoUser(host=self.host, user=self.user, password=self.password)
        usuario = daouser.get_usuario(email)
        
        if usuario:
            fecha = datetime.now().date()
            hora = time.strftime('%H:%M:%S', time.localtime())
            latitud, longitud = self._location()
            
            self.config(
                fecha=fecha, hora=hora, latitud=latitud, longitud=longitud, 
                pregunta=pregunta, uso_usuario=usuario.uso, localidad_usuario=usuario.localidad, 
                cp_usuario=usuario.cp, edad_usuario=usuario.edad
            )
            self.logger.info(f"Registro de POWERBI creado: {self}")
            return self.save_datos()
        else:
            self.logger.error(f"Usuario {email} no encontrado, no se puede crear el registro")
            return False
    
    
    def __str__(self):
        return (f"PowerBI(fecha={self.fecha}, hora={self.hora}, latitud={self.latitud}, "
                f"longitud={self.longitud}, pregunta={self.pregunta}, uso_usuario={self.uso_usuario}, "
                f"localidad_usuario={self.localidad_usuario}, cp_usuario={self.cp_usuario}, edad_usuario={self.edad_usuario})")


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
        

# Ejemplo de uso:
# if __name__ == '__main__':
#     powerbi = PowerBI(host='localhost', user='root', password='test_pass')
#     powerbi.NuevoRegistro("¿Qué es Linux?", "juan69@gmail.com")
    
#     powerbi.to_csv()   # Genera un archivo CSV con los datos de la tabla powerbi.
