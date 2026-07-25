from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import time
import re
import os
import requests


# =====================================================
# CONFIGURACIÓN
# =====================================================

dominio = "https://www.cedarlng.com"

pendientes = [
    dominio
]

visitadas = set()

pdfs = set()

imagenes = set()


carpeta_descargas = "descargas"

os.makedirs(
    carpeta_descargas,
    exist_ok=True
)



# =====================================================
# LIMPIAR URL
# =====================================================

def limpiar_url(url):

    partes = urlparse(url)

    return urlunparse(
        (
            partes.scheme,
            partes.netloc,
            partes.path,
            partes.params,
            partes.query,
            ""
        )
    )



# =====================================================
# VALIDAR DOMINIO
# =====================================================

def es_del_dominio(url):

    host = urlparse(url).netloc.lower()

    return (
        host.endswith("www.cedarlng.com")
    )



# =====================================================
# DESCARGAR ARCHIVOS
# =====================================================

def descargar(url):

    try:

        nombre = urlparse(url).path.split("/")[-1]


        if not nombre:

            nombre = "archivo"



        nombre = re.sub(
            r'[^a-zA-Z0-9._-]',
            "_",
            nombre
        )


        ruta = os.path.join(
            carpeta_descargas,
            nombre
        )


        if os.path.exists(ruta):

            return



        print(
            "Descargando:",
            url
        )


        respuesta = requests.get(
            url,
            timeout=40,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            }
        )


        if respuesta.status_code == 200:

            with open(
                ruta,
                "wb"
            ) as f:

                f.write(
                    respuesta.content
                )


    except Exception as e:

        print(
            "Error descarga:",
            url,
            e
        )



# =====================================================
# SELENIUM
# =====================================================

options = Options()

# Quitar comentario si quieres ocultarlo
# options.add_argument("--headless")

options.add_argument(
    "--no-sandbox"
)

options.add_argument(
    "--disable-dev-shm-usage"
)

options.add_argument(
    "--window-size=1920,1080"
)


driver = webdriver.Chrome(
    options=options
)



# =====================================================
# AÑADIR SITEMAP
# =====================================================

try:

    sitemap = dominio + "/sitemap.xml"

    r = requests.get(
        sitemap,
        timeout=10
    )


    if r.status_code == 200:

        urls = re.findall(
            r'<loc>(.*?)</loc>',
            r.text
        )


        for u in urls:

            if es_del_dominio(u):

                pendientes.append(
                    limpiar_url(u)
                )


        print(
            "Sitemap cargado:",
            len(urls),
            "URLs"
        )


except:

    pass



# =====================================================
# CRAWLER
# =====================================================

while pendientes:


    url_actual = pendientes.pop(0)


    url_actual = limpiar_url(
        url_actual
    )


    if url_actual in visitadas:

        continue



    if not es_del_dominio(url_actual):

        continue



    print("\n====================")
    print(
        "Visitando:",
        url_actual
    )
    print("====================")


    visitadas.add(
        url_actual
    )



    try:

        driver.get(
            url_actual
        )


        time.sleep(2)


        html = driver.page_source



        soup = BeautifulSoup(
            html,
            "html.parser"
        )



        # =====================================================
        # PDF EN HTML
        # =====================================================

        encontrados = re.findall(
            r'https?://[^"\']+\.pdf',
            html,
            re.I
        )


        for pdf in encontrados:

            pdfs.add(
                pdf.replace(
                    "\\/",
                    "/"
                )
            )



        # =====================================================
        # IMAGENES IMG
        # =====================================================

        for img in soup.find_all(
            "img"
        ):


            fuentes = []


            for atributo in [
                "src",
                "data-src",
                "data-original"
            ]:

                if img.get(atributo):

                    fuentes.append(
                        img[atributo]
                    )



            if img.get("srcset"):

                for x in img["srcset"].split(","):

                    fuentes.append(
                        x.strip().split()[0]
                    )



            for fuente in fuentes:


                imagen = limpiar_url(
                    urljoin(
                        url_actual,
                        fuente
                    )
                )


                if es_del_dominio(imagen):

                    if re.search(
                        r'\.(jpg|jpeg|png|gif|webp|svg)',
                        imagen,
                        re.I
                    ):

                        imagenes.add(
                            imagen
                        )



        # =====================================================
        # IMAGENES CSS
        # =====================================================

        css = re.findall(
            r'url\(["\']?(.*?)["\']?\)',
            html,
            re.I
        )


        for img in css:


            imagen = limpiar_url(
                urljoin(
                    url_actual,
                    img
                )
            )


            if re.search(
                r'\.(jpg|jpeg|png|gif|webp|svg)',
                imagen,
                re.I
            ):

                imagenes.add(
                    imagen
                )



        # =====================================================
        # ENLACES
        # =====================================================

        for enlace in soup.find_all(
            "a",
            href=True
        ):


            href = enlace["href"].strip()



            if href.startswith(
                (
                    "#",
                    "mailto:",
                    "tel:",
                    "javascript:"
                )
            ):

                continue



            recurso = limpiar_url(
                urljoin(
                    url_actual,
                    href
                )
            )



            if not es_del_dominio(
                recurso
            ):

                continue



            if re.search(
                r'\.pdf($|\?)',
                recurso,
                re.I
            ):

                pdfs.add(
                    recurso
                )

                continue



            if re.search(
                r'\.(jpg|jpeg|png|gif|webp|svg)($|\?)',
                recurso,
                re.I
            ):

                imagenes.add(
                    recurso
                )

                continue



            if recurso not in visitadas:

                if recurso not in pendientes:

                    print(
                        "Nueva página:",
                        recurso
                    )

                    pendientes.append(
                        recurso
                    )



    except Exception as e:

        print(
            "ERROR:",
            e
        )



# =====================================================
# FINAL
# =====================================================

driver.quit()



print("\n====================")
print("FINALIZADO")
print("====================")

print(
    "Paginas visitadas:",
    len(visitadas)
)

print(
    "PDF encontrados:",
    len(pdfs)
)

print(
    "Imagenes encontradas:",
    len(imagenes)
)



# =====================================================
# DESCARGAS
# =====================================================

for pdf in sorted(pdfs):

    descargar(
        pdf
    )


for img in sorted(imagenes):

    descargar(
        img
    )



# =====================================================
# GUARDAR RESULTADOS
# =====================================================

with open(
    "paginas_visitadas.txt",
    "w",
    encoding="utf-8"
) as f:

    for x in sorted(visitadas):

        f.write(
            x+"\n"
        )



with open(
    "pdfs_encontrados.txt",
    "w",
    encoding="utf-8"
) as f:

    for x in sorted(pdfs):

        f.write(
            x+"\n"
        )



with open(
    "imagenes_encontradas.txt",
    "w",
    encoding="utf-8"
) as f:

    for x in sorted(imagenes):

        f.write(
            x+"\n"
        )



print("\nArchivos creados:")
print("paginas_visitadas.txt")
print("pdfs_encontrados.txt")
print("imagenes_encontradas.txt")
print("carpeta descargas/")