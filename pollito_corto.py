from tkinter import *
import random

# Configuracion del juego
BASE = 800
ALTURA = 530
NIVEL_MAXIMO = 7

# Variables del pollito (el jugador)
px = 400
py = 480

# Variables del estado del juego
nivel = 1
pausa = False
fin = False
gano = False

# Listas de obstaculos
carros = []
baches = []


def crear():
    # Crea los carros y los baches segun el nivel actual
    global carros, baches
    carros = []
    cantidad_carros = 6 + nivel
    fila = 0
    for i in range(cantidad_carros):
        x = random.randint(0, BASE)
        y = 100 + fila * 100
        velocidad = 3 + nivel
        if random.choice([True, False]):
            velocidad = velocidad * -1
        carros.append([x, y, velocidad])

        fila = fila + 1
        if fila > 3:
            fila = 0

    baches = []
    if nivel >= 3:
        cantidad_baches = nivel - 2
        for i in range(cantidad_baches):
            x = random.randint(50, 700)
            y = random.randint(100, 450)
            baches.append([x, y])


def dibujar():
    c.delete("all")
    # Pasto arriba y abajo, carretera en el medio
    c.create_rectangle(0, 0, BASE, 50, fill="lightgreen")
    c.create_rectangle(0, 50, BASE, 490, fill="gray")
    c.create_rectangle(0, 490, BASE, ALTURA, fill="lightgreen")

    # Lineas blancas de la carretera
    for y in range(150, 450, 100):
        for x in range(0, BASE, 80):
            c.create_rectangle(x, y, x + 40, y + 5, fill="white")

    # Dibujar baches
    for bache in baches:
        a = bache[0]
        b = bache[1]
        c.create_oval(a, b, a + 70, b + 40, fill="black")

    # Dibujar carros
    for carro in carros:
        x = carro[0]
        y = carro[1]
        c.create_rectangle(x, y - 15, x + 60, y + 15, fill="red")
        c.create_oval(x + 5, y + 10, x + 18, y + 23, fill="black")
        c.create_oval(x + 42, y + 10, x + 55, y + 23, fill="black")

    # Dibujar el pollito
    c.create_oval(px - 15, py - 10, px + 15, py + 20, fill="yellow")
    c.create_oval(px - 12, py - 30, px + 12, py, fill="yellow")
    c.create_oval(px - 7, py - 22, px - 2, py - 17, fill="black")
    c.create_polygon(px, py - 10, px + 12, py - 5, px, py, fill="orange")

    # Texto de nivel y mensajes
    texto_nivel = "Nivel " + str(nivel) + "/" + str(NIVEL_MAXIMO)
    c.create_text(60, 25, text=texto_nivel, font=("Arial", 16, "bold"))

    if pausa:
        c.create_text(400, 265, text="PAUSADO", font=("Arial", 35, "bold"))

    if fin:
        if gano:
            c.create_text(400, 265, text="GANASTE", font=("Arial", 35, "bold"))
        else:
            c.create_text(400, 265, text="PERDISTE", font=("Arial", 35, "bold"))


def choque():
    # Revisa si el pollito choco con un carro o un bache
    global fin, gano

    for carro in carros:
        x = carro[0]
        y = carro[1]
        ancho = 60
        alto = 15
        if px - 15 < x + ancho and px + 15 > x and py - 20 < y + alto and py + 20 > y - alto:
            fin = True
            gano = False
            return

    for bache in baches:
        x = bache[0]
        y = bache[1]
        ancho = 70
        alto = 20
        if px - 15 < x + ancho and px + 15 > x and py - 20 < y + alto and py + 20 > y - alto:
            fin = True
            gano = False
            return


def meta():
    # Revisa si el pollito llego a la meta (arriba de todo)
    global nivel, px, py, fin, gano

    if py <= 50:
        if nivel < NIVEL_MAXIMO:
            nivel = nivel + 1
            px = 400
            py = 480
            crear()
        else:
            fin = True
            gano = True


def mover(evento):
    global px, py

    if pausa or fin:
        return

    tecla = evento.keysym
    if tecla == "Up":
        py = py - 20
    if tecla == "Down":
        py = py + 20
    if tecla == "Left":
        px = px - 20
    if tecla == "Right":
        px = px + 20

    # Que el pollito no se salga de la pantalla
    if px < 20:
        px = 20
    if px > BASE - 20:
        px = BASE - 20
    if py < 20:
        py = 20
    if py > 490:
        py = 490

    choque()
    meta()
    dibujar()


def mover_carros():
    # Mueve los carros cada cierto tiempo
    if not pausa and not fin:
        for carro in carros:
            carro[0] = carro[0] + carro[2]
            if carro[2] > 0 and carro[0] > BASE:
                carro[0] = -70
            if carro[2] < 0 and carro[0] < -70:
                carro[0] = BASE
        choque()
        dibujar()

    ventana.after(40, mover_carros)


def pausar():
    global pausa
    pausa = not pausa
    if pausa:
        boton.config(text="CONTINUAR")
    else:
        boton.config(text="PAUSAR")
    dibujar()


def reiniciar():
    global nivel, px, py, pausa, fin, gano
    nivel = 1
    px = 400
    py = 480
    pausa = False
    fin = False
    gano = False
    crear()
    dibujar()


# Ventana principal
ventana = Tk()
ventana.title("Pollito Cruzando")
ventana.geometry("800x600")
ventana.resizable(False, False)

c = Canvas(ventana, width=BASE, height=ALTURA)
c.pack()

f = Frame(ventana, bg="black")
f.pack(fill=X)
Label(f, text="Usa las flechas para mover", fg="white", bg="black").pack(side=LEFT, padx=10)
boton = Button(f, text="PAUSAR", command=pausar, width=10)
boton.pack(side=RIGHT)
Button(f, text="REINICIAR", command=reiniciar, width=10).pack(side=RIGHT)
Button(f, text="SALIR", command=ventana.destroy, width=10).pack(side=RIGHT)

ventana.bind("<KeyPress>", mover)

crear()
dibujar()
mover_carros()
ventana.mainloop()
