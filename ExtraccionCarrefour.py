from bs4 import BeautifulSoup
import pandas as pd

def extract_carrefour_filters_from_html(html_content):
    """
    Extrae marcas y sus conteos de productos de un snippet HTML de filtros de Carrefour.
    """
    print("Extrayendo información de filtros del HTML proporcionado...")
    soup = BeautifulSoup(html_content, "html.parser")
    
    brands_data = []

    # Encontrar el contenedor de filtros de marca
    # El HTML muestra 'valtech-carrefourar-search-result-3-x-filter__container--brand'
    brand_filter_container = soup.find('div', class_='valtech-carrefourar-search-result-3-x-filter__container--brand')

    if brand_filter_container:
        # Encontrar todos los ítems de filtro dentro del contenedor de marcas
        # Los ítems individuales tienen la clase 'vaaltech-carrefourar-search-result-3-x-filterItem'
        # La expresión lambda asegura que se busquen clases que contienen 'valtech-carrefourar-search-result-3-x-filterItem--'
        # pero que NO son la clase genérica 'valtech-carrefourar-search-result-3-x-filterItem--brand'
        filter_items = brand_filter_container.find_all('div', class_=lambda x: x and 'valtech-carrefourar-search-result-3-x-filterItem--' in x and 'valtech-carrefourar-search-result-3-x-filterItem--brand' not in x)

        for item in filter_items:
            try:
                # El nombre de la marca está en la etiqueta <label>
                label = item.find('label', class_='vtex-checkbox__label')
                if label:
                    # Obtener el texto antes del <span> del conteo
                    # Si el span de conteo es el primer o único hijo, contents[0] podría no ser el nombre
                    # Es mejor buscar el texto directamente o iterar en contents
                    brand_name_parts = [c.strip() for c in label.contents if c.name is None]
                    brand_name = " ".join(brand_name_parts).strip()
                    
                    # El conteo de productos está en un <span> con class="valtech-carrefourar-search-result-3-x-productCount"
                    count_span = label.find('span', class_='valtech-carrefourar-search-result-3-x-productCount')
                    product_count = 0
                    if count_span:
                        # Extraer el número entre paréntesis, ej. "(19)" -> 19
                        count_text = count_span.get_text(strip=True)
                        # Usamos list comprehension con isdigit para ser más robustos
                        product_count = int("".join(filter(str.isdigit, count_text))) 

                    brands_data.append({
                        "Marca": brand_name,
                        "Cantidad de Productos": product_count
                    })
            except Exception as e:
                # Imprimir el error y el fragmento del HTML problemático para depuración
                print(f"Error procesando item de marca: {e} en {item.prettify()[:200]}...") # Aumenté a 200 caracteres para más contexto
                continue
    else:
        print("No se encontró el contenedor de filtros de marca en el HTML proporcionado.")

    return brands_data

def save_filters_to_csv(data, filename="carrefour_filtros_marcas.csv"):
    if not data:
        print("No se extrajeron datos de filtros para guardar.")
        return

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"Archivo guardado como '{filename}' con {len(df)} marcas únicas.")

if __name__ == "__main__":
    # El snippet HTML que me proporcionaste, lo pongo en una variable
    html_snippet = """
    <div class="flex mt0 mb0 pt0 pb0 justify-start vtex-flex-layout-0-x-flexRowContent items-stretch w-100">
        <div class="pr0 vtex-flex-layout-0-x-stretchChildrenWidth flex" style="width: 20%;">
            <div class="vtex-flex-layout-0-x-flexCol vtex-flex-layout-0-x-flexCol--filterCol ml0 mr0 pl5 pr5 flex flex-column h-100 w-100">
                <div class="vtex-flex-layout-0-x-flexColChild vtex-flex-layout-0-x-flexColChild--filterCol pb0" style="height: auto;">
                    <div class="valtech-carrefourar-search-result-3-x-filters--layout ">
                        <div class=" valtech-carrefourar-search-result-3-x-filtersWrapper">
                            <div class="valtech-carrefourar-search-result-3-x-filtersContainer">
                                <div class=" valtech-carrefourar-search-result-3-x-filtersWrapper">
                                    <div class="valtech-carrefourar-search-result-3-x-filter__container valtech-carrefourar-search-result-3-x-filter__container--title bb b--muted-4">
                                        <h5 class="valtech-carrefourar-search-result-3-x-filterMessage t-heading-5 mv5">Filtros</h5>
                                        <div class="valtech-carrefourar-search-result-3-x-switchContainer flex flex-row items-center relative">
                                            <input class="valtech-carrefourar-search-result-3-x-switchCheckbox" id="switchNew" type="checkbox">
                                            <label class="valtech-carrefourar-search-result-3-x-switchLabel false" for="switchNew">
                                                <span class="valtech-carrefourar-search-result-3-x-switchButton"></span>
                                            </label>
                                            <span class="valtech-carrefourar-search-result-3-x-switchText false">MARCA CARREFOUR</span>
                                        </div>
                                    </div>
                                    <div class="valtech-carrefourar-search-result-3-x-filter__container bb b--muted-4 valtech-carrefourar-search-result-3-x-filter__container--brand">
                                        <div class="valtech-carrefourar-search-result-3-x-filter pv5 valtech-carrefourar-search-result-3-x-filterAvailable">
                                            <div role="button" tabindex="0" class="pointer outline-0" aria-disabled="false">
                                                <div class="valtech-carrefourar-search-result-3-x-filterTitle">
                                                    <span class="valtech-carrefourar-search-result-3-x-filterTitleSpan">Marca</span>
                                                    <span class="valtech-carrefourar-search-result-3-x-filterIcon flex items-center c-muted-3">
                                                        <svg fill="none" width="14" height="14" viewBox="0 0 16 16" class=" valtech-carrefourar-search-result-3-x-caretIcon" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                                                            <use href="#nav-caret--down" xlink:href="#nav-caret--down"></use>
                                                        </svg>
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="valtech-carrefourar-search-result-3-x-filterTemplateOverflow overflow-y-auto" data-testid="scrollable-element" style="max-height: 200px;" aria-hidden="true">
                                            <div style="overflow: hidden; height: 0px;">
                                                <div class="valtech-carrefourar-search-result-3-x-filterContent">
                                                    <div class="valtech-carrefourar-search-result-3-x-filterItem valtech-carrefourar-search-result-3-x-filterItem--carrefour lh-copy w-100" style="hyphens: auto; word-break: break-word;" alt="Carrefour" title="Carrefour">
                                                        <div class="vtex-checkbox__line-container flex items-start relative pointer">
                                                            <div class="vtex-checkbox__container relative w1 h1 mr3">
                                                                <div class="vtex-checkbox__inner-container h1 w1 absolute ba bw1 br1 b--muted-4 pointer mr3" style="transition: background 20ms, border 100ms;"></div>
                                                                <div class="vtex-checkbox__box-wrapper absolute w1 h1 flex o-100" style="left: 0px;">
                                                                    <div class="vtex-checkbox__box absolute top-0 left-0 bottom-0 overflow-hidden w-100 flex items-center align-center justify-center c-on-action-primary" style="transition: right 110ms ease-in-out 30ms;"></div>
                                                                </div>
                                                                <input class="vtex-checkbox__input h1 w1 absolute o-0 pointer" id="brand-carrefour" name="Carrefour" type="checkbox" tabindex="0" value="Carrefour">
                                                            </div>
                                                            <label class="vtex-checkbox__label w-100 c-on-base pointer" for="brand-carrefour">Carrefour <span data-testid="facet-quantity-carrefour-19" class="valtech-carrefourar-search-result-3-x-productCount">(19)</span></label>
                                                        </div>
                                                    </div>
                                                    <div class="valtech-carrefourar-search-result-3-x-filterItem valtech-carrefourar-search-result-3-x-filterItem--aloha lh-copy w-100" style="hyphens: auto; word-break: break-word;" alt="Aloha" title="Aloha">
                                                        <div class="vtex-checkbox__line-container flex items-start relative pointer">
                                                            <div class="vtex-checkbox__container relative w1 h1 mr3">
                                                                <div class="vtex-checkbox__inner-container h1 w1 absolute ba bw1 br1 b--muted-4 pointer mr3" style="transition: background 20ms, border 100ms;"></div>
                                                                <div class="vtex-checkbox__box-wrapper absolute w1 h1 flex o-100" style="left: 0px;">
                                                                    <div class="vtex-checkbox__box absolute top-0 left-0 bottom-0 overflow-hidden w-100 flex items-center align-center justify-center c-on-action-primary" style="transition: right 110ms ease-in-out 30ms;"></div>
                                                                </div>
                                                                <input class="vtex-checkbox__input h1 w1 absolute o-0 pointer" id="brand-aloha" name="Aloha" type="checkbox" tabindex="0" value="Aloha">
                                                            </div>
                                                            <label class="vtex-checkbox__label w-100 c-on-base pointer" for="brand-aloha">Aloha <span data-testid="facet-quantity-aloha-9" class="valtech-carrefourar-search-result-3-x-productCount">(9)</span></label>
                                                        </div>
                                                    </div>
                                                    <div class="valtech-carrefourar-search-result-3-x-filterItem valtech-carrefourar-search-result-3-x-filterItem--arcor lh-copy w-100" style="hyphens: auto; word-break: break-word;" alt="Arcor" title="Arcor">
                                                        <div class="vtex-checkbox__line-container flex items-start relative pointer">
                                                            <div class="vtex-checkbox__container relative w1 h1 mr3">
                                                                <div class="vtex-checkbox__inner-container h1 w1 absolute ba bw1 br1 b--muted-4 pointer mr3" style="transition: background 20ms, border 100ms;"></div>
                                                                <div class="vtex-checkbox__box-wrapper absolute w1 h1 flex o-100" style="left: 0px;">
                                                                    <div class="vtex-checkbox__box absolute top-0 left-0 bottom-0 overflow-hidden w-100 flex items-center align-center justify-center c-on-action-primary" style="transition: right 110ms ease-in-out 30ms;"></div>
                                                                </div>
                                                                <input class="vtex-checkbox__input h1 w1 absolute o-0 pointer" id="brand-arcor" name="Arcor" type="checkbox" tabindex="0" value="Arcor">
                                                            </div>
                                                            <label class="vtex-checkbox__label w-100 c-on-base pointer" for="brand-arcor">Arcor <span data-testid="facet-quantity-arcor-3" class="valtech-carrefourar-search-result-3-x-productCount">(3)</span></label>
                                                        </div>
                                                    </div>
                                                    <div class="valtech-carrefourar-search-result-3-x-filterItem valtech-carrefourar-search-result-3-x-filterItem--bon-o-bon lh-copy w-100" style="hyphens: auto; word-break: break-word;" alt="Bon O Bon" title="Bon O Bon">
                                                        <div class="vtex-checkbox__line-container flex items-start relative pointer">
                                                            <div class="vtex-checkbox__container relative w1 h1 mr3">
                                                                <div class="vtex-checkbox__inner-container h1 w1 absolute ba bw1 br1 b--muted-4 pointer mr3" style="transition: background 20ms, border 100ms;"></div>
                                                                <div class="vtex-checkbox__box-wrapper absolute w1 h1 flex o-100" style="left: 0px;">
                                                                    <div class="vtex-checkbox__box absolute top-0 left-0 bottom-0 overflow-hidden w-100 flex items-center align-center justify-center c-on-action-primary" style="transition: right 110ms ease-in-out 30ms;"></div>
                                                                </div>
                                                                <input class="vtex-checkbox__input h1 w1 absolute o-0 pointer" id="brand-bon-o-bon" name="Bon O Bon" type="checkbox" tabindex="0" value="Bon O Bon">
                                                            </div>
                                                            <label class="vtex-checkbox__label w-100 c-on-base pointer" for="brand-bon-o-bon">Bon O Bon <span data-testid="facet-quantity-bon-o-bon-2" class="valtech-carrefourar-search-result-3-x-productCount">(2)</span></label>
                                                        </div>
                                                    </div>
                                                    <div class="valtech-carrefourar-search-result-3-x-filterItem valtech-carrefourar-search-result-3-x-filterItem--bulnez lh-copy w-100" style="hyphens: auto; word-break: break-word;" alt="Bulnez" title="Bulnez">
                                                        <div class="vtex-checkbox__line-container flex items-start relative pointer">
                                                            <div class="vtex-checkbox__container relative w1 h1 mr3">
                                                                <div class="vtex-checkbox__inner-container h1 w1 absolute ba bw1 br1 b--muted-4 pointer mr3" style="transition: background 20ms, border 100ms;"></div>
                                                                <div class="vtex-checkbox__box-wrapper absolute w1 h1 flex o-100" style="left: 0px;">
                                                                    <div class="vtex-checkbox__box absolute top-0 left-0 bottom-0 overflow-hidden w-100 flex items-center align-center justify-center c-on-action-primary" style="transition: right 110ms ease-in-out 30ms;"></div>
                                                                </div>
                                                                <input class="vtex-checkbox__input h1 w1 absolute o-0 pointer" id="brand-bulnez" name="Bulnez" type="checkbox" tabindex="0" value="Bulnez">
                                                            </div>
                                                            <label class="vtex-checkbox__label w-100 c-on-base pointer" for="brand-bulnez">Bulnez <span data-testid="facet-quantity-bulnez-8" class="valtech-carrefourar-search-result-3-x-productCount">(8)</span></label>
                                                        </div>
                                                    </div>
                                                    <div class="valtech-carrefourar-search-result-3-x-filterItem valtech-carrefourar-search-result-3-x-filterItem--chocolinas lh-copy w-100" style="hyphens: auto; word-break: break-word;" alt="Chocolinas" title="Chocolinas">
                                                        <div class="vtex-checkbox__line-container flex items-start relative pointer">
                                                            <div class="vtex-checkbox__container relative w1 h1 mr3">
                                                                <div class="vtex-checkbox__inner-container h1 w1 absolute ba bw1 br1 b--muted-4 pointer mr3" style="transition: background 20ms, border 100ms;"></div>
                                                                <div class="vtex-checkbox__box-wrapper absolute w1 h1 flex o-100" style="left: 0px;">
                                                                    <div class="vtex-checkbox__box absolute top-0 left-0 bottom-0 overflow-hidden w-100 flex items-center align-center justify-center c-on-action-primary" style="transition: right 110ms ease-in-out 30ms;"></div>
                                                                </div>
                                                                <input class="vtex-checkbox__input h1 w1 absolute o-0 pointer" id="brand-chocolinas" name="Chocolinas" type="checkbox" tabindex="0" value="Chocolinas">
                                                            </div>
                                                            <label class="vtex-checkbox__label w-100 c-on-base pointer" for="brand-chocolinas">Chocolinas <span data-testid="facet-quantity-chocolinas-2" class="valtech-carrefourar-search-result-3-x-productCount">(2)</span></label>
                                                        </div>
                                                    </div>
                                                    <div class="valtech-carrefourar-search-result-3-x-filterItem valtech-carrefourar-search-result-3-x-filterItem--chomp lh-copy w-100" style="hyphens: auto; word-break: break-word;" alt="Chomp" title="Chomp">
                                                        <div class="vtex-checkbox__line-container flex items-start relative pointer">
                                                            <div class="vtex-checkbox__container relative w1 h1 mr3">
                                                                <div class="vtex-checkbox__inner-container h1 w1 absolute ba bw1 br1 b--muted-4 pointer mr3" style="transition: background 20ms, border 100ms;"></div>
                                                                <div class="vtex-checkbox__box-wrapper absolute w1 h1 flex o-100" style="left: 0px;">
                                                                    <div class="vtex-checkbox__box absolute top-0 left-0 bottom-0 overflow-hidden w-100 flex items-center align-center justify-center c-on-action-primary" style="transition: right 110ms ease-in-out 30ms;"></div>
                                                                </div>
                                                                <input class="vtex-checkbox__input h1 w1 absolute o-0 pointer" id="brand-chomp" name="Chomp" type="checkbox" tabindex="0" value="Chomp">
                                                            </div>
                                                            <label class="vtex-checkbox__label w-100 c-on-base pointer" for="brand-chomp">Chomp <span data-testid="facet-quantity-chomp-1" class="valtech-carrefourar-search-result-3-x-productCount">(1)</span></label>
                                                        </div>
                                                    </div>
                                                    <div class="valtech-carrefourar-search-result-3-x-filterItem valtech-carrefourar-search-result-3-x-filterItem--chungo lh-copy w-100" style="hyphens: auto; word-break: break-word;" alt="Chungo" title="Chungo">
                                                        <div class="vtex-checkbox__line-container flex items-start relative pointer">
                                                            <div class="vtex-checkbox__container relative w1 h1 mr3">
                                                                <div class="vtex-checkbox__inner-container h1 w1 absolute ba bw1 br1 b--muted-4 pointer mr3" style="transition: background 20ms, border 100ms;"></div>
                                                                <div class="vtex-checkbox__box-wrapper absolute w1 h1 flex o-100" style="left: 0px;">
                                                                    <div class="vtex-checkbox__box absolute top-0 left-0 bottom-0 overflow-hidden w-100 flex items-center align-center justify-center c-on-action-primary" style="transition: right 110ms ease-in-out 30ms;"></div>
                                                                </div>
                                                                <input class="vtex-checkbox__input h1 w1 absolute o-0 pointer" id="brand-chungo" name="Chungo" type="checkbox" tabindex="0" value="Chungo">
                                                            </div>
                                                            <label class="vtex-checkbox__label w-100 c-on-base pointer" for="brand-chungo">Chungo <span data-testid="facet-quantity-chungo-3" class="valtech-carrefourar-search-result-3-x-productCount">(3)</span></label>
                                                        </div>
                                                    </div>
                                                    <div class="valtech-carrefourar-search-result-3-x-filterItem valtech-carrefourar-search-result-3-x-filterItem--cofler lh-copy w-100" style="hyphens: auto; word-break: break-word;" alt="Cofler" title="Cofler">
                                                        <div class="vtex-checkbox__line-container flex items-start relative pointer">
                                                            <div class="vtex-checkbox__container relative w1 h1 mr3">
                                                                <div class="vtex-checkbox__inner-container h1 w1 absolute ba bw1 br1 b--muted-4 pointer mr3" style="transition: background 20ms, border 100ms;"></div>
                                                                <div class="vtex-checkbox__box-wrapper absolute w1 h1 flex o-100" style="left: 0px;">
                                                                    <div class="vtex-checkbox__box absolute top-0 left-0 bottom-0 overflow-hidden w-100 flex items-center align-center justify-center c-on-action-primary" style="transition: right 110ms ease-in-out 30ms;"></div>
                                                                </div>
                                                                <input class="vtex-checkbox__input h1 w1 absolute o-0 pointer" id="brand-cofler" name="Cofler" type="checkbox" tabindex="0" value="Cofler">
                                                            </div>
                                                            <label class="vtex-checkbox__label w-100 c-on-base pointer" for="brand-cofler">Cofler <span data-testid="facet-quantity-cofler-3" class="valtech-carrefourar-search-result-3-x-productCount">(3)</span></label>
                                                        </div>
                                                    </div>
                                                    <div class="valtech-carrefourar-search-result-3-x-filterItem valtech-carrefourar-search-result-3-x-filterItem--dinamita lh-copy w-100" style="hyphens: auto; word-break: break-word;" alt="Dinamita" title="Dinamita">
                                                        <div class="vtex-checkbox__line-container flex items-start relative pointer">
                                                            <div class="vtex-checkbox__container relative w1 h1 mr3">
                                                                <div class="vtex-checkbox__inner-container h1 w1 absolute ba bw1 br1 b--muted-4 pointer mr3" style="transition: background 20ms, border 100ms;"></div>
                                                                <div class="vtex-checkbox__box-wrapper absolute w1 h1 flex o-100" style="left: 0px;">
                                                                    <div class="vtex-checkbox__box absolute top-0 left-0 bottom-0 overflow-hidden w-100 flex items-center align-center justify-center c-on-action-primary" style="transition: right 110ms ease-in-out 30ms;"></div>
                                                                </div>
                                                                <input class="vtex-checkbox__input h1 w1 absolute o-0 pointer" id="brand-dinamita" name="Dinamita" type="checkbox" tabindex="0" value="Dinamita">
                                                            </div>
                                                            <label class="vtex-checkbox__label w-100 c-on-base pointer" for="brand-dinamita">Dinamita <span data-testid="facet-quantity-dinamita-1" class="valtech-carrefourar-search-result-3-x-productCount">(1)</span></label>
                                                        </div>
                                                    </div>
                                                    <div class="valtech-carrefourar-search-result-3-x-filterItem valtech-carrefourar-search-result-3-x-filterItem--epa lh-copy w-100" style="hyphens: auto; word-break: break-word;" alt="Epa" title="Epa">
                                                        <div class="vtex-checkbox__line-container flex items-start relative pointer">
                                                            <div class="vtex-checkbox__container relative w1 h1 mr3">
                                                                <div class="vtex-checkbox__inner-container h1 w1 absolute ba bw1 br1 b--muted-4 pointer mr3" style="transition: background 20ms, border 100ms;"></div>
                                                                <div class="vtex-checkbox__box-wrapper absolute w1 h1 flex o-100" style="left: 0px;">
                                                                    <div class="vtex-checkbox__box absolute top-0 left-0 bottom-0 overflow-hidden w-100 flex items-center align-center justify-center c-on-action-primary" style="transition: right 110ms ease-in-out 30ms;"></div>
                                                                </div>
                                                                <input class="vtex-checkbox__input h1 w1 absolute o-0 pointer" id="brand-epa" name="Epa" type="checkbox" tabindex="0" value="Epa">
                                                            </div>
                                                            <label class="vtex-checkbox__label w-100 c-on-base pointer" for="brand-epa">Epa <span data-testid="facet-quantity-epa-2" class="valtech-carrefourar-search-result-3-x-productCount">(2)</span></label>
                                                        </div>
                                                    </div>
                                                    <div class="valtech-carrefourar-search-result-3-x-filterItem valtech-carrefourar-search-result-3-x-filterItem--eskimo lh-copy w-100" style="hyphens: auto; word-break: break-word;" alt="Eskimo" title="Eskimo">
                                                        <div class="vtex-checkbox__line-container flex items-start relative pointer">
                                                            <div class="vtex-checkbox__container relative w1 h1 mr3">
                                                                <div class="vtex-checkbox__inner-container h1 w1 absolute ba bw1 br1 b--muted-4 pointer mr3" style="transition: background 20ms, border 100ms;"></div>
                                                                <div class="vtex-checkbox__box-wrapper absolute w1 h1 flex o-100" style="left: 0px;">
                                                                    <div class="vtex-checkbox__box absolute top-0 left-0 bottom-0 overflow-hidden w-100 flex items-center align-center justify-center c-on-action-primary" style="transition: right 110ms ease-in-out 30ms;"></div>
                                                                </div>
                                                                <input class="vtex-checkbox__input h1 w1 absolute o-0 pointer" id="brand-eskimo" name="Eskimo" type="checkbox" tabindex="0" value="Eskimo">
                                                            </div>
                                                            <label class="vtex-checkbox__label w-100 c-on-base pointer" for="brand-eskimo">Eskimo <span data-testid="facet-quantity-eskimo-1" class="valtech-carrefourar-search-result-3-x-productCount">(1)</span></label>
                                                        </div>
                                                    </div>
                                                    <div class="valtech-carrefourar-search-result-3-x-filterItem valtech-carrefourar-search-result-3-x-filterItem--franui lh-copy w-100" style="hyphens: auto; word-break: break-word;" alt="Franui" title="Franui">
                                                        <div class="vtex-checkbox__line-container flex items-start relative pointer">
                                                            <div class="vtex-checkbox__container relative w1 h1 mr3">
                                                                <div class="vtex-checkbox__inner-container h1 w1 absolute ba bw1 br1 b--muted-4 pointer mr3" style="transition: background 20ms, border 100ms;"></div>
                                                                <div class="vtex-checkbox__box-wrapper absolute w1 h1 flex o-100" style="left: 0px;">
                                                                    <div class="vtex-checkbox__box absolute top-0 left-0 bottom-0 overflow-hidden w-100 flex items-center align-center justify-center c-on-action-primary" style="transition: right 110ms ease-in-out 30ms;"></div>
                                                                </div>
                                                                <input class="vtex-checkbox__input h1 w1 absolute o-0 pointer" id="brand-franui" name="Franui" type="checkbox" tabindex="0" value="Franui">
                                                            </div>
                                                            <label class="vtex-checkbox__label w-100 c-on-base pointer" for="brand-franui">Franui <span data-testid="facet-quantity-franui-1" class="valtech-carrefourar-search-result-3-x-productCount">(1)</span></label>
                                                        </div>
                                                    </div>
                                                    <div class="valtech-carrefourar-search-result-3-x-filterItem valtech-carrefourar-search-result-3-x-filterItem--freddo lh-copy w-100" style="hyphens: auto; word-break: break-word;" alt="Freddo" title="Freddo">
                                                        <div class="vtex-checkbox__line-container flex items-start relative pointer">
                                                            <div class="vtex-checkbox__container relative w1 h1 mr3">
                                                                <div class="vtex-checkbox__inner-container h1 w1 absolute ba bw1 br1 b--muted-4 pointer mr3" style="transition: background 20ms, border 100ms;"></div>
                                                                <div class="vtex-checkbox__box-wrapper absolute w1 h1 flex o-100" style="left: 0px;">
                                                                    <div class="vtex-checkbox__box absolute top-0 left-0 bottom-0 overflow-hidden w-100 flex items-center align-center justify-center c-on-action-primary" style="transition: right 110ms ease-in-out 30ms;"></div>
                                                                </div>
    """ # Se corta aquí, ya que el original también se cortó

    # Ejecutar la función de extracción
    extracted_data = extract_carrefour_filters_from_html(html_snippet)

    # Guardar los datos extraídos en un archivo CSV
    save_filters_to_csv(extracted_data)

    # Opcional: imprimir los datos extraídos para verificar
    if extracted_data:
        print("\nDatos extraídos:")
        for entry in extracted_data:
            print(f"- Marca: {entry['Marca']}, Cantidad: {entry['Cantidad de Productos']}")