import mysql.connector
import logging
import os


class Usuario:
    def __init__(self,id, username, password, email, direccion, localidad, telefono, uso, cp,edad):
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
    
    def __str__(self):
        return (f"Usuario(username={self.username}, email={self.email}, "
                f"direccion={self.direccion}, localidad={self.localidad}, "
                f"telefono={self.telefono}, CP={self.cp}, uso={self.uso}), edad={self.edad})")

class DaoUser:
    
    def __init__(self, host, user, password):
        self._inicia_logs()
        self.host=host
        self.user=user
        self.password=password    
    
    def _connect(self):
        """
        Establece una conexión con la base de datos.

        Returns:
            connection (mysql.connector.connection.MySQLConnection): Objeto de conexión a la base de datos.

        Raises:
            mysql.connector.Error: Si ocurre un error al intentar establecer la conexión.
        """
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database='ChatBOC'
            )
            self.logger.info("Conexión exitosa a la base de datos.")
            return connection
        except mysql.connector.Error as err:
            self.logger.error(f"Error de conexión: {err}")
            raise
        
    def check_login(self, email, password):
        """
        Verifica las credenciales del usuario.
        
        Returns:
            False si el usuario o la contraseña es incorrecta.
            True si el login es correcto.
        """  
        try:
            # Conectar a la base de datos MySQL
            with self._connect() as connection:
                cursor = connection.cursor()
                query = "SELECT password FROM usuarios WHERE email = %s"
                cursor.execute(query,(email,))
                user = cursor.fetchone()
                
                if user is None or password != user[0]:
                    self.logger.info("Error de login: usuario inexistente o contraseña incorrecta.")
                    return False
                
                self.logger.info("Login correcto.")
                return True              

        except (mysql.connector.Error, Exception) as e:
            self.logger.error(f"Error de conexión a la base de datos o inesperado: {e}")
            return False
        
    def registrar_usuario(self, usuario: Usuario):
        """
        Registra un nuevo usuario en la base de datos.

        Args:
            usuario (Usuario): Una instancia de la clase Usuario.

        Returns:
            bool: True si el registro fue exitoso, False en caso contrario.
        """
        try:
            with self._connect() as connection:
                cursor = connection.cursor()
                query = """INSERT INTO usuarios (username, password, email, direccion, localidad, telefono, cp, uso, edad)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                valores = (usuario.username, usuario.password, usuario.email, usuario.direccion, usuario.localidad, usuario.telefono, usuario.cp, usuario.uso, usuario.edad)
                cursor.execute(query, valores)
                connection.commit()
                
                if cursor.rowcount == 1:
                        self.logger.info("Usuario registrado exitosamente.")
                        return True
                else:
                    self.logger.warning("El usuario no pudo ser registrado.")
                    return False
        
        except (mysql.connector.Error, Exception) as e:
            self.logger.error(f"Error durante el registro del usuario: {e}")
            return False
    
    def get_usuario(self,email):
        """
        Obtiene un usuario de la base de datos por su email.

        Args:
            email (str): El correo electrónico del usuario.

        Returns:
            Usuario: Una instancia de la clase Usuario si el usuario es encontrado.
            None: Si no se encuentra el usuario.
            False: Si ocurre un error durante la operación.
        """
        try:
            with self._connect() as connection:
                cursor = connection.cursor()
                query = "SELECT * FROM usuarios WHERE email = %s"
                cursor.execute(query, (email,))
                result = cursor.fetchone()

                if result:
                    self.logger.info(f"Usuario encontrado: {email}")
                    return Usuario(*result)
                else:
                    self.logger.info(f"Usuario no encontrado: {email}")
                    return None
                
        except (mysql.connector.Error, Exception) as e:
            self.logger.error(f"Error durante la obtención del usuario: {e}")
            return False
    
    def _inicia_logs(self):
        """
        Inicializa los registros de log.
        
        """
        log_dir = "Log_System"
        if not os.path.exists(log_dir):
                os.makedirs(log_dir)

        logging.basicConfig(
            filename=os.path.join(log_dir, 'system.log'), 
            level=logging.INFO, 
            format='%(asctime)s %(levelname)s %(name)s %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p'
        )
        
        self.logger = logging.getLogger(__name__)
  
# Ejemplo de uso:      
# if __name__ == "__main__":
    
#     dao = DaoUser(host='localhost', user='root', password='test_pass') # Crear objeto DaoUser.
    
#     usuario = Usuario(
#         id=1, 
#         username='test', 
#         password='test', 
#         email= 'juan@gmail.com', 
#         direccion='calle 123', 
#         localidad='CDMX', 
#         telefono='1234567890', 
#         uso='personal', 
#         cp='12345', 
#         edad=25
#     )
#     print("Añadido: ", usuario)
    
#     dao.registrar_usuario(usuario) # Guardar el usuario en la base de datos.
    
#     usuario_recuperado = dao.get_usuario('juan@gmail.com')
#     print("Recuperado: ", usuario_recuperado)
    
#     login = dao.check_login('juan69@gmail.com', 'test')
#     print("Login: ", login)
       