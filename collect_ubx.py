import os
import sys


def colectar_punto(ruta: str, nombre: str, tiempo: str = '30') -> int:
    sentencia = "timeout {0} str2str -in serial://ttyACM0:9600#ubx -out file://{1}{2}".format(str(tiempo), str(ruta),
                                                                                              str(nombre))
    bash = os.system(sentencia)
    return bash


if __name__ == "__main__":
    try:
        if len(sys.argv) == 4:
            locals()[sys.argv[1]](sys.argv[2], sys.argv[3])
        elif len(sys.argv) == 5:
            print(sys.argv)
            locals()[sys.argv[1]](sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            print("Error al ejecutar la función")
    except:
        print(len(sys.argv))
        print("No ha sido posible ejecutar la función")
