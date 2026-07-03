import re
from entidad_base import EntidadBase
from excepciones import ClienteInvalidoError, DatosInvalidosError
from logger_config import logger


class Cliente(EntidadBase):
    _documentos_registrados = set()

    def __init__(self, nombre, documento, email, telefono):
        super().__init__()
        self.nombre = nombre
        self.documento = documento
        self.email = email
        self.telefono = telefono
        logger.info(f"Cliente creado correctamente -> ID {self.id} | {self.nombre}")

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ClienteInvalidoError("El nombre del cliente no puede estar vacío")
        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]{3,60}$", valor.strip()):
            raise ClienteInvalidoError(
                f"El nombre '{valor}' contiene caracteres no válidos"
            )
        self._nombre = valor.strip().title()

    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, valor):
        valor_str = str(valor).strip()
        if not valor_str.isdigit() or not (5 <= len(valor_str) <= 15):
            raise ClienteInvalidoError(
                f"El documento '{valor}' no es válido (debe ser numérico, 5-15 dígitos)"
            )
        if valor_str in Cliente._documentos_registrados:
            raise ClienteInvalidoError(
                f"Ya existe un cliente registrado con el documento {valor_str}"
            )
        Cliente._documentos_registrados.add(valor_str)
        self._documento = valor_str

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        patron = r"^[\w\.\-]+@[\w\-]+\.[a-zA-Z]{2,}$"
        if not isinstance(valor, str) or not re.match(patron, valor.strip()):
            raise DatosInvalidosError(f"El correo '{valor}' no tiene un formato válido")
        self._email = valor.strip().lower()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        valor_str = str(valor).strip()
        if not valor_str.isdigit() or not (7 <= len(valor_str) <= 10):
            raise DatosInvalidosError(
                f"El teléfono '{valor}' no es válido (debe tener 7-10 dígitos)"
            )
        self._telefono = valor_str

    def validar(self):
        campos_validos = all([
            isinstance(self._nombre, str) and self._nombre.strip(),
            self._documento.isdigit(),
            re.match(r"^[\w\.\-]+@[\w\-]+\.[a-zA-Z]{2,}$", self._email),
            self._telefono.isdigit(),
        ])
        if not campos_validos:
            raise ClienteInvalidoError(f"El cliente #{self.id} tiene datos inconsistentes")
        return True

    def describir(self):
        return (
            f"Cliente #{self.id} | {self.nombre} | Doc: {self.documento} "
            f"| Email: {self.email} | Tel: {self.telefono}"
        )
