from abc import abstractmethod
from entidad_base import EntidadBase
from excepciones import ServicioInvalidoError, CalculoInconsistenteError
from logger_config import logger


class Servicio(EntidadBase):
    def __init__(self, nombre, precio_base, disponible=True):
        super().__init__()
        self.nombre = nombre
        self.precio_base = precio_base
        self._disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ServicioInvalidoError("El nombre del servicio no puede estar vacío")
        self._nombre = valor.strip()

    @property
    def precio_base(self):
        return self._precio_base

    @precio_base.setter
    def precio_base(self, valor):
        try:
            valor_num = float(valor)
        except (TypeError, ValueError) as err:
            raise ServicioInvalidoError(
                f"El precio base '{valor}' no es un número válido"
            ) from err
        if valor_num <= 0:
            raise ServicioInvalidoError("El precio base debe ser mayor que cero")
        self._precio_base = valor_num

    @property
    def disponible(self):
        return self._disponible

    def marcar_no_disponible(self):
        self._disponible = False
        logger.info(f"Servicio '{self.nombre}' (#{self.id}) marcado como NO disponible")

    def calcular_costo(self, impuesto=0.0, descuento=0.0, **kwargs):
        if impuesto < 0 or descuento < 0:
            raise CalculoInconsistenteError(
                "Impuesto y descuento no pueden ser valores negativos"
            )
        if descuento > 100:
            raise CalculoInconsistenteError("El descuento no puede superar el 100%")

        subtotal = self.precio_base
        subtotal -= subtotal * (descuento / 100)
        subtotal += subtotal * (impuesto / 100)

        if subtotal < 0:
            raise CalculoInconsistenteError(
                f"El cálculo de costo del servicio '{self.nombre}' resultó negativo"
            )
        return round(subtotal, 2)

    @abstractmethod
    def describir(self):
        raise NotImplementedError

    @abstractmethod
    def validar(self):
        raise NotImplementedError


class ReservaSala(Servicio):
    def __init__(self, nombre, precio_base, capacidad, horas=1, disponible=True):
        super().__init__(nombre, precio_base, disponible)
        self.capacidad = capacidad
        self.horas = horas

    @property
    def capacidad(self):
        return self._capacidad

    @capacidad.setter
    def capacidad(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ServicioInvalidoError("La capacidad de la sala debe ser un entero positivo")
        self._capacidad = valor

    @property
    def horas(self):
        return self._horas

    @horas.setter
    def horas(self, valor):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ServicioInvalidoError("Las horas de reserva deben ser un número positivo")
        self._horas = valor

    def calcular_costo(self, impuesto=0.0, descuento=0.0, **kwargs):
        base = super().calcular_costo(impuesto=0.0, descuento=0.0)
        total = base * self.horas
        total -= total * (descuento / 100)
        total += total * (impuesto / 100)
        if total < 0:
            raise CalculoInconsistenteError("Costo inconsistente en ReservaSala")
        return round(total, 2)

    def validar(self):
        if self._capacidad <= 0 or self._horas <= 0 or self._precio_base <= 0:
            raise ServicioInvalidoError(f"Sala '{self.nombre}' tiene datos inconsistentes")
        return True

    def describir(self):
        return (
            f"[Sala] #{self.id} {self.nombre} | Capacidad: {self.capacidad} pers. "
            f"| {self.horas}h | Precio base: ${self.precio_base:,.2f} "
            f"| Disponible: {self.disponible}"
        )


class AlquilerEquipo(Servicio):
    def __init__(self, nombre, precio_base, dias=1, disponible=True):
        super().__init__(nombre, precio_base, disponible)
        self.dias = dias

    @property
    def dias(self):
        return self._dias

    @dias.setter
    def dias(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ServicioInvalidoError("Los días de alquiler deben ser un entero positivo")
        self._dias = valor

    def calcular_costo(self, impuesto=0.0, descuento=0.0, **kwargs):
        base = super().calcular_costo(impuesto=0.0, descuento=0.0)
        total = base * self.dias
        if self.dias > 5:
            total *= 1.05
        total -= total * (descuento / 100)
        total += total * (impuesto / 100)
        if total < 0:
            raise CalculoInconsistenteError("Costo inconsistente en AlquilerEquipo")
        return round(total, 2)

    def validar(self):
        if self._dias <= 0 or self._precio_base <= 0:
            raise ServicioInvalidoError(f"Equipo '{self.nombre}' tiene datos inconsistentes")
        return True

    def describir(self):
        return (
            f"[Equipo] #{self.id} {self.nombre} | {self.dias} día(s) "
            f"| Precio base/día: ${self.precio_base:,.2f} | Disponible: {self.disponible}"
        )


class AsesoriaEspecializada(Servicio):
    def __init__(self, nombre, precio_base, horas, nivel_experto="junior", disponible=True):
        super().__init__(nombre, precio_base, disponible)
        self.horas = horas
        self.nivel_experto = nivel_experto

    @property
    def horas(self):
        return self._horas

    @horas.setter
    def horas(self, valor):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ServicioInvalidoError("Las horas de asesoría deben ser un número positivo")
        self._horas = valor

    @property
    def nivel_experto(self):
        return self._nivel_experto

    @nivel_experto.setter
    def nivel_experto(self, valor):
        niveles_validos = {"junior": 1.0, "senior": 1.3, "experto": 1.6}
        if valor not in niveles_validos:
            raise ServicioInvalidoError(
                f"Nivel de experto '{valor}' no reconocido. Use: {list(niveles_validos)}"
            )
        self._nivel_experto = valor
        self._factor_experto = niveles_validos[valor]

    def calcular_costo(self, impuesto=0.0, descuento=0.0, **kwargs):
        base = super().calcular_costo(impuesto=0.0, descuento=0.0)
        total = base * self.horas * self._factor_experto
        total -= total * (descuento / 100)
        total += total * (impuesto / 100)
        if total < 0:
            raise CalculoInconsistenteError("Costo inconsistente en AsesoriaEspecializada")
        return round(total, 2)

    def validar(self):
        if self._horas <= 0 or self._precio_base <= 0:
            raise ServicioInvalidoError(f"Asesoría '{self.nombre}' tiene datos inconsistentes")
        return True

    def describir(self):
        return (
            f"[Asesoría] #{self.id} {self.nombre} | Nivel: {self.nivel_experto} "
            f"| {self.horas}h | Precio base/h: ${self.precio_base:,.2f} "
            f"| Disponible: {self.disponible}"
        )
