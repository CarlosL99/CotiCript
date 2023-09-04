from playwright.sync_api import sync_playwright
import time
import tkinter as tk
from tkinter import Scrollbar
from PIL import Image, ImageTk
from io import BytesIO
import requests


def clear_window_content(root):
    for widget in root.winfo_children():
        widget.destroy()


def update_content():
    clear_window_content(root)
    with sync_playwright() as p:
        # Establecelo en true si no quieres ver la ventana del navegador
        browser = p.firefox.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://coinmarketcap.com/es/")
        # page.goto("https://www.google.com/")

        # Pausa para que la página se cargue completamente
        # time.sleep(5)

        scroll_height = page.evaluate("document.body.scrollHeight;")
        current_scroll = 0
        while current_scroll < scroll_height:
            page.evaluate(f"window.scrollTo(0, {current_scroll});")
            time.sleep(1)  # Pausa ir cargando contenido
            current_scroll += 300  # Ajusta la cantidad de desplazamiento

        imagenes = page.query_selector_all(
            "html body.DAY div#__next div.sc-5909f15e-1.bGBEnA div.main-content div.cmc-body-wrapper div.grid div div.sc-b28ea1c6-2.kaxzEy table.sc-b28ea1c6-3.izgIsg.cmc-table tbody tr td div.sc-aef7b723-0.LCOyB a.cmc-link div.sc-aef7b723-0.sc-b585f443-0.hqAcrb img.coin-logo")

        src_imagenes = [imagen.get_attribute("src") for imagen in imagenes]

        nombre_monedas = page.query_selector_all(
            "html body.DAY div#__next div.sc-5909f15e-1.bGBEnA div.main-content div.cmc-body-wrapper div.grid div div.sc-b28ea1c6-2.kaxzEy table.sc-b28ea1c6-3.izgIsg.cmc-table tbody tr td div.sc-aef7b723-0.LCOyB a.cmc-link div.sc-aef7b723-0.sc-b585f443-0.hqAcrb div.sc-aef7b723-0.sc-b585f443-1.dUXsZC.hide-ranking-number p.sc-4984dd93-0.kKpPOn")

        nombres = [nombre.inner_text() for nombre in nombre_monedas]

        simbolos_monedas = page.query_selector_all(
            "html body.DAY div#__next div.sc-5909f15e-1.bGBEnA div.main-content div.cmc-body-wrapper div.grid div div.sc-b28ea1c6-2.kaxzEy table.sc-b28ea1c6-3.izgIsg.cmc-table tbody tr td div.sc-aef7b723-0.LCOyB a.cmc-link div.sc-aef7b723-0.sc-b585f443-0.hqAcrb div.sc-aef7b723-0.sc-b585f443-1.dUXsZC.hide-ranking-number div.sc-b585f443-2.SoolS p.sc-4984dd93-0.iqdbQL.coin-item-symbol")

        simbolos = [simbolo.inner_text() for simbolo in simbolos_monedas]

        Precios_monedas = page.query_selector_all(
            "html body.DAY div#__next div.sc-5909f15e-1.bGBEnA div.main-content div.cmc-body-wrapper div.grid div div.sc-b28ea1c6-2.kaxzEy table.sc-b28ea1c6-3.izgIsg.cmc-table tbody tr td div.sc-a0353bbc-0.gDrtaY a.cmc-link span")
        # Revisa porque debido a q precio
        # tiene un color la clase del div ademas
        # de sc- y los numeros se te agrega otra segun el color
        # debes sacarla y dejar solo sc-

        precios = [precio.inner_text() for precio in Precios_monedas]

        Capitalización_Monedas = page.query_selector_all(
            "html body.DAY div#__next div.sc-5909f15e-1.bGBEnA div.main-content div.cmc-body-wrapper div.grid div div.sc-b28ea1c6-2.kaxzEy table.sc-b28ea1c6-3.izgIsg.cmc-table tbody tr td p.sc-4984dd93-0.jZrMxO span.sc-f8982b1f-1.bOsKfy")

        CapMonedas = [Cap_Moneda.inner_text()
                      for Cap_Moneda in Capitalización_Monedas]

        Variaciones_monedas = page.query_selector_all(
            "html body.DAY div#__next div.sc-5909f15e-1.bGBEnA div.main-content div.cmc-body-wrapper div.grid div div.sc-b28ea1c6-2.kaxzEy table.sc-b28ea1c6-3.izgIsg.cmc-table tbody tr td span.sc-d55c02b-0")
        # Aqui en variaciones sucede lo mismo q precio al
        # final solo deja sc- y el numero no pegues la clase q sigue

        variaciones = [variacion.inner_text()
                       for variacion in Variaciones_monedas]

        lista_colores = []

        # Obtener los colores de las variaciones q son las 300
        for span_element in Variaciones_monedas:
            color = span_element.evaluate(
                '(element) => getComputedStyle(element).color')
            lista_colores.append(color)

        if nombres and src_imagenes and simbolos and precios and CapMonedas and lista_colores:
            print("Cotizaciones Capturadas")
        else:
            print("Las clases Cambiaron")

        browser.close()

        def center_window(window, width, height):
            # Obtiene el ancho y alto de la pantalla
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()

            # Calcula las coordenadas X e Y para centrar la ventana
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2

            # Ubica la ventana en el centro de la pantalla
            window.geometry(f"{width}x{height}+{x}+{y}")

        def rgb_to_hex(rgb):
            r, g, b = map(int, rgb[4:-1].split(','))
            return f'#{r:02x}{g:02x}{b:02x}'

        center_window(root, width, height)

        # Título encima de la grilla
        titulo_label = tk.Label(
            root, text="Cotización de Criptomonedas", font=("Helvetica", 16, "bold"))
        titulo_label.pack(pady=10)

        # Marco Todo Contenido
        marco_contenido = tk.Frame(root)
        marco_contenido.pack(fill=tk.BOTH)

        # Marco Titulos
        marco_titulos = tk.Frame(marco_contenido)
        marco_titulos.pack(fill=tk.X, expand=True)

        Titulos = ["TOP", "Nombre", "Simbolo", "Precio",
                   "1h", "24h", "7dias", "Capital de Mercado"]

        for i, titulo in enumerate(Titulos):

            if titulo == "TOP" or titulo == "Capital de Mercado":
                tk.Label(marco_titulos, text=titulo).grid(
                    row=0, column=i * 2, padx=(10, 30), pady=20)
            elif titulo == "Nombre":
                tk.Label(marco_titulos, text=titulo).grid(
                    row=0, column=i * 2, padx=(180, 20), pady=20)
            elif titulo == "Simbolo":
                tk.Label(marco_titulos, text=titulo).grid(
                    row=0, column=i * 2, padx=(30, 20), pady=20)
            elif titulo == "Precio":
                tk.Label(marco_titulos, text=titulo).grid(
                    row=0, column=i * 2, padx=(45, 20), pady=20)
            elif titulo == "1h" or "24h" or "7dias":
                tk.Label(marco_titulos, text=titulo).grid(
                    row=0, column=i * 2, padx=(40, 20), pady=20)
            else:
                tk.Label(marco_titulos, text=titulo).grid(
                    row=0, column=i * 2, padx=20, pady=20)

            # Agrega línea vertical
            separator_vertical = tk.Frame(
                marco_titulos, height=0, width=0)
            separator_vertical.grid(row=0, column=(i * 2) + 1, padx=0, pady=0)
            separator_vertical.config(background="")

        # Agrega línea horizontal
        separator_horizontal = tk.Frame(
            marco_titulos, height=2, width=200, background='black')
        separator_horizontal.grid(
            row=(i * 2) + 1, columnspan=15, sticky="ew")

        # Barra de scroll vertical
        scrollbar = tk.Scrollbar(marco_contenido, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Lienzo para todo el contenido con la barra de scroll
        lienzo = tk.Canvas(marco_contenido, yscrollcommand=scrollbar.set)
        lienzo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configurar la barra de scroll
        scrollbar.config(command=lienzo.yview)

        # Marco que contiene todo
        marco_interior = tk.Frame(lienzo)
        lienzo.create_window((0, 0), window=marco_interior, anchor=tk.NW)

        # * Para las variaciones y colores
        count = 0
        #  *********

        for i, (nombre, url_imagen, simbolo, precio, CapMoneda) in enumerate(zip(nombres, src_imagenes, simbolos, precios, CapMonedas)):

            imagen_response = requests.get(url_imagen)
            imagen_bytes = BytesIO(imagen_response.content)
            imagen = Image.open(imagen_bytes)
            imagen = imagen.resize((64, 64))  # Redimensionar la imagen
            imagen_tk = ImageTk.PhotoImage(imagen)

            label_Top = tk.Label(marco_interior, text=i + 1)
            label_Top.grid(row=i * 2, column=0, padx=10, pady=0)

            # Agrega línea vertical
            separator_vertical = tk.Frame(
                marco_interior, height=50, background='black')
            separator_vertical.grid(row=i * 2, column=1, padx=20, pady=0)

            label_imagen = tk.Label(marco_interior, image=imagen_tk)
            label_imagen.image = imagen_tk
            label_imagen.grid(row=i * 2, column=2, padx=20, pady=0)

            label_titulo = tk.Label(marco_interior, text=nombre)
            label_titulo.grid(row=i * 2, column=3, padx=20, pady=0)

            label_simbolo = tk.Label(marco_interior, text=simbolo)
            label_simbolo.grid(row=i * 2, column=4, padx=20, pady=0)

            label_precio = tk.Label(marco_interior, text=precio)
            label_precio.grid(row=i * 2, column=5, padx=20, pady=0)

            # Variaciones //////////////////////
            for j in range(3):

                color_rgb = lista_colores[count]
                label_variacion = tk.Label(
                    marco_interior, text=variaciones[count])
                label_variacion.grid(row=i * 2, column=6 + j,
                                     padx=20, pady=0)

                # Usa la función rgb_to_hex que definiste antes
                color_hex = rgb_to_hex(color_rgb)

                label_variacion.config(fg=color_hex)

                count += 1
            # //////////////////////////////

            label_CapMoneda = tk.Label(marco_interior, text=CapMoneda)
            label_CapMoneda.grid(row=i * 2, column=9, padx=20, pady=0)

            # Agrega línea horizontal
            separator_horizontal = tk.Frame(
                marco_interior, height=2, width=200, background='black')
            separator_horizontal.grid(
                row=(i * 2) + 1, columnspan=10, sticky="ew")

        # Configurar el área de desplazamiento del lienzo
        marco_interior.update_idletasks()
        lienzo.config(scrollregion=lienzo.bbox("all"))

        root.after(60000, update_content)


root = tk.Tk()
root.title("Cotizacion de las CriptoMonedas")
width = 950
height = 400

update_content()

root.mainloop()
