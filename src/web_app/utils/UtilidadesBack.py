import re

class UtilidadesBack:
  """
  Clase con utilidades para implementar en el backend de la UI.

  Methods:
    validar_email(email): Verifica si una dirección de correo electrónico es válida.
    validar_password(password, min_caracteres, max_caracteres): Verifica si una contraseña es válida.
    validar_codigo_postal(codigo_postal): Verifica si un código postal es válido.

  """  

  def validar_email(email):
    """
    Este método valida si la cadena proporcionada es una dirección de correo electrónico válida.

    Args:
      correo (str): La cadena de dirección de correo electrónico que se va a validar.

    Returns:
      bool: True si la dirección de correo electrónico es válida, False en caso contrario.
    """
    # Expresión regular para validar el formato de correo electrónico.
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    # Evaluar si el correo elecrónico cumple la expresión regular:
    if re.match(regex, email):
      return True
    else:
      return False

  def validar_password(password, min_caracteres, max_caracteres):
    """
    Este método determina si una contraseña es válida según los criterios especificados posteriormente.

    Args:
      password (str): La contraseña a validar.
      min_caracteres (int): Longitud mínima permitida para la contraseña.
      max_caracteres (int): Longitud máxima permitida para la contraseña.

    Returns:
      list: Una lista con dos elementos:
        - [0] bool: True si la contraseña es válida, False en caso contrario.
        - [1] str: Mensaje de error si la contraseña no es válida.
    """  
    # Declarar variable para el texto del error:
    mensaje_error = ""
    
    # Definir los distintos criterios de validación:
    if len(password) < min_caracteres:
      mensaje_error = f'La contraseña no cumple con la longitud mínima, debe ser mayor de {min_caracteres-1} carácteres.'
      return [False, mensaje_error]
    else:
      if len(password) > max_caracteres:
        mensaje_error = f'La contraseña excede la longitud máxima, debe ser menor de {max_caracteres+1} carácteres y mayor de {min_caracteres-1} carácteres.'
        return [False, mensaje_error]
      else:
        # Expresión regular para validar el formato de la contraseña:
        regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)'

        # Evaluar si la contraseña no cumple la expresión regular:
        if not re.match(regex, password):
          mensaje_error = f'La contraseña debe contener varias letras, al menos una letra mayúscula y un número.'
          return [False, mensaje_error]
        else:
          return [True, mensaje_error]
        
  def validar_codigo_postal(codigo_postal):
    """
    Este método determina si un código postal es válido para España.

    Args:
      codigo_postal (str): El código postal que se desea validar. Sus dos primeros dígitos deben estar entre 01 y 52, los tres últimos dígitos entre 0 y 9.

    Returns:
      bool: True si el código postal es válido, False en caso contrario.
    """
    # Expresión regular para validar el formato del código postal:
    regex = r'^(0[1-9]|[1-4][0-9]|5[0-2])[0-9]{3}$'

    return re.search(regex, codigo_postal) is not None
