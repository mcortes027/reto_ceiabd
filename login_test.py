import login
import usuario

# login.registrar_usuario(
#     username="juanperez",
#     password="password123",
#     email="juanperez@example.com",
#     direccion="Calle Falsa 123",
#     localidad="Springfield",
#     telefono="555-1234",
#     cp="12345",
#     uso="personal"
# )

if login.check_login('juanperez','password123'):
    print('Login correcto')
else:
    print('login incorrecto')
