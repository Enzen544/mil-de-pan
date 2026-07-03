from abc import ABC, abstractmethod
from datetime import datetime
import itertools


class EntidadBase(ABC):
    _contador = itertools.count(1)

    def __init__(self):
        self._id = next(EntidadBase._contador)
        self._fecha_creacion = datetime.now()

    @property
    def id(self):
        return self._id

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @abstractmethod
    def describir(self):
        raise NotImplementedError

    @abstractmethod
    def validar(self):
        raise NotImplementedError

    def __str__(self):
        return self.describir()
