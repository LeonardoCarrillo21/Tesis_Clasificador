from tkinter import Tk, Button, Label,BooleanVar, StringVar, IntVar, ttk, Frame, Entry
from PIL import ImageTk, Image
import os
from tkinter.filedialog import askopenfilename,askdirectory
from keysjuntos3 import Keys
# from gen import Generador
from creaBaseDetectores import GeneradorBaseDescriptores
import numpy as np
import cv2
from tratamiento import Tratamiento
from cuadros import Cuadros

class Interfaz:

    def __init__(self):

        self.ventana = Tk()
        self.orb = cv2.ORB_create()
        self.gen = GeneradorBaseDescriptores("baseMomentos.csv",50)
        self.cuadros = Cuadros()
        self.panel3 = Frame(self.ventana, bg="lightgray")#[boton_seleccionar_imagen,boton_seleccionar_carpeta]
        self.panel1 = Frame(self.panel3, bg="lightgray")#[boton_seleccionar_imagen,boton_seleccionar_carpeta]
        self.panel2 = Frame(self.panel3, bg="lightgray")#[boton_seleccionar_imagen,boton_seleccionar_carpeta]
        self.panel4 = Frame(self.ventana, bg="lightgray")#[boton_seleccionar_imagen,boton_seleccionar_carpeta]
        self.ventana.title("Aplicación de Procesamiento de Imágenes")
        self.ventana.geometry("")

        self.imagen_seleccionada = StringVar()
        self.bordes = StringVar()
        self.suavizado_valor = IntVar()
        self.puntos_valor = IntVar()
        self.binarizada_valor = BooleanVar()

        #           panel 4
        #etiqueta de nombre de clase
        self.etiqueta_nombre_clase = Label(self.panel4,text="Nombre Clase: ")
        self.etiqueta_nombre_clase.grid(row=0,column=0)
        # entrada de nombre de clase
        self.entrada_nombre_clase= Entry(self.panel4)
        self.entrada_nombre_clase.insert(0,"botella")
        self.entrada_nombre_clase.grid(row=0,column=1)

        #etiqueta entrada carpeta destino
        self.etiqueta_carpeta_destino = Label(self.panel4,text="Carpeta Destino: ")
        self.etiqueta_carpeta_destino.grid(row=1,column=0)
        # entradas de carpeta destino
        self.entrada_carpeta_destino = Entry(self.panel4,width=60)
        self.entrada_carpeta_destino.insert(0,"Encontrados")
        self.entrada_carpeta_destino.grid(row=1,column=1)
        #boton carpeta destino
        self.boton_seleccionar_carpeta_destino = Button(self.panel4, text="elegir", command=self.seleccionar_carpeta_destino)
        self.boton_seleccionar_carpeta_destino.grid(row=1,column=3)
        self.panel4.pack()

        #       etiqueta de imagen
        self.fondo_blanco = Image.new("RGB", (400, 400), "white")
        #etiqueta imagen
        # self.etiqueta_imagen = Label(self.panel2,text="Imagen")
        # self.etiqueta_imagen.pack()
        #imagen
        self.label_imagen = Label(self.panel2,image=ImageTk.PhotoImage(self.fondo_blanco),text="imagen")
        self.label_imagen.pack()
        self.panel2.grid(row=0,column=0)

        #       panel 1
        #Boton seleccionar Imagen
        self.boton_seleccionar_imagen = Button(self.panel1, text="Seleccionar Imagen", command=self.seleccionar_imagen)
        self.boton_seleccionar_imagen.grid(row=0,column=0,padx=5,pady=10)
        #boton seleccionar carpeta
        self.boton_seleccionar_carpeta = Button(self.panel1, text="Seleccionar Carpeta", command=self.seleccionar_carpeta)
        self.boton_seleccionar_carpeta.grid(row=0,column=1,padx=5,pady=10)

        #etiqueta Canny
        self.etiqueta_borde = Label(self.panel1, text="contorno ")
        self.etiqueta_borde.grid(row=1,column=0,padx=5,pady=10)
        #seleccion de Canny (true,false)
        self.combobox_borde = ttk.Combobox(self.panel1, textvariable=self.bordes)
        self.combobox_borde['values'] = ('canny', 'sobel')
        self.combobox_borde.set('sobel')
        self.combobox_borde.grid(row=1,column=1,padx=5,pady=10)

        #etiqueta suavisado
        self.etiqueta_suavisado = Label(self.panel1, text="suavisado")
        self.etiqueta_suavisado.grid(row=2,column=0,padx=5,pady=10)

        #seleccion suavisado
        self.combobox_suavizado = ttk.Combobox(self.panel1, textvariable=self.suavizado_valor)
        self.combobox_suavizado['values'] = (0, 1, 2, 3)
        self.combobox_suavizado.set(0)
        self.combobox_suavizado.grid(row=2,column=1,padx=5,pady=10)

        #etiqueta puntos de interes
        self.etiqueta_puntos = Label(self.panel1, text="puntos interes")
        self.etiqueta_puntos.grid(row=3,column=0,padx=5,pady=10)
        #seleccion puntos de interes
        self.combobox_puntos = ttk.Combobox(self.panel1, textvariable=self.puntos_valor)
        self.combobox_puntos['values'] = (40, 50,60,100)
        self.combobox_puntos.set(100)
        self.combobox_puntos.grid(row=3,column=1,padx=5,pady=10)

        #etiqueta puntos importantes
        self.etiqueta_binarizada = Label(self.panel1, text="Binarizado")
        self.etiqueta_binarizada.grid(row=4,column=0,padx=5,pady=10)
        #seleccion de puntos importantes
        self.combobox_binarizada = ttk.Combobox(self.panel1, textvariable=self.binarizada_valor)
        self.combobox_binarizada['values'] = ('True','False')
        self.combobox_binarizada.set('True')
        self.combobox_binarizada.grid(row=4,column=1,padx=5,pady=10)
        
        #           Botones
        #boton de iniciar
        self.boton_iniciar = Button(self.panel1, text="Procesar", width=10, height=2,command=self.iniciar_procesamiento)
        self.boton_iniciar.grid(row=5,column=0,padx=5,pady=10)
        #boton de generar Base
        self.boton_gen_base= Button(self.panel1, text="generar base", width=10, height=2,command=self.getBase)
        self.boton_gen_base.grid(row=5,column=1,padx=5,pady=10)
        #boton evaluar_con_Momentos
        self.boton_evaluar_con_momentos= Button(self.panel1, text="evaluar con Momentos", width=20, height=2,command=self.clasificar_con_momentos_de_hu)
        self.boton_evaluar_con_momentos.grid(row=6,column=0,padx=5,pady=10)
        #boton evaluar_con_KeyPoints
        self.boton_evaluar_con_keys= Button(self.panel1, text="evaluar con detectores", width=20, height=2,command=self.clasificar_con_puntos_de_interes)
        self.boton_evaluar_con_keys.grid(row=6,column=1,padx=5,pady=10)
        
        self.panel1.grid(row=0,column=1)
        self.panel3.pack()
        #ejecutar ventana
        self.ventana.mainloop()

    def seleccionar_imagen(self):
        self.ruta = askopenfilename()
        image = Image.open(self.ruta).resize((400,400))  # Reemplaza "ruta_de_la_imagen.jpg" con la ruta de tu imagen
        self.photo = ImageTk.PhotoImage(image)
        self.label_imagen.configure(image=self.photo)
        self.opcion='imagen'

    def seleccionar_carpeta(self):
        self.folder_path = askdirectory()
        self.opcion='carpeta'
    def seleccionar_carpeta_destino(self):
        self.folder_path = askdirectory()
        self.entrada_carpeta_destino.delete(0, 'end')
        self.entrada_carpeta_destino.insert(0,self.folder_path)

    def iniciar_procesamiento(self):
        if self.opcion=='imagen':
            self.individual()
        if self.opcion=='carpeta':
            print(f'opcion {self.opcion}')
            self.varias()

    def individual(self):
        Tratamiento(self.ruta,
             self.combobox_borde.get(),
             int(self.combobox_suavizado.get()),
             self.combobox_binarizada.get(),
             self.entrada_carpeta_destino.get(),
             self.entrada_nombre_clase.get()).tratamiento()

    def buscar(self,ruta):
        for nombre in os.listdir(ruta):
            ruta_com = os.path.join(ruta,nombre)
            esDirectorio = os.path.isdir(ruta_com)
            if not esDirectorio:        
                Keys(self.ruta,
                    self.combobox_canny.get(),
                    int(self.combobox_suavizado.get()),
                    int(self.combobox_puntos.get()),
                    self.combobox_binarizada.get(),
                    self.entrada_carpeta_destino.get(),
                    self.entrada_nombre_clase.get()).circulos()

    def varias(self):
        # Lógica de procesamiento para una carpeta seleccionada
        print(f'en varias()')
        self.buscar(self.folder_path)
    
    def clasificar_con_momentos_de_hu(self):
        recortes = self.cuadros.generadorCuadros(cv2.resize(cv2.imread(self.ruta,0),(400,400)),20)
        # from tensorflow import keras
        # loaded_model = keras.models.load_model("modelo.h5")
        # Cargar solo los pesos del modelo desde un archivo
        # loaded_model.load_weights("pesos.h5")
        
        def clase(arreglo):
            pass

        for recorte in recortes:
            tratado = self.gen.tratamiento(recorte)
            momentos = self.gen.getMomentos(tratado)
            # prediccion = loaded_model.predict([[momentos]])
            # print(prediccion)
            # probabilidad = clase(prediccion)
            print(f'momentos recorte {momentos}')

    def clasificar_con_puntos_de_interes(self):
        _,detectores = self.orb.detectAndCompute(cv2.resize(cv2.imread(self.ruta,0),(400,400)),None)
        if detectores is not None:
            arreglo = [int(valor) for detector in detectores[:50] for valor in detector]
            print(arreglo)
            matriz = np.array(arreglo).reshape(50,32)
            # print(matriz)
            # for renglon in matriz:
            #     print(renglon)
        else:
            print("no es posible trabajar la imagen")

    def getBase(self):
        self.rutaBase= askdirectory()
        if self.rutaBase:
            self.gen.buscar(self.rutaBase,"")
# Crear instancia de la clase Interfaz
interfaz = Interfaz()