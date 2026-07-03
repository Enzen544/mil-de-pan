import sys
sys.stdout.reconfigure(encoding="utf-8")

from cliente import Cliente
from servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva
from excepciones import SoftwareFJError
from logger_config import logger

clientes = []
servicios = []
reservas = []


def linea(titulo):
    print("\n" + "=" * 70)
    print(titulo)
    print("=" * 70)


def operacion(numero, descripcion, funcion):
    print(f"\n--- Operación {numero}: {descripcion} ---")
    try:
        resultado = funcion()
        print(f"OK: {resultado}")
        return resultado
    except SoftwareFJError as err:
        logger.error(f"Operación {numero} ({descripcion}) FALLÓ: {err}")
        print(f"ERROR controlado: {err}")
        return None
    except Exception as err:
        logger.critical(f"Operación {numero} ({descripcion}) - ERROR INESPERADO: {err}")
        print(f"ERROR INESPERADO (registrado en logs): {err}")
        return None


def main():
    linea("SOFTWARE FJ - DEMOSTRACIÓN DEL SISTEMA")

    def op1():
        c = Cliente("Cristian Gomez", "1052345678", "cristian@example.com", "3125557788")
        clientes.append(c)
        return c.describir()

    def op2():
        c = Cliente("Ana Rodriguez", "10AB56", "ana@example.com", "3115557788")
        clientes.append(c)
        return c.describir()

    operacion(1, "Registrar cliente válido (Cristian)", op1)
    operacion(2, "Registrar cliente con documento inválido", op2)

    def op3():
        c = Cliente("Ana Graciela Rodriguez", "1098765432", "ana.rodriguez@correo.com", "3011234567")
        clientes.append(c)
        return c.describir()

    def op4():
        c = Cliente("Pedro Perez", "1000111222", "pedro-en-correo-mal", "3009876543")
        clientes.append(c)
        return c.describir()

    operacion(3, "Registrar cliente válido (Ana)", op3)
    operacion(4, "Registrar cliente con email inválido", op4)

    def op5():
        s = ReservaSala("Sala Ejecutiva A", 50000, capacidad=10, horas=3)
        servicios.append(s)
        return s.describir()

    def op6():
        s = AlquilerEquipo("Videobeam Epson", -20000, dias=2)
        servicios.append(s)
        return s.describir()

    operacion(5, "Crear servicio ReservaSala válido", op5)
    operacion(6, "Crear servicio AlquilerEquipo con precio negativo", op6)

    def op7():
        s = AlquilerEquipo("Portátil Dell Precision", 35000, dias=4)
        servicios.append(s)
        return s.describir()

    def op8():
        s = AsesoriaEspecializada("Asesoría en Ciberseguridad", 80000, horas=2, nivel_experto="senior")
        servicios.append(s)
        return s.describir()

    operacion(7, "Crear servicio AlquilerEquipo válido", op7)
    operacion(8, "Crear servicio AsesoriaEspecializada válido", op8)

    def op9():
        s = AsesoriaEspecializada("Asesoría Legal", 60000, horas=1, nivel_experto="maestro-jedi")
        servicios.append(s)
        return s.describir()

    operacion(9, "Crear AsesoriaEspecializada con nivel inválido", op9)

    def op10():
        cliente_ok = clientes[0]
        servicio_ok = servicios[0]
        r = Reserva(cliente_ok, servicio_ok, duracion=3)
        r.procesar(impuesto=19, descuento=10)
        r.confirmar()
        reservas.append(r)
        return r.describir()

    operacion(10, "Crear y confirmar reserva exitosa (con impuesto/descuento)", op10)

    def op11():
        servicio_ok = servicios[2] if len(servicios) > 2 and servicios[2] else servicios[0]
        r = Reserva(clientes[0], servicio_ok, duracion=4)
        r.procesar()
        r.confirmar()
        reservas.append(r)
        return r.describir()

    operacion(11, "Crear y confirmar reserva exitosa (costo simple)", op11)

    def op12():
        servicio_agotado = servicios[0]
        servicio_agotado.marcar_no_disponible()
        r = Reserva(clientes[0], servicio_agotado, duracion=1)
        reservas.append(r)
        return r.describir()

    operacion(12, "Intentar reservar un servicio ya no disponible", op12)

    def op13():
        r = reservas[0]
        r.cancelar()
        r.confirmar()
        return r.describir()

    operacion(13, "Cancelar reserva y luego intentar confirmarla (debe fallar)", op13)

    linea("RESUMEN FINAL DEL SISTEMA")
    print(f"\nClientes registrados exitosamente: {len(clientes)}")
    for c in clientes:
        print(f"  - {c.describir()}")

    print(f"\nServicios creados exitosamente: {len(servicios)}")
    for s in servicios:
        print(f"  - {s.describir()}")

    print(f"\nReservas gestionadas: {len(reservas)}")
    for r in reservas:
        print(f"  - {r.describir()}")

    print("\nEl sistema ejecutó todas las operaciones sin detenerse.")
    print("Revisa el archivo 'logs/eventos.log' para el detalle completo de eventos y errores.")


if __name__ == "__main__":
    main()
