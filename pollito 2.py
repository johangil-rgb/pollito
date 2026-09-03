from tkinter import *
import random

# ===== VARIABLES =====
x=400
y=480
nivel=1
carros=[]
baches=[]

# ===== CREAR =====
def crear():
    global carros,baches
    carros=[]
    baches=[]

    for i in range(6+nivel):
        carros.append([random.randint(0,800),100+(i%4)*100,random.choice([-3-nivel,3+nivel])])

    if nivel>=3:
        for i in range(nivel-2):
            baches.append([random.randint(50,700),random.randint(100,450)])

# ===== MOVER =====
def mover(e):
    global x,y,nivel

    if e.keysym=="Up": y-=20
    if e.keysym=="Down": y+=20
    if e.keysym=="Left": x-=20
    if e.keysym=="Right": x+=20

    if y<=50:
        if nivel<7:
            nivel+=1
            x=400
            y=480
            crear()
        else:
            c.create_text(400,250,text="¡GANASTE!",font=30)

    dibujar()

# ===== DIBUJAR =====
def dibujar():
    c.delete("all")
    c.create_rectangle(0,50,800,490,fill="gray")

    for yy in (150,250,350,450):
        for xx in range(0,800,80):
            c.create_rectangle(xx,yy,xx+40,yy+5,fill="white")

    for a,b in baches:
        c.create_oval(a,b,a+70,b+40,fill="black")

    for a,b,v in carros:
        c.create_rectangle(a,b-15,a+60,b+15,fill="red")
        c.create_oval(a+5,b+10,a+18,b+23,fill="black")
        c.create_oval(a+42,b+10,a+55,b+23,fill="black")

    c.create_oval(x-15,y-10,x+15,y+20,fill="yellow")
    c.create_oval(x-12,y-30,x+12,y,fill="yellow")
    c.create_oval(x-7,y-22,x-2,y-17,fill="black")
    c.create_oval(x+2,y-22,x+7,y-17,fill="black")
    c.create_polygon(x,y-10,x+10,y-5,x,y,fill="orange")

    c.create_text(50,25,text="Nivel "+str(nivel))

# ===== CARROS =====
def mover_carros():
    for a in carros:
        a[0]+=a[2]
        if a[0]>800: a[0]=-60
        if a[0]<-60: a[0]=800
    dibujar()
    ventana.after(50,mover_carros)

# ===== VENTANA =====
ventana=Tk()
ventana.title("Pollito Cruzando")
ventana.geometry("800x550")

c=Canvas(ventana,width=800,height=530)
c.pack()

ventana.bind("<KeyPress>",mover)

crear()
dibujar()
mover_carros()

ventana.mainloop()