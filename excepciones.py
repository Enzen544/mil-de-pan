class SoftwareFJError(Exception):
    def __init__(self, mensaje="Ha ocurrido un error en el sistema Software FJ"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class DatosInvalidosError(SoftwareFJError):
    def __init__(self, mensaje="Los datos ingresados no son válidos"):
        super().__init__(mensaje)


class ParametroFaltanteError(SoftwareFJError):
    def __init__(self, mensaje="Falta un parámetro obligatorio"):
        super().__init__(mensaje)


class ClienteInvalidoError(SoftwareFJError):
    def __init__(self, mensaje="El cliente ingresado no es válido"):
        super().__init__(mensaje)


class ServicioNoDisponibleError(SoftwareFJError):
    def __init__(self, mensaje="El servicio solicitado no está disponible"):
        super().__init__(mensaje)


class ServicioInvalidoError(SoftwareFJError):
    def __init__(self, mensaje="El servicio ingresado no es válido"):
        super().__init__(mensaje)


class OperacionNoPermitidaError(SoftwareFJError):
    def __init__(self, mensaje="La operación solicitada no está permitida"):
        super().__init__(mensaje)


class ReservaInvalidaError(SoftwareFJError):
    def __init__(self, mensaje="La reserva no pudo ser procesada"):
        super().__init__(mensaje)


class CalculoInconsistenteError(SoftwareFJError):
    def __init__(self, mensaje="Se detectó un cálculo inconsistente"):
        super().__init__(mensaje)
