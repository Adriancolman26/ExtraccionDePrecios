from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time


def get_dia_products_selenium(duracion_ms=8000):
   print(f"Extrayendo productos de DIA por {duracion_ms / 1000} segundos con Selenium...")


   options = Options()
   options.add_argument("--headless")  # No abre ventana del navegador
   options.add_argument("--disable-gpu")
   driver = webdriver.Chrome(options=options) # Cambié 'navegador' a 'driver' para consistencia con el resto del código


   base_url = "https://diaonline.supermercadosdia.com.ar"
   url = "https://diaonline.supermercadosdia.com.ar/frutos?_q=frutos&map=ft"
   driver.get(url)


   tiempo_limite = time.time() + duracion_ms / 1000.0
   productos = []
   productos_urls_vistos = set() # Para evitar duplicados si los productos se repiten en el scraping


   while time.time() < tiempo_limite:
       soup = BeautifulSoup(driver.page_source, "html.parser")


       # --- CORRECCIÓN 1: Selector para la tarjeta de producto ---
       # Basado en el HTML proporcionado, la sección que contiene un producto completo
       # parece ser 'section' con las clases de 'vtex-product-summary-2-x-container'
       product_cards = soup.find_all('section', class_='vtex-product-summary-2-x-container')


       if not product_cards:
           print("No se encontraron tarjetas de productos con el selector actual. Verificando...")
           # Puedes agregar aquí un print de driver.page_source para depurar
           # o intentar otros selectores si el sitio cambió.
           break # Sale del bucle si no encuentra tarjetas


       for card in product_cards:
           try:
               # El enlace contiene el nombre del producto y la URL relativa
               link = card.find('a', class_='vtex-product-summary-2-x-clearLink')
               if not link:
                   continue


               nombre = link.get_text(strip=True)
               href = link['href']
               url_producto = base_url + href


               # Evitar duplicados si ya hemos procesado esta URL de producto
               if url_producto in productos_urls_vistos:
                   continue
               productos_urls_vistos.add(url_producto)


               # --- CORRECCIÓN 2: Selector para el precio ---
               # Basado en el HTML proporcionado, la clase del span del precio es 'diaio-store-5-x-sellingPriceValue'
               precio_span = card.find('span', class_='diaio-store-5-x-sellingPriceValue')
               precio = precio_span.get_text(strip=True) if precio_span else "N/A"


               productos.append({
                   "Supermercado": "DIA",
                   "Producto": nombre,
                   "Precio": precio,
                   "URL": url_producto
               })
           except Exception as e:
               # Puedes hacer este print más detallado para ver qué tarjeta falló
               # print(f"Error procesando tarjeta de producto (posiblemente falta elemento): {e} en tarjeta {card.prettify()[:200]}...")
               print(f"Error procesando producto: {e}")
               continue


       # Aquí podrías simular scroll para cargar más productos si la página es infinita
       # Por ejemplo: driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
       time.sleep(1)  # Espera un poco entre iteraciones para no sobrecargar el servidor


   driver.quit()
   print(f"Total de productos extraídos: {len(productos)}")
   return productos


def guardar_csv(productos, filename="precios_dia.csv"):
   if not productos:
       print("No se extrajeron productos para guardar.")
       return


   df = pd.DataFrame(productos)
   # drop_duplicates en el DataFrame es una buena medida, pero la verificación por URL en el scraping es más rápida
   df.drop_duplicates(subset=['URL'], inplace=True) # Mejor duplicados por URL para mayor precisión
   df.to_csv(filename, index=False, encoding='utf-8-sig')
   print(f"Archivo guardado como '{filename}' con {len(df)} productos únicos.")


if __name__ == "__main__":
   # La duración de 10000 ms (10 segundos) puede que no sea suficiente para cargar muchos productos
   # Considera aumentarla o implementar un scroll dinámico si la página carga más contenido al bajar
   productos_extraidos = get_dia_products_selenium(8000)
   guardar_csv(productos_extraidos)
