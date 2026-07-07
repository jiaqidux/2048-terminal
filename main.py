from __future__ import annotations
from typing import Callable
from typing import Union
from typing import Optional
import random

FILE1 = "2048"
FILE2 = "fibo"


class Fila:
    def __init__(self, param: Union[int, list[Optional[int]]], condic: Callable[[int, int], bool]):
        # Si param == int: creamos una fila de ese tamaño
        # Si param == list[Optional[int]]: creamos una fila con esos números
        if isinstance(param, int):
            self.fila = [None] * param
        else:
            self.fila = param
        # Condición para que puedan concatenarse dos números
        self.concatenables = condic

    def longitud(self) -> int:
        return len(self.fila)

    # Función que reemplaza un número de la fila
    def añadir_num(self, pos: int, num: int) -> None:
        # <= pos <= len(Fila) - 1
        self.fila[pos] = num

    # Función que devuelve un número de la fila
    def devolver_num(self, pos: int) -> int:
        # <= pos <= len(Fila) - 1
        return self.fila[pos]

    # Función que refleja una fila
    def reflejar(self) -> None:
        result = []
        # Añadimos los elementos a las filas empezando desde el final
        for i in range(len(self.fila)):
            result.append(self.fila[len(self.fila) - 1 - i])
        self.fila = result

    # Función que devuelve el máximo de una fila
    def maximo(self) -> int:
        mayor = 0
        for num in self.fila:
            if num is not None and num > mayor:
                mayor = num
        return mayor

    # Función que desliza una fila hacia la izquierda, concatenándolos si es posible
    def deslizar(self) -> tuple[bool, int, int]:
        # Devuelve si se ha producido movimiento o no, la puntuación y el mayor número
        result = []
        puntuacion = 0
        i = 0
        while i < len(self.fila):
            # Buscamos el primer elemento no nulo
            if self.fila[i] is None:
                i += 1
            else:
                # Buscamos el siguiente elemento no nulo
                j = i + 1
                while j < len(self.fila) and self.fila[j] is None:
                    j += 1
                # Si los dos elementos son concatenables, añadimos su suma a la nueva fila
                # y repetimos el proceso desde la posición j + 1
                if j < len(self.fila) and self.concatenables(self.fila[i], self.fila[j]):
                    result.append(self.fila[i] + self.fila[j])
                    puntuacion += (self.fila[i] + self.fila[j])
                    i = j + 1
                # En caso contrario (no son concatenables), añadimos el primer elemento a la nueva fila
                # y seguimos el proceso desde la posición j
                else:
                    result.append(self.fila[i])
                    i = j
        # Añadimos None hasta que la nueva fila alcance la longitud necesaria
        while len(result) < len(self.fila):
            result.append(None)
        # Miramos si se ha producido movimiento
        cambio = self.fila != result
        # Actualizamos nuestra fila actual
        self.fila = result
        # Buscamos el mayor número
        mayor = self.maximo()
        return cambio, puntuacion, mayor

    # Función que nos indica si una fila está llena
    def esta_lleno(self) -> bool:
        # Si encontramos una celda vacía, no está llena
        for i in range(len(self.fila)):
            if self.fila[i] is None:
                return False
        return True

    # Función que devuelve si dos filas se pueden concatenar
    def final(self, other: Fila) -> int:
        for i in range(len(self.fila)):
            if self.concatenables(self.fila[i], other.fila[i]):
                return True
        return False

    # Función que convierte una fila en un str para guardarlo en un archivo
    def str_archivo(self) -> str:
        result = ""
        for num in self.fila:
            result += str(num) + " "
        result += "\n"
        return result

    # Función que convierte una fila en un str para imprimirlo
    def __str__(self) -> str:
        result = "|"
        for num in self.fila:
            if num is None:
                num = ""
            result += f"{num:<4}|"
        return result

    def __eq__(self, other: Fila) -> bool:
        return self.fila == other.fila

    @staticmethod
    def prueba_deslizar():
        f1 = Fila([2, 2, 4, 4], Juego.son_iguales)
        f2 = Fila([2, None, 2, 4], Juego.son_iguales)
        f3 = Fila([1, 1, 1, 1, 1], Juego.son_consecutivos)
        f4 = Fila([0, 3, 5, 0, 1], Juego.son_consecutivos)
        f1.deslizar()
        f2.deslizar()
        f3.deslizar()
        f4.deslizar()
        assert f1 == Fila([4, 8, None, None], Juego.son_iguales), " ERROR en [2, 2, 4, 4]. Debería ser [4, 8, None, None]"
        assert f2 == Fila([4, 4, None, None], Juego.son_iguales), "ERROR en [2, 0, 2, 4]. Debería ser [4, 4, None, None]"
        assert f3 == Fila([2, 2, 1, None, None], Juego.son_consecutivos), "ERROR en [1, 1, 1, 0, 0]. Debería ser [2, 2, 1, None, None]"
        assert f4 == Fila([0, 8, 1, None, None], Juego.son_consecutivos), "ERROR en [0, 3, 5, 0, 1]. Debería ser [0, 8, 1, None, None]"


class Tablero:
    def __init__(self, param: Union[int, list[Fila]], condic: Callable[[int, int], bool]):
        # Si param == int: creamos un tablero de ese tamaño
        # Si param == list[Fila]: creamos un tablero con esas filas
        if isinstance(param, int):
            self.tablero = []
            for i in range(param):
                self.tablero.append(Fila(param, condic))
        else:
            self.tablero = param
        self.concatenables = condic

    # Función que devuelve el tamaño de un tablero
    def tamaño(self) -> int:
        for fila in self.tablero:
            return fila.longitud()

    # Función que añade un número en una posición aleatoria del tablero
    def añadir_num(self, num: int) -> None:
        # Generamos dos posiciones
        x, y = random.randint(0, self.tamaño() - 1), random.randint(0, self.tamaño() - 1)
        # Miramos si las posiciones están vacías
        while self.tablero[x].devolver_num(y) is not None:
            x, y = random.randint(0, self.tablero[0].longitud() - 1), random.randint(0, self.tablero[0].longitud() - 1)
        self.tablero[x].añadir_num(y, num)

    # Función que refleja un tablero
    def reflejar(self) -> None:
        for fila in self.tablero:
            fila.reflejar()

    # Función que transpone un tablero
    def transponer(self) -> None:
        result = []
        for j in range(self.tamaño()):
            fila0 = []
            for i in range(self.tamaño()):
                # Intercambiamos las posiciones de las filas y las columnas
                fila0.append(self.tablero[i].devolver_num(j))
            result.append(Fila(fila0, self.concatenables))
        self.tablero = result

    # Funciones de movimiento
    # Todas devuelven lo mismo (al igual que en clase Fila)
    def mover_l(self) -> tuple[bool, int, int]:
        cambio, puntuacion, mayor = False, 0, 0
        for fila in self.tablero:
            cambio0, puntuacion0, mayor0 = fila.deslizar()
            if cambio0:
                cambio = True
                puntuacion += puntuacion0
                if mayor0 > mayor:
                    mayor = mayor0
        return cambio, puntuacion, mayor

    # Para mover hacia la derecha reflejamos y movemos hacia la izquierda
    def mover_r(self) -> tuple[bool, int, int]:
        self.reflejar()
        cambio, puntuacion, mayor = self.mover_l()
        self.reflejar()
        return cambio, puntuacion, mayor

    # Para mover hacia arriba transponemos y movemos hacia la izquierda
    def mover_u(self) -> tuple[bool, int, int]:
        self.transponer()
        cambio, puntuacion, mayor = self.mover_l()
        self.transponer()
        return cambio, puntuacion, mayor

    # Para mover hacia abajo transponemos y movemos hacia la derecha
    def mover_d(self) -> tuple[bool, int, int]:
        self.transponer()
        cambio, puntuacion, mayor = self.mover_r()
        self.transponer()
        return cambio, puntuacion, mayor

    # Función que devuelve si un tablero está lleno
    def esta_lleno(self) -> bool:
        for fila in self.tablero:
            if not fila.esta_lleno():
                return False
        return True

    # Función que devuelve si en un tablero se pueden concatenar filas
    def final(self) -> bool:
        for i in range(self.tablero[0].longitud() - 1):
            # Miramos si hay dos filas o dos columnas concatenables
            if self.tablero[i].final(self.tablero[i + 1]):
                return False
            # Transponemos para mirar las columnas
            self.transponer()
            if self.tablero[i].final(self.tablero[i + 1]):
                # Devolvemos el tablero a su forma original
                self.transponer()
                return False
            self.transponer()
        return True

    # Función que convierte un tablero en un str para guardarlo en un archivo
    def str_archivo(self) -> str:
        result = ""
        for fila in self.tablero:
            result += fila.str_archivo()
        return result

    # Función que convierte un tablero en un str para imprimirlo
    def __str__(self) -> str:
        result = ""
        for fila in self.tablero:
            result += str(fila) + "\n"
        return result

    def __eq__(self, other: Tablero) -> bool:
        return self.tablero == other.tablero

    @staticmethod
    def prueba_mover_l():
        condic = Juego.son_iguales
        f1 = Fila([2, 2, 4, 8], condic)
        f2 = Fila([2, 2, 2, 2], condic)
        f3 = Fila([None, None, 2, 2], condic)
        f4 = Fila([2, None, 2, 4], condic)
        t1 = Tablero([f1, f2, f3, f4], condic)
        t1.mover_l()
        f5 = Fila([4, 4, 8, None], condic)
        f6 = Fila([4, 4, None, None], condic)
        f7 = Fila([4, None, None, None], condic)
        f8 = Fila([4, 4, None, None], condic)
        assert t1 == Tablero([f5, f6, f7, f8], condic), "ERROR"

    @staticmethod
    def prueba_mover_r():
        condic = Juego.son_consecutivos
        f1 = Fila([0, 5, 0, 8], condic)
        f2 = Fila([1, 3, 0, 5], condic)
        f3 = Fila([1, 2, 0, None], condic)
        f4 = Fila([0, 1, 1, 1], condic)
        t1 = Tablero([f1, f2, f3, f4], condic)
        t1.mover_r()
        f5 = Fila([0, 5, 0, 8], condic)
        f6 = Fila([1, 3, 0, 5], condic)
        f7 = Fila([None, None, 3, 0], condic)
        f8 = Fila([None, None, 1, 2], condic)
        assert t1 == Tablero([f5, f6, f7, f8], condic), "ERROR"

    @staticmethod
    def prueba_mover_u():
        condic = Juego.son_consecutivos
        f1 = Fila([0, 5, 0, 8], condic)
        f2 = Fila([1, 3, 0, 5], condic)
        f3 = Fila([1, 2, 0, None], condic)
        f4 = Fila([0, 1, 1, 1], condic)
        t1 = Tablero([f1, f2, f3, f4], condic)
        t1.mover_u()
        f5 = Fila([1, 8, 0, 13], condic)
        f6 = Fila([1, 3, 0, 1], condic)
        f7 = Fila([None, None, 1, None], condic)
        f8 = Fila([None, None, None, None], condic)
        assert t1 == Tablero([f5, f6, f7, f8], condic), "ERROR"

    @staticmethod
    def prueba_mover_d():
        condic = Juego.son_iguales
        f1 = Fila([2, 2, 4, 8], condic)
        f2 = Fila([2, 2, 2, 2], condic)
        f3 = Fila([None, None, 2, 2], condic)
        f4 = Fila([2, None, 2, 4], condic)
        t1 = Tablero([f1, f2, f3, f4], condic)
        t1.mover_d()
        f5 = Fila([None, None, None, None], condic)
        f6 = Fila([None, None, 4, 8], condic)
        f7 = Fila([2, None, 2, 4], condic)
        f8 = Fila([4, 4, 4, 4], condic)
        assert t1 == Tablero([f5, f6, f7, f8], condic), "ERROR"


class Juego:
    def __init__(self, tam: int, tipo: str):
        # Creamos un tablero según el tipo de juego
        # Asignamos un archivo a cada tipo de juego
        self.tipo = tipo
        if self.tipo == "2048":
            self.tablero = Tablero(tam, Juego.son_iguales)
            self.archivo = FILE1
        else:
            self.tablero = Tablero(tam, Juego.son_consecutivos)
            self.archivo = FILE2
        # Añadimos dos números aleatorios según el tipo de juego
        x, y = Juego.generar_num(self.tipo), Juego.generar_num(self.tipo)
        self.tablero.añadir_num(x)
        self.tablero.añadir_num(y)
        self.puntuacion = 0
        self.mayor = max(x, y)

    @staticmethod
    # Función que genera un número según el tipo de juego
    # Versión 2048: 10% -> 4 y 90% -> 2
    # Versión Fibonacci:  10% -> 0 y 90% -> 1
    def generar_num(tipo: str) -> int:
        num = random.randint(1, 10)
        if tipo == "2048":
            if num == 1:
                return 4
            else:
                return 2
        else:
            if num == 1:
                return 0
            else:
                return 1

    @staticmethod
    # Función que indica si dos números son concatenables en la versión 2048
    # Basta que sean iguales
    def son_iguales(n: int, m: int) -> bool:
        return n == m

    @staticmethod
    # Función que dada un número te devuelve su siguiente en la secuencia de Fibonacci
    def fibonacci(n: int) -> int:
        x, y = 0, 1
        result = x + y
        while result <= n:
            x, y = y, result
            result = x + y
        return result

    @staticmethod
    # Función que indica si dos números son concatenables en la versión Fibonacci
    # Basta que sean consecutivos en la secuencia de Fibonacci
    def son_consecutivos(n: int, m: int) -> bool:
        if n == m == 1:
            return True
        # Elegimos el menor número de los 2
        elif m < n:
            n, m = m, n
        # Generamos el número de Fibonacci mayor que n y vemos si coincide con m
        return Juego.fibonacci(n) == m

    # Funciones de movimiento
    # Si se produce movimiento:
    # 1) Actualizamos los valores de puntuación y mayor número
    # 2) Añadimos un número aleatorio
    def mover_l(self) -> None:
        cambio, puntuacion, mayor = self.tablero.mover_l()
        if cambio:
            num = Juego.generar_num(self.tipo)
            mayor = max(mayor, num)
            self.tablero.añadir_num(num)
            self.puntuacion += puntuacion
            if mayor > self.mayor:
                self.mayor = mayor

    def mover_r(self) -> None:
        cambio, puntuacion, mayor = self.tablero.mover_r()
        if cambio:
            num = Juego.generar_num(self.tipo)
            mayor = max(mayor, num)
            self.tablero.añadir_num(num)
            self.puntuacion += puntuacion
            if mayor > self.mayor:
                self.mayor = mayor

    def mover_u(self) -> None:
        cambio, puntuacion, mayor = self.tablero.mover_u()
        if cambio:
            num = Juego.generar_num(self.tipo)
            mayor = max(mayor, num)
            self.tablero.añadir_num(num)
            self.puntuacion += puntuacion
            if mayor > self.mayor:
                self.mayor = mayor

    def mover_d(self) -> None:
        cambio, puntuacion, mayor = self.tablero.mover_d()
        if cambio:
            num = Juego.generar_num(self.tipo)
            mayor = max(mayor, num)
            self.tablero.añadir_num(num)
            self.puntuacion += puntuacion
            if mayor > self.mayor:
                self.mayor = mayor

    # Resumen de las funciones de movimiento
    def hacer_jugada(self, mov: str) -> None:
        if mov == "a":
            self.mover_l()
        elif mov == "d":
            self.mover_r()
        elif mov == "w":
            self.mover_u()
        elif mov == "s":
            self.mover_d()

    # Función que guarda la puntuación, el mayor número, el tablero y su tamaño en su archivo correspondiente
    def save(self) -> None:
        f = open(self.archivo, "w")
        # Guardamos el tamaño en una línea aparte para facilitar luego load()
        f.write(f"{self.tablero.tamaño()}\n{self.puntuacion} {self.mayor}\n")
        f.write(self.tablero.str_archivo())
        f.close()

    # Función que recupera el tablero de su archivo
    # Devuelve el tamaño del archivo recuperado
    def load(self) -> int:
        f = open(self.archivo, "r")
        linea = f.readline()
        # Si no tenemos ningún tablero guardado devuelve 0
        if len(linea) == 0:
            f.close()
            return 0
        tam = int(linea)
        # Si el tamaño del tablero actual y del tablero recuperado es la misma,
        # actualizamos nuestra información actual
        if self.tablero.tamaño() == tam:
            result = []
            result0 = []
            linea = f.readline()
            for num in linea.split():
                result0.append(int(num))
            # Actualizamos la puntuación y el mayor valor
            self.puntuacion, self.mayor = result0
            linea = f.readline()
            while linea != "":
                fila0 = []
                for num in linea.split():
                    if num == "None":
                        fila0.append(None)
                    else:
                        fila0.append(int(num))
                result.append(Fila(fila0, self.tablero.concatenables))
                linea = f.readline()
            self.tablero = Tablero(result, self.tablero.concatenables)
            f.close()
        return tam

    # Función que devuelve si un juego ha terminado o no
    def final(self) -> bool:
        # Termina si llegamos a 2048 o 2584
        if self.mayor == 2048 or self.mayor == 2584:
            return True
        # También termina si el tablero está lleno y no hay filas concatenables
        elif self.tablero.esta_lleno():
            return self.tablero.final()
        return False

    # Función que muestra la puntuación, el mayor número y el tablero
    def __str__(self) -> str:
        return f"Puntuación: {self.puntuacion}\nMayor valor: {self.mayor}\n{self.tablero}"


class Partida:
    def __init__(self, tam: int, tipo: str):
        self.partida = Juego(tam, tipo)

    def jugar(self):
        # Mostramos el tablero al jugador
        print(self.partida)
        victoria = self.partida.final()
        # Seguimos jugando mientras no se de la condición victoria
        while not victoria:
            mov = input("Introduzca el movimiento (w/a/s/d): ")
            if mov == "end":
                victoria = True
            elif mov == "save":
                self.partida.save()
            elif mov == "load":
                # Miramos si el tamaño del tablero actual y del tablero guardado coinciden
                tam = self.partida.load()
                if self.partida.tablero.tamaño() != tam:
                    print(f"No tienes ningún tablero {self.partida.tablero.tamaño()}x{self.partida.tablero.tamaño()} guardado")
                print(self.partida)
            else:
                self.partida.hacer_jugada(mov)
                print(self.partida)
                # Actualizamos la condición victoria
                victoria = self.partida.final()
            if victoria:
                print("GAME OVER")

    def __str__(self) -> str:
        return str(self.partida)
    
# Pide al usuario la versión del juego que quiere jugar
def pedir_tipo() -> str:
    while True:
        entrada = input("Tipo de juego (2048 / fibo): ").strip().lower()
        if entrada in ("2048", "fibo"):
            return entrada
        print("Escribe '2048' o 'fibo'.")

# Pide al usuario el tamaño del tablero con el que quiere jugar
def pedir_tamaño() -> int:
    while True:
        entrada = input("Tamaño del tablero: ")
        if entrada.isdigit() and int(entrada) >= 2:
            return int(entrada)
        print("Introduce un número entero mayor o igual que 2.")


if __name__ == "__main__":
    tipo = pedir_tipo()
    tam = pedir_tamaño()
    p = Partida(tam, tipo)
    p.jugar()
