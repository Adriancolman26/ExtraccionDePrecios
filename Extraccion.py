from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_dia_products_selenium(duracion_ms=5000):
    print(f"Extrayendo productos de DIA por {duracion_ms} ms con Selenium...")

    options = Options()
    options.add_argument("--headless")  # No abre ventana
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    base_url = "https://diaonline.supermercadosdia.com.ar"
    url = "https://diaonline.supermercadosdia.com.ar/frutos?_q=frutos&map=ft"
    driver.get(url)

    tiempo_limite = time.time() + duracion_ms / 1000.0
    productos = []

    while time.time() < tiempo_limite:
        soup = BeautifulSoup(driver.page_source, "html.parser")

        product_cards = soup.find_all('div', class_='vtex-flex-layout-0-x-flexColChild vtex-flex-layout-0-x-flexColChild--plp_grid pb0')

        for card in product_cards:
            try:
                link = card.find('a', class_='vtex-product-summary-2-x-clearLink')
                if not link:
                    continue

                nombre = link.get_text(strip=True)
                href = link['href']
                url_producto = base_url + href

                precio_span = card.find('span', class_='vtex-product-price-1-x-sellingPrice')
                precio = precio_span.get_text(strip=True) if precio_span else "N/A"

                productos.append({
                    "Supermercado": "DIA",
                    "Producto": nombre,
                    "Precio": precio,
                    "URL": url_producto
                })
            except Exception as e:
                print(f"Error procesando producto: {e}")
                continue

        time.sleep(1)  # Espera un poco entre iteraciones

    driver.quit()
    print(f"Total de productos extraídos: {len(productos)}")
    return productos

def guardar_csv(productos, filename="precios_dia.csv"):
    if not productos:
        print("No se extrajeron productos.")
        return

    df = pd.DataFrame(productos)
    df.drop_duplicates(inplace=True)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"Archivo guardado como {filename} con {len(df)} productos.")

if __name__ == "__main__":
    productos = get_dia_products_selenium(5000)
    guardar_csv(productos)
