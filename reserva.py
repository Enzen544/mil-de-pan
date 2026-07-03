from entidad_base import EntidadBase
from cliente import Cliente
from servicio import Servicio
from excepciones import (
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
)
from logger_config import logger

ESTADOS_VALIDOS = ("pendiente", "confirmada", "cancelada")


class Reserva(EntidadBase):
    def __init__(self, cliente, servicio, duracion):
        super().__init__()

        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un objeto Cliente válido")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un objeto Servicio válido")
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ReservaInvalidaError("La duración de la reserva debe ser un número positivo")

        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre}' no está disponible para reservar"
            )

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self._estado = "pendiente"
        self._costo_final = None
        logger.info(
            f"Reserva #{self.id} creada (pendiente) -> Cliente: {cliente.nombre} "
            f"| Servicio: {servicio.nombre}"
        )

    @property
    def estado(self):
        return self._estado

    @property
    def costo_final(self):
        return self._costo_final

    def procesar(self, impuesto=0.0, descuento=0.0):
        if self._estado == "cancelada":
            raise OperacionNoPermitidaError(
                f"No se puede procesar la reserva #{self.id}: ya está cancelada"
            )
        try:
            self._costo_final = self.servicio.calcular_costo(
                impuesto=impuesto, descuento=descuento
            )
        except CalculoInconsistenteError as err:
            logger.error(f"Fallo al procesar reserva #{self.id}: {err}")
            raise ReservaInvalidaError(
                f"No fue posible procesar la reserva #{self.id} por un cálculo inconsistente"
            ) from err
        else:
            logger.info(f"Reserva #{self.id} procesada. Costo final: ${self._costo_final:,.2f}")
        finally:
            logger.debug(f"Intento de procesamiento finalizado para reserva #{self.id}")
        return self._costo_final

    def confirmar(self):
        if self._estado == "cancelada":
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva #{self.id}: está cancelada"
            )
        if self._costo_final is None:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar la reserva #{self.id} sin haberla procesado antes"
            )
        self._estado = "confirmada"
        logger.info(f"Reserva #{self.id} CONFIRMADA")
        return True

    def cancelar(self):
        if self._estado == "confirmada":
            logger.warning(
                f"Se cancela la reserva #{self.id} que ya estaba confirmada"
            )
        self._estado = "cancelada"
        logger.info(f"Reserva #{self.id} CANCELADA")
        return True

    def validar(self):
        if self._estado not in ESTADOS_VALIDOS:
            raise ReservaInvalidaError(f"Estado de reserva '#{self._estado}' no reconocido")
        return True

    def describir(self):
        costo = f"${self._costo_final:,.2f}" if self._costo_final is not None else "N/A"
        return (
            f"Reserva #{self.id} | Cliente: {self.cliente.nombre} "
            f"| Servicio: {self.servicio.nombre} | Duración: {self.duracion} "
            f"| Estado: {self.estado} | Costo: {costo}"
        )
