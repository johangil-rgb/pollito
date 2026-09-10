from tkinter import *
import random

# Configuracion del juego
BASE = 800
ALTURA = 530
NIVEL_MAXIMO = 7

# Variables del pollito (el jugador)
px = 40
py = 265

# Variables del estado del juego
nivel = 1
pausa = False
fin = False
gano = False

# Variables para la animacion del gif
cuadro_actual = 0
esta_quieto = True
contador_quieto = 0
mirando_izquierda = False
cuadros_quieto = []
cuadros_quieto_izquierda = []
cuadros_caminando = []
cuadros_caminando_izquierda = []

# Diccionario para saber que teclas estan abajo en este momento
teclas_abajo = {}

# Listas de obstaculos
carros = []
baches = []


def crear():
    # Crea los carros y los baches segun el nivel actual
    global carros, baches
    carros = []
    cantidad_carros = 6 + nivel
    columna = 0
    for i in range(cantidad_carros):
        x = 150 + columna * 150
        y = random.randint(60, 470)
        velocidad = 3 + nivel
        if random.choice([True, False]):
            velocidad = velocidad * -1
        carros.append([x, y, velocidad])

        columna = columna + 1
        if columna > 3:
            columna = 0

    baches = []
    if nivel >= 3:
        cantidad_baches = nivel - 2
        for i in range(cantidad_baches):
            x = random.randint(150, 650)
            y = random.randint(70, 460)
            baches.append([x, y])


def dibujar():
    c.delete("all")
    # Pasto a los lados y carretera en el medio
    c.create_rectangle(0, 0, 70, ALTURA, fill="lightgreen")
    c.create_rectangle(70, 0, 730, ALTURA, fill="gray")
    c.create_rectangle(730, 0, BASE, ALTURA, fill="lightgreen")

    # Lineas blancas de la carretera
    for x in range(150, 700, 150):
        for y in range(0, ALTURA, 80):
            c.create_rectangle(x, y, x + 5, y + 40, fill="white")

    # Dibujar baches
    for bache in baches:
        a = bache[0]
        b = bache[1]
        c.create_oval(a - 25, b - 25, a + 25, b + 25, fill="black")

    # Dibujar carros
    for carro in carros:
        x = carro[0]
        y = carro[1]
        c.create_rectangle(x - 15, y - 30, x + 15, y + 30, fill="red")
        c.create_oval(x - 13, y - 25, x, y - 12, fill="black")
        c.create_oval(x - 13, y + 12, x, y + 25, fill="black")

    # Dibujar el pollito con el cuadro de animacion actual
    global img
    if esta_quieto and mirando_izquierda:
        lista_cuadros = cuadros_quieto_izquierda
    elif esta_quieto:
        lista_cuadros = cuadros_quieto
    elif mirando_izquierda:
        lista_cuadros = cuadros_caminando_izquierda
    else:
        lista_cuadros = cuadros_caminando

    # Por seguridad, si el cuadro no existe en esta lista, usamos el primero
    indice = cuadro_actual
    if indice >= len(lista_cuadros):
        indice = 0

    img = lista_cuadros[indice]
    c.create_image(px, py, image=img)

    # Texto de nivel y mensajes
    texto_nivel = "Nivel " + str(nivel) + "/" + str(NIVEL_MAXIMO)
    c.create_text(60, 20, text=texto_nivel, font=("Arial", 14, "bold"))

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
        ancho = 15
        alto = 30
        if px - 13 < x + ancho and px + 13 > x - ancho and py - 13 < y + alto and py + 13 > y - alto:
            fin = True
            gano = False
            return

    for bache in baches:
        x = bache[0]
        y = bache[1]
        ancho = 25
        alto = 25
        if px - 13 < x + ancho and px + 13 > x - ancho and py - 13 < y + alto and py + 13 > y - alto:
            fin = True
            gano = False
            return


def meta():
    # Revisa si el pollito llego a la meta (al otro lado)
    global nivel, px, py, fin, gano

    if px >= 750:
        if nivel < NIVEL_MAXIMO:
            nivel = nivel + 1
            px = 40
            py = 265
            crear()
        else:
            fin = True
            gano = True


def mover(evento):
    global px, py, esta_quieto, contador_quieto, mirando_izquierda

    if pausa or fin:
        return

    tecla = evento.keysym
    if tecla != "Up" and tecla != "Down" and tecla != "Left" and tecla != "Right":
        return

    # Como se presiono una tecla de movimiento, el pollito ya no esta quieto
    esta_quieto = False
    contador_quieto = 0

    if tecla == "Left":
        mirando_izquierda = True
    if tecla == "Right":
        mirando_izquierda = False

    if tecla == "Up":
        py = py - 20
    if tecla == "Down":
        py = py + 20
    if tecla == "Left":
        px = px - 20
    if tecla == "Right":
        px = px + 20

    # Que el pollito no se salga de la pantalla
    if px < 15:
        px = 15
    if px > BASE - 15:
        px = BASE - 15
    if py < 15:
        py = 15
    if py > ALTURA - 15:
        py = ALTURA - 15

    choque()
    meta()
    dibujar()


def quitar_tecla(tecla):
    # Se llama un instante despues de soltar la tecla.
    # Si en ese instante llego una repeticion automatica, la tecla
    # todavia aparecera como "abajo" otra vez y no pasara nada raro.
    if tecla in teclas_abajo:
        del teclas_abajo[tecla]


def tecla_liberada(evento):
    # Esperamos 1 milisegundo antes de marcar la tecla como suelta.
    # Asi, si el sistema manda una repeticion automatica (tecla mantenida),
    # esa repeticion llega primero y no se cuenta como un toque nuevo.
    ventana.after(1, quitar_tecla, evento.keysym)


def tecla_presionada(evento):
    tecla = evento.keysym

    if tecla in teclas_abajo:
        # La tecla ya estaba abajo, esto es una repeticion automatica: se ignora
        return

    teclas_abajo[tecla] = True
    mover(evento)


def mover_carros():
    # Mueve los carros cada cierto tiempo
    if not pausa and not fin:
        for carro in carros:
            carro[1] = carro[1] + carro[2]
            if carro[2] > 0 and carro[1] > ALTURA + 30:
                carro[1] = -30
            if carro[2] < 0 and carro[1] < -30:
                carro[1] = ALTURA + 30
        choque()
        dibujar()

    ventana.after(40, mover_carros)


def animar_pollito():
    # Cambia el cuadro del gif para que el pollito se vea caminando o quieto
    global cuadro_actual, esta_quieto, contador_quieto

    if not pausa and not fin:
        # Si el pollito lleva un rato sin moverse, pasa a estar quieto
        if not esta_quieto:
            contador_quieto = contador_quieto + 1
            if contador_quieto >= 3:
                esta_quieto = True

        if esta_quieto and mirando_izquierda:
            limite = len(cuadros_quieto_izquierda)
        elif esta_quieto:
            limite = len(cuadros_quieto)
        elif mirando_izquierda:
            limite = len(cuadros_caminando_izquierda)
        else:
            limite = len(cuadros_caminando)

        cuadro_actual = cuadro_actual + 1
        if cuadro_actual >= limite:
            cuadro_actual = 0

        dibujar()

    ventana.after(150, animar_pollito)


def pausar():
    global pausa
    pausa = not pausa
    if pausa:
        boton.config(text="CONTINUAR")
    else:
        boton.config(text="PAUSAR")
    dibujar()


def reiniciar():
    global nivel, px, py, pausa, fin, gano, esta_quieto, contador_quieto, mirando_izquierda
    nivel = 1
    px = 40
    py = 265
    pausa = False
    fin = False
    gano = False
    esta_quieto = True
    contador_quieto = 0
    mirando_izquierda = False
    teclas_abajo.clear()
    crear()
    dibujar()


def cargar_cuadros_del_gif(archivo):
    # Carga todos los cuadros de un gif animado, uno por uno
    cuadros = []
    indice = 0
    while True:
        try:
            formato = "gif -index " + str(indice)
            cuadro = PhotoImage(file=archivo, format=formato)
            cuadro = cuadro.zoom(2)
            cuadros.append(cuadro)
            indice = indice + 1
        except TclError:
            break
    return cuadros


# Ventana principal
ventana = Tk()
ventana.title("Pollito Cruzando")
ventana.geometry("800x600")
ventana.resizable(False, False)

c = Canvas(ventana, width=BASE, height=ALTURA)
c.pack()

cuadros_quieto = cargar_cuadros_del_gif("pollito1.gif")
cuadros_quieto_izquierda = cargar_cuadros_del_gif("pollito3.gif")
cuadros_caminando = cargar_cuadros_del_gif("pollito2.gif")
cuadros_caminando_izquierda = cargar_cuadros_del_gif("pollito4.gif")

f = Frame(ventana, bg="black")
f.pack(fill=X)
Label(f, text="Usa las flechas para mover", fg="white", bg="black").pack(side=LEFT, padx=10)
boton = Button(f, text="PAUSAR", command=pausar, width=10)
boton.pack(side=RIGHT)
Button(f, text="REINICIAR", command=reiniciar, width=10).pack(side=RIGHT)
Button(f, text="SALIR", command=ventana.destroy, width=10).pack(side=RIGHT)

ventana.bind("<KeyPress>", tecla_presionada)
ventana.bind("<KeyRelease>", tecla_liberada)

crear()
dibujar()
mover_carros()
animar_pollito()
ventana.mainloop()
