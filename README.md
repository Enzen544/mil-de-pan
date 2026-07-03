# Software FJ — Sistema Integral de Gestión de Clientes, Servicios y Reservas
## Requisitos
- Python 3.8 o superior (no requiere librerías externas).

## Cómo ejecutar

```bash
python3 main.py
```

## Estructura del proyecto

```
software_fj/
├── main.py              # Programa principal / demo de 13 operaciones
├── entidad_base.py       # Clase abstracta base (EntidadBase)
├── cliente.py             # Clase Cliente (encapsulación + validaciones)
├── servicio.py             # Clase abstracta Servicio + 3 subclases:
│                              ReservaSala, AlquilerEquipo, AsesoriaEspecializada
├── reserva.py               # Clase Reserva (integra Cliente + Servicio)
├── excepciones.py            # Excepciones personalizadas del sistema
├── logger_config.py           # Configuración del logging a archivo
└── logs/
    └── eventos.log            # Se genera automáticamente al ejecutar
```

## Principios de POO aplicados

- **Abstracción**: `EntidadBase` y `Servicio` son clases abstractas
  (`ABC` + `@abstractmethod`) que obligan a las subclases a implementar
  `describir()` y `validar()`.
- **Herencia**: `Cliente`, `Servicio` y `Reserva` heredan de `EntidadBase`.
  `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada` heredan de `Servicio`.
- **Polimorfismo**: cada subclase de `Servicio` sobrescribe
  `calcular_costo()` y `describir()` con su propia lógica particular
  (por horas, por días, por nivel de experto).
- **Encapsulación**: todos los atributos son privados (`_atributo`) y se
  acceden/validan mediante `@property` / `@x.setter`.
- **Sobrecarga (simulada)**: `calcular_costo(impuesto=0.0, descuento=0.0, **kwargs)`
  admite distintas combinaciones de parámetros opcionales.

## Manejo de excepciones

Todas las excepciones personalizadas (`excepciones.py`) heredan de
`SoftwareFJError`. Se usan bloques `try/except`, `try/except/else`,
`try/except/finally` y **encadenamiento** (`raise ... from err`) en
`reserva.py` (método `procesar`) y en `servicio.py` (setter de precio).
Cada error se registra en `logs/eventos.log` mediante el módulo
`logging`, y el programa **nunca se detiene**: `main.py` atrapa
cualquier excepción por operación y continúa con la siguiente.

## Autores
_(Aqui ponen los nombres del grupo rodrigo, cada integrante)_
