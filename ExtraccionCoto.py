from bs4 import BeautifulSoup
import pandas as pd


def extract_products_from_html(html_content):
   """
   Extrae información de productos (nombre, precio, URL) de un fragmento HTML dado.
   """
   soup = BeautifulSoup(html_content, 'html.parser')
   products_data = []


   # El contenedor principal de los productos es 'div.productos.row'
   # Dentro de este, cada producto individual está en 'div.producto-card'
   product_cards = soup.find_all('div', class_='producto-card')


   base_url = "https://www.cotodigital3.com.ar" # Necesario para construir la URL completa


   for card in product_cards:
       try:
           # Extraer el nombre del producto
           name_tag = card.find('h3', class_='nombre-producto')
           name = name_tag.get_text(strip=True) if name_tag else "N/A"


           # Extraer el precio
           price_tag = card.find('h4', class_='card-title')
           price = price_tag.get_text(strip=True) if price_tag else "N/A"


           # Extraer la URL
           link_tag = card.find('a', class_='d-flex justify-content-end')
           href = link_tag.get('href') if link_tag else None
           full_url = base_url + href.split('?')[0] if href else "N/A"


           products_data.append({
               "Supermercado": "Coto",
               "Producto": name,
               "Precio": price,
               "URL": full_url
           })
       except Exception as e:
           print(f"Error procesando una tarjeta de producto: {e}")
           continue


   return products_data


def save_to_csv(data, filename="productos_extraidos.csv"):
   """
   Guarda la lista de diccionarios en un archivo CSV.
   """
   if data:
       df = pd.DataFrame(data)
       df.to_csv(filename, index=False, encoding='utf-8-sig')
       print(f"Datos guardados exitosamente en '{filename}'.")
   else:
       print("No hay datos para guardar.")


if __name__ == "__main__":
   # ¡Aquí está la corrección! Tu HTML ahora está envuelto en comillas triples.
   # Esto soluciona el error de sintaxis causado por las comillas dobles internas.
   html_sample = """
<div _ngcontent-ord-c120="" class="productos row"><div _ngcontent-ord-c120="" class="col-xl-4 col-lg-4 col-md-6 col-sm-6 col-xs-12 mb-4 producto-card ng-star-inserted"><catalogue-product _ngcontent-ord-c120="" _nghost-ord-c119=""><div _ngcontent-ord-c119="" class="card-container"><div _ngcontent-ord-c119="" class="d-flex justify-content-between top-imagen-promos"><div _ngcontent-ord-c119="" class="d-flex justify-content-start promos"><span _ngcontent-ord-c119="" class="cucarda-promo oferta ng-star-inserted">LLEVANDO 2</span><span _ngcontent-ord-c119="" class="cucarda-promo x-cantidad ng-star-inserted">70% 2DA</span></div><a _ngcontent-ord-c119="" class="d-flex justify-content-end" href="/sitios/cdigi/productos/papas-fritas-crema-y-cebolla-saladix-58-grm/_/R-00543292-00543292-200%3FDy%3D1&amp;"><img _ngcontent-ord-c119="" class="product-image" title="Papas Fritas Crema Y Cebolla Saladix 58 Grm" alt="Papas Fritas Crema Y Cebolla Saladix 58 Grm" src="https://static.cotodigital3.com.ar/sitios/fotos/large/00543200/00543292.jpg"></a></div><div _ngcontent-ord-c119="" class="centro-precios"><h3 _ngcontent-ord-c119="" class="nombre-producto cursor-pointer">Papas Fritas Crema Y Cebolla Saladix 58 Grm</h3><small _ngcontent-ord-c119="" class="offer-crum ng-star-inserted"> PRECIO CON 70% 2DA </small><h4 _ngcontent-ord-c119="" class="card-title text-center mt-1 m-0 p-0 ng-star-inserted"> $1.299,99 </h4><div _ngcontent-ord-c119="" class="d-flex flex-column align-items-center ng-star-inserted"><small _ngcontent-ord-c119="" class="card-text d-block ng-star-inserted"> Precio Regular: $1.999,99 </small><small _ngcontent-ord-c119="" class="text-center"> Precio sin impuestos nacionales: $1.652,88 </small></div><div _ngcontent-ord-c119="" class="w-100 ng-star-inserted"></div><div _ngcontent-ord-c119="" class="text-center ng-star-inserted"><small _ngcontent-ord-c119="" class="card-text mt-1 mb-1 d-block ng-star-inserted"> Precio por 1 Kilo : $34.482,58 </small></div><div _ngcontent-ord-c119="" class="bottom-botones ng-star-inserted"><product-add-show-remove _ngcontent-ord-c119="" class="w-100" _nghost-ord-c103=""><div _ngcontent-ord-c103="" class="row d-flex ps-3"><div _ngcontent-ord-c103="" class="col ng-star-inserted"><button _ngcontent-ord-c103="" href="javascript:void(0);" class="btn btn-primary w-100 px-2 sizePcMedium"> Agregar </button></div></div></product-add-show-remove><a _ngcontent-ord-c119="" href="javascript:void(0)" class="fs-6"> Ver planes de cuotas </a></div></div></div></catalogue-product></div><div _ngcontent-ord-c120="" class="col-xl-4 col-lg-4 col-md-6 col-sm-6 col-xs-12 mb-4 producto-card ng-star-inserted"><catalogue-product _ngcontent-ord-c120="" _nghost-ord-c119=""><div _ngcontent-ord-c119="" class="card-container"><div _ngcontent-ord-c119="" class="d-flex justify-content-between top-imagen-promos"><div _ngcontent-ord-c119="" class="d-flex justify-content-start promos"><span _ngcontent-ord-c119="" class="cucarda-promo oferta ng-star-inserted">LLEVANDO 2</span><span _ngcontent-ord-c119="" class="cucarda-promo x-cantidad ng-star-inserted">70% 2DA</span></div><a _ngcontent-ord-c119="" class="d-flex justify-content-end" href="/sitios/cdigi/productos/papas-fritas-crema-y-cebolla-saladix-95-grm/_/R-00503763-00503763-200%3FDy%3D1&amp;"><img _ngcontent-ord-c119="" class="product-image" title="Papas Fritas Crema Y Cebolla SALADIX 95 Grm" alt="Papas Fritas Crema Y Cebolla SALADIX 95 Grm" src="https://static.cotodigital3.com.ar/sitios/fotos/large/00503700/00503763.jpg"></a></div><div _ngcontent-ord-c119="" class="centro-precios"><h3 _ngcontent-ord-c119="" class="nombre-producto cursor-pointer">Papas Fritas Crema Y Cebolla SALADIX 95 Grm</h3><small _ngcontent-ord-c119="" class="offer-crum ng-star-inserted"> PRECIO CON 70% 2DA </small><h4 _ngcontent-ord-c119="" class="card-title text-center mt-1 m-0 p-0 ng-star-inserted"> $1.711,44 </h4><div _ngcontent-ord-c119="" class="d-flex flex-column align-items-center ng-star-inserted"><small _ngcontent-ord-c119="" class="card-text d-block ng-star-inserted"> Precio Regular: $2.632,99 </small><small _ngcontent-ord-c119="" class="text-center"> Precio sin impuestos nacionales: $2.176,02 </small></div><div _ngcontent-ord-c119="" class="w-100 ng-star-inserted"></div><div _ngcontent-ord-c119="" class="text-center ng-star-inserted"><small _ngcontent-ord-c119="" class="card-text mt-1 mb-1 d-block ng-star-inserted"> Precio por 1 Kilo : $27.715,68 </small></div><div _ngcontent-ord-c119="" class="bottom-botones ng-star-inserted"><product-add-show-remove _ngcontent-ord-c119="" class="w-100" _nghost-ord-c103=""><div _ngcontent-ord-c103="" class="row d-flex ps-3"><div _ngcontent-ord-c103="" class="col ng-star-inserted"><button _ngcontent-ord-c103="" href="javascript:void(0);" class="btn btn-primary w-100 px-2 sizePcMedium"> Agregar </button></div></div></product-add-show-remove><a _ngcontent-ord-c119="" href="javascript:void(0)" class="fs-6"> Ver planes de cuotas </a></div></div></div></catalogue-product></div><div _ngcontent-ord-c120="" class="col-xl-4 col-lg-4 col-md-6 col-sm-6 col-xs-12 mb-4 producto-card ng-star-inserted"><catalogue-product _ngcontent-ord-c120="" _nghost-ord-c119=""><div _ngcontent-ord-c119="" class="card-container"><div _ngcontent-ord-c119="" class="d-flex justify-content-between top-imagen-promos"><div _ngcontent-ord-c119="" class="d-flex justify-content-start promos"><span _ngcontent-ord-c119="" class="cucarda-promo oferta ng-star-inserted">LLEVANDO 2</span><span _ngcontent-ord-c119="" class="cucarda-promo x-cantidad ng-star-inserted">70% 2DA</span></div><a _ngcontent-ord-c119="" class="d-flex justify-content-end" href="/sitios/cdigi/productos/papas-fritas-saladix-original-65g/_/R-00289031-00289031-200%3FDy%3D1&amp;"><img _ngcontent-ord-c119="" class="product-image" title="Papas Fritas SALADIX Original 65g" alt="Papas Fritas SALADIX Original 65g" src="https://static.cotodigital3.com.ar/sitios/fotos/large/00289000/00289031.jpg"></a></div><div _ngcontent-ord-c119="" class="centro-precios"><h3 _ngcontent-ord-c119="" class="nombre-producto cursor-pointer">Papas Fritas SALADIX Original 65g</h3><small _ngcontent-ord-c119="" class="offer-crum ng-star-inserted"> PRECIO CON 70% 2DA </small><h4 _ngcontent-ord-c119="" class="card-title text-center mt-1 m-0 p-0 ng-star-inserted"> $1.411,80 </h4><div _ngcontent-ord-c119="" class="d-flex flex-column align-items-center ng-star-inserted"><small _ngcontent-ord-c119="" class="card-text d-block ng-star-inserted"> Precio Regular: $2.172,00 </small><small _ngcontent-ord-c119="" class="text-center"> Precio sin impuestos nacionales: $1.795,04 </small></div><div _ngcontent-ord-c119="" class="w-100 ng-star-inserted"></div><div _ngcontent-ord-c119="" class="text-center ng-star-inserted"><small _ngcontent-ord-c119="" class="card-text mt-1 mb-1 d-block ng-star-inserted"> Precio por 1 Kilo : $21.720,00 </small></div><div _ngcontent-ord-c119="" class="bottom-botones ng-star-inserted"><product-add-show-remove _ngcontent-ord-c119="" class="w-100" _nghost-ord-c103=""><div _ngcontent-ord-c103="" class="row d-flex ps-3"><div _ngcontent-ord-c103="" class="col ng-star-inserted"><button _ngcontent-ord-c103="" href="javascript:void(0);" class="btn btn-primary w-100 px-2 sizePcMedium"> Agregar </button></div></div></product-add-show-remove><a _ngcontent-ord-c119="" href="javascript:void(0)" class="fs-6"> Ver planes de cuotas </a></div></div></div></catalogue-product></div></div>
   """


   # Extraer los datos de los productos
   products = extract_products_from_html(html_sample)


   # Guardar los datos en un archivo CSV
   save_to_csv(products, "productos_coto.csv")


   # Opcional: Imprimir los
