# 2048 en la terminal 

## Descripción

Este proyecto es una versión del clásico juego 2048 para jugar directamente en la terminal, sin necesidad de navegador ni interfaz gráfica. Está programado en Python, usando programación orientada a objetos (POO):

Además del modo clásico, incluye una versión basada en la secuencia de Fibonacci (se explicará con más detalle a continuación).

## Requisitos

- Tener instalado Python 3.8 o superior.
- No hace falta instalar ninguna librería externa: el juego solo usa módulos que ya vienen incluidos con Python.

## Instalación

Sigue estos pasos:

1. Descarga o clona el proyecto en tu ordenador, de forma que tengas el archivo `main.py` en una carpeta.

2. **Comprueba que tienes Python instalado.** Abre una terminal y escribe:
   ```
   python --version
   ```
   o, en algunos sistemas:
   ```
   python3 --version
   ```
   Debería mostrarte una versión 3.8 o superior. Si no tienes Python instalado, descárgalo desde [python.org](https://www.python.org/downloads/).

3. Sitúate en la carpeta del proyecto con la terminal:
   ```
   cd ruta/a/la/carpeta/del/proyecto
   ```

4. Ejecuta el juego:
   ```
   python juego.py
   ```
   O, si en tu sistema hace falta especificar la versión:
   ```
   python3 juego.py
   ```

5. Al arrancar, el juego te preguntará el tipo de partiday el tamaño del tablero. Escribe tu respuesta y pulsa Enter.

## Reglas del juego 

### Movimiento

El tablero se controla con las teclas **W, A, S, D**, igual que en muchos videojuegos:

| Tecla | Dirección   |
|-------|-------------|
| `w`   | Arriba      |
| `a`   | Izquierda   |
| `s`   | Abajo       |
| `d`   | Derecha     |

Para mover, escribe la letra correspondiente en la terminal y pulsa Enter.

### El objetivo

Cada vez que mueves el tablero en una dirección, todas las fichas se deslizan hacia ese lado. Si dos fichas "compatibles" chocan entre sí, se combinan en una sola ficha de mayor valor. Después de cada movimiento válido, aparece una ficha nueva en una casilla vacía al azar.

Para ganar, tienes que alcanzar la ficha objetivo (2048 en el modo clásico, o 2584 en el modo Fibonacci) evitando que el tablero se llene por completo. 

### Otros comandos

Además de moverte, puedes escribir estos comandos en cualquier momento:

- **`save`** → Guarda tu partida actual, para poder continuarla más adelante.
- **`load`** → Recupera la última partida guardada de este mismo modo de juego (2048 o Fibonacci).
- **`end`** → Termina la partida en cualquier momento.

> **Nota sobre `save`/`load`:** Las partidas se guardan según el tipo de juego (2048 o Fibonacci), no según el tamaño del tablero. Si guardas una partida y luego empiezas otra del mismo tipo pero con un tamaño de tablero distinto, al usar `save` se sobrescribirá el archivo guardado anteriormente. `load` no te dejará cargar una partida en un tablero de tamaño incompatible, pero la partida guardada previa se perderá igualmente si la sobrescribes.

## Modalidades de juego

Al empezar, puedes elegir entre dos modos:

### 2048 (modo clásico)

Es el juego original: las fichas empiezan siendo 2 o 4, y dos fichas se combinan cuando tienen el mismo valor (por ejemplo, 2+2 = 4, 8+8 = 16). El objetivo es llegar a la ficha de 2048.

### Fibonacci (modo alternativo)

En este modo, las fichas empiezan siendo 0 o 1, y dos fichas se combinan solo si son números consecutivos en la secuencia de Fibonacci (0, 1, 1, 2, 3, 5, 8, 13, 21...). Por ejemplo, 3 y 5 se combinan en 8, porque son consecutivos en la secuencia. El objetivo es llegar a la ficha de 2584.

## Tamaño del tablero

Puedes elegir el tamaño del tablero al empezar la partida (por ejemplo, 4x4, como en el juego original, aunque puedes elegir otros tamaños).

No hay un límite máximo técnico para el tamaño del tablero. Sin embargo, se recomienda no pasar de un tablero de unas 10x10 casillas, ya que con tableros muy grandes el texto puede desalinearse visualmente en la terminal a medida que los números crecen, y la partida se vuelve más difícil de seguir a simple vista.

