from models import Cliente
from logs import Log
import os

log = Log()

def cargarCliente(tipo):
    while True:
        num = input("Introduce el número de cliente: ")
        log.escribir(
            "INFO",
            f"Se está intentando cargar el cliente {num}"
        )

        if len(num) != 6 or not num.isdigit():
            print("El formato introducido no es correcto")
            continue

        if tipo == "movimientos":
            return leerFichero(num)

        elif tipo == "guardado":
            return cargarClienteGuardado(num)


def leerFichero(numCliente):

    cliente = Cliente(numCliente)
    procesos=0

    try:
        with open(f"ficherosClientes/{numCliente}.txt", "r") as f:

            linea = f.readline()

            while linea:

                datos = linea.strip().split(";")

                cantidad = float(datos[0])
                operacion = datos[1]
                destino = datos[2]

                if destino == "Cuenta" and operacion == "Ingreso":
                    cliente.cuenta.ingresar(cantidad)
                    procesos+=1

                elif destino == "Cuenta" and operacion == "Retirada":
                    cliente.cuenta.retirar(cantidad)
                    procesos += 1

                elif destino == "Deposito" and operacion == "Ingreso":
                    cliente.deposito.ingresar(cantidad)
                    procesos += 1

                elif destino == "Deposito" and operacion == "Retirada":
                    cliente.deposito.retirar(cantidad)
                    procesos += 1
                else:
                    log.escribir("WARNING",
                                 f"movimiento ignorando en cliente {numCliente}:operacion {operacion} o destino: {destino} desconocido")


                linea = f.readline()

        # Guardamos el estado final del cliente
        cliente.guardar()

        print("Datos del cliente cargados correctamente")
        print(f"Cliente: {cliente.getNumero()}\n" +
              f"Saldo cuenta:  {float(cliente.getCuenta().getSaldo())}€\n" +
              f"Saldo depósito: {float(cliente.getDeposito().getSaldo())}€\n")
        print(f"Movimientos procesados: {procesos}")
        log.escribir( "INFO",f"Movimientos del cliente {numCliente} procesados: {procesos}")

        log.escribir(
            "INFO",
            f"Se han cargado los datos del cliente {cliente.getNumero()}"
        )
        return cliente

    except FileNotFoundError:
        print("El usuario no tiene ninguna cuenta con el banco")
        log.escribir(
            "ERROR",
            f"Fichero de movimientos inexistente"
        )
        return None


def cargarClienteGuardado(numCliente):

    try:
        with open(f"datosClientes/{numCliente}.txt", "r") as f:

            linea = f.readline()
            datos = linea.split(";")

            cliente = Cliente(datos[0])

            cliente.cuenta.saldo = float(datos[1])
            cliente.deposito.saldo = float(datos[2])
            log.escribir(
                "INFO",
                f"Se han cargado las cuentas del {cliente.getNumero()}"
            )
            return cliente

    except FileNotFoundError:
        print("Primero tienes que cargar los datos de este cliente")
        return None

def listarClientes():
    print("Clientes cargados")
    if not os.path.exists("datosClientes"):
        print("No hay clientes cargados")
        return

    numeros = sorted(
        nombre[:-4] for nombre in os.listdir("datosClientes")
        if nombre.endswith(".txt")
    )

    if not numeros:
        print("No hay clientes cargados")
        return

    for numero in numeros:
        print(f"- {numero}")

    print("")
