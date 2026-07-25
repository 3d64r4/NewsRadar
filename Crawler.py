import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import time


# =====================================================
# CONFIGURACIÓN
# =====================================================

dominio = "https://ues.sonora.gob.mx"

pendientes = [
    dominio
]

visitadas = set()


headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}



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
            "",
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
        host.endswith("ues.sonora.gob.mx")
    )



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



    print(
        "Visitando:",
        url_actual
    )


    visitadas.add(
        url_actual
    )



    try:

        respuesta = requests.get(
            url_actual,
            headers=headers,
            timeout=20
        )


        if respuesta.status_code != 200:

            continue



        soup = BeautifulSoup(
            respuesta.text,
            "html.parser"
        )



        # Buscar todos los enlaces

        for enlace in soup.find_all(
            "a",
            href=True
        ):


            href = enlace["href"].strip()



            # Ignorar enlaces no web

            if href.startswith(
                (
                    "#",
                    "mailto:",
                    "tel:",
                    "javascript:"
                )
            ):

                continue



            nueva_url = limpiar_url(
                urljoin(
                    url_actual,
                    href
                )
            )



            if not es_del_dominio(
                nueva_url
            ):

                continue



            if nueva_url not in visitadas:

                if nueva_url not in pendientes:

                    pendientes.append(
                        nueva_url
                    )



        # evitar saturar servidor

        time.sleep(0.5)



    except Exception as e:

        print(
            "Error:",
            url_actual,
            e
        )



# =====================================================
# RESULTADOS
# =====================================================

print("\n==============================")
print("CRAWLER TERMINADO")
print("==============================")

print(
    "Páginas encontradas:",
    len(visitadas)
)



for pagina in sorted(visitadas):

    print(
        pagina
    )



# Guardar lista

with open(
    "paginas_visitadas.txt",
    "w",
    encoding="utf-8"
) as archivo:


    for pagina in sorted(visitadas):

        archivo.write(
            pagina + "\n"
        )



print(
    "\nArchivo generado:"
)

print(
    "paginas_visitadas.txt"
)