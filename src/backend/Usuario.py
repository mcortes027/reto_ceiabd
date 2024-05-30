
class Usuario():
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
      self.edad = edad

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
