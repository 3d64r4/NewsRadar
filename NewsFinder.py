
import os
import csv
import requests
import feedparser
import urllib.parse
from datetime import datetime

from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SERPAPI_API_KEY")

if not API_KEY:
    raise Exception("No se encontró SERPAPI_API_KEY en el archivo .env")


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

archivo_csv = "monitoreo_resultados.csv"

temas_defecto = [

    "Amigo LNG",
    "Amigo GNL",
    "LNG Alliance",
    "Guaymas LNG",
    "Muthu Chezhian",
    "Sonora gas natural licuado",
    "terminal GNL Guaymas"

]


# ==========================================================
# PALABRAS IMPORTANTES
# ==========================================================

palabras_importantes = [

    "amigo lng",
    "amigo gnl",
    "lng alliance",
    "guaymas",
    "sonora",
    "mexico",
    "méxico",
    "gas natural licuado",
    "lng",
    "gnl",
    "epsilon",
    "terminal",
    "licuefacción"

]


# ==========================================================
# PALABRAS A EXCLUIR
# ==========================================================

palabras_excluir = [

    "empleo",
    "vacante",
    "indeed",
    "computrabajo",
    "amazon",
    "alibaba",
    "mercadolibre",
    "wikipedia",
    "pinterest"

]


# ==========================================================
# PALABRAS POSITIVAS
# ==========================================================

positivas = [

    "inversión",
    "desarrollo",
    "crecimiento",
    "empleos",
    "beneficio",
    "expansión",
    "progreso",
    "acuerdo"

]


# ==========================================================
# PALABRAS NEGATIVAS
# ==========================================================

negativas = [

    "protesta",
    "demanda",
    "amparo",
    "contaminación",
    "impacto",
    "cancelación",
    "suspensión",
    "rechazo",
    "ballenas",
    "riesgo"

]


# ==========================================================
# DETECTAR FUENTE
# ==========================================================

def detectar_fuente(url):

    url = url.lower()

    if "facebook.com" in url:
        return "Facebook"

    if "instagram.com" in url:
        return "Instagram"

    if "x.com" in url:
        return "X"

    if "twitter.com" in url:
        return "X"

    if "linkedin.com" in url:
        return "LinkedIn"

    if "youtube.com" in url:
        return "YouTube"

    return "Web"


# ==========================================================
# CALCULAR PUNTAJE
# ==========================================================

def calcular_puntaje(texto):

    texto = texto.lower()

    puntaje = 0

    for palabra in palabras_importantes:

        if palabra in texto:
            puntaje += 1

    if "amigo gnl" in texto:
        puntaje += 5

    if "amigo lng" in texto:
        puntaje += 5

    if "guaymas" in texto:
        puntaje += 3

    if "sonora" in texto:
        puntaje += 2

    return puntaje


# ==========================================================
# DETECTAR PALABRAS
# ==========================================================

def detectar_palabras(texto):

    texto = texto.lower()

    encontradas = []

    for palabra in palabras_importantes:

        if palabra in texto:
            encontradas.append(palabra)

    return ", ".join(encontradas)


# ==========================================================
# ANALIZAR SENTIMIENTO
# ==========================================================

def analizar_sentimiento(texto):

    texto = texto.lower()

    positivos = 0
    negativos_total = 0

    for palabra in positivas:

        if palabra in texto:
            positivos += 1

    for palabra in negativas:

        if palabra in texto:
            negativos_total += 1

    if positivos > negativos_total:
        return "POSITIVO"

    if negativos_total > positivos:
        return "NEGATIVO"

    return "NEUTRAL"

# FIN DE LA PRIMER PARTE iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
# ==========================================================
# FUNCIÓN PRINCIPAL
# ==========================================================
# ==========================================================
# FUNCIÓN PRINCIPAL
# ==========================================================

def buscar_menciones(dias, temas_usuario=None):


    # ---------------------------------------------
    # Determinar temas
    # ---------------------------------------------

    if temas_usuario:

        temas = [
            t.strip()
            for t in temas_usuario.split(",")
            if t.strip()
        ]

    else:

        temas = temas_defecto



    # ---------------------------------------------
    # Fechas
    # ---------------------------------------------

    fecha_actual = datetime.now()

    fecha_inicio = fecha_actual - timedelta(days=dias)

    fecha_google = fecha_inicio.strftime("%Y-%m-%d")

    fecha_busqueda = fecha_actual.strftime("%Y-%m-%d %H:%M")



    print()
    print("=" * 70)
    print("MONITOR DE MEDIOS")
    print("=" * 70)

    print("Periodo:", dias, "días")
    print("Desde:", fecha_google)
    print("Temas:", temas)

    print("=" * 70)



    resultados_guardados = set()

    resultados_finales = []



    # ---------------------------------------------
    # Recorrer temas
    # ---------------------------------------------

    for tema in temas:


        print()
        print("=" * 70)
        print("BUSCANDO:", tema)
        print("=" * 70)



        consultas = [

            f'"{tema}" after:{fecha_google}',

            f'"{tema}" Guaymas after:{fecha_google}',

            f'"{tema}" Sonora after:{fecha_google}',

            f'"{tema}" México after:{fecha_google}',

            f'"{tema}" LNG after:{fecha_google}',

            f'"{tema}" GNL after:{fecha_google}',

            f'"{tema}" "gas natural licuado" after:{fecha_google}',

            f'site:facebook.com "{tema}" after:{fecha_google}',

            f'site:instagram.com "{tema}" after:{fecha_google}',

            f'site:x.com "{tema}" after:{fecha_google}',

            f'site:linkedin.com "{tema}" after:{fecha_google}',

            f'site:youtube.com "{tema}" after:{fecha_google}'

        ]



        # -----------------------------------------
        # Ejecutar consultas
        # -----------------------------------------

        for consulta in consultas:


            print()
            print("Consulta:", consulta)



            try:

                respuesta = requests.get(

                    "https://serpapi.com/search",

                    params={

                        "engine": "google",

                        "q": consulta,

                        "hl": "es",

                        "gl": "mx",

                        "num": 10,

                        "api_key": API_KEY

                    },

                    timeout=30

                )


            except Exception as error:

                print("Error:", error)

                continue



            if respuesta.status_code != 200:

                print("HTTP:", respuesta.status_code)

                continue



            datos = respuesta.json()



            resultados = datos.get(

                "organic_results",

                []

            )



            print("Resultados:", len(resultados))

            for r in resultados:

                titulo = r.get("title", "")
                descripcion = r.get("snippet", "")
                url = r.get("link", "")

                if not url:
                    continue

                if url in resultados_guardados:
                    continue

                resultados_guardados.add(url)

                texto = (
                        titulo +
                        " " +
                        descripcion +
                        " " +
                        url
                ).lower()

                ignorar = False

                for palabra in palabras_excluir:

                    if palabra in texto:
                        ignorar = True
                        break

                if ignorar:
                    continue

                puntaje = calcular_puntaje(texto)

                if puntaje < 5:
                    continue

                fuente = detectar_fuente(url)

                sentimiento = analizar_sentimiento(texto)

                palabras = detectar_palabras(texto)

                print()
                print("✔ RESULTADO")
                print("Título:", titulo)
                print("Fuente:", fuente)
                print("Puntaje:", puntaje)

                resultados_finales.append({

                    "fecha": fecha_busqueda,
                    "tema": tema,
                    "consulta": consulta,
                    "fuente": fuente,
                    "puntaje": puntaje,
                    "sentimiento": sentimiento,
                    "palabras": palabras,
                    "titulo": titulo,
                    "descripcion": descripcion,
                    "url": url

                })


            # -------------------------------------
            # Procesar resultados encontrados
            # -------------------------------------

            for resultado in resultados:


                titulo = resultado.get(
                    "title",
                    ""
                )


                descripcion = resultado.get(
                    "snippet",
                    ""
                )


                url = resultado.get(
                    "link",
                    ""
                )



                if not url:

                    continue



                if url in resultados_guardados:

                    continue



                texto = (

                    titulo +

                    " " +

                    descripcion +

                    " " +

                    url

                ).lower()



                # excluir basura

                ignorar = False


                for palabra in palabras_excluir:


                    if palabra in texto:

                        ignorar = True

                        break



                if ignorar:

                    continue



                puntaje = calcular_puntaje(texto)



                if puntaje < 5:

                    continue



                resultados_guardados.add(url)



                fuente = detectar_fuente(url)


                sentimiento = analizar_sentimiento(texto)


                palabras = detectar_palabras(texto)



                print()
                print("✔ RESULTADO")
                print("Título:", titulo)
                print("Fuente:", fuente)
                print("Puntaje:", puntaje)



                resultados_finales.append({

                    "fecha": fecha_busqueda,

                    "tema": tema,

                    "consulta": consulta,

                    "fuente": fuente,

                    "puntaje": puntaje,

                    "sentimiento": sentimiento,

                    "palabras": palabras,

                    "titulo": titulo,

                    "descripcion": descripcion,

                    "url": url

                })

    # ---------------------------------------------
    # Agregar resultados de Google News RSS
    # ---------------------------------------------

    for tema in temas:

        resultados_rss = buscar_google_rss(
            tema,
            dias
        )

        for r in resultados_rss:

            if r["url"] not in resultados_guardados:

                resultados_guardados.add(
                    r["url"]
                )

                resultados_finales.append(r)

    # ---------------------------------------------
    # Guardar CSV al terminar
    # ---------------------------------------------

    with open(

        archivo_csv,

        "w",

        newline="",

        encoding="utf-8"

    ) as archivo:


        escritor = csv.writer(archivo)


        escritor.writerow([

            "Fecha",

            "Tema",

            "Consulta",

            "Fuente",

            "Puntaje",

            "Sentimiento",

            "Palabras",

            "Título",

            "Descripción",

            "URL"

        ])



        for r in resultados_finales:


            escritor.writerow([

                r["fecha"],

                r["tema"],

                r["consulta"],

                r["fuente"],

                r["puntaje"],

                r["sentimiento"],

                r["palabras"],

                r["titulo"],

                r["descripcion"],

                r["url"]

            ])



    print()

    print("=" * 70)

    print("TOTAL RESULTADOS:", len(resultados_finales))

    print("CSV generado:", archivo_csv)

    print("=" * 70)

    # ---------------------------------------------
    # Agregar resultados Google RSS
    # ---------------------------------------------

    for tema in temas:

        resultados_rss = buscar_google_rss(
            tema,
            dias
        )

        for r in resultados_rss:

            if r["url"] not in resultados_guardados:

                resultados_guardados.add(
                    r["url"]
                )

                resultados_finales.append(r)


    # ---------------------------------------------
    # Agregar Google News RSS
    # ---------------------------------------------

    for tema in temas:

        rss = buscar_google_rss(
            tema,
            dias
        )

        for r in rss:

            url = r["url"]

            if url in resultados_guardados:
                continue

            texto = (
                    r["titulo"]
                    + " "
                    + r["descripcion"]
            ).lower()

            puntaje = calcular_puntaje(texto)

            sentimiento = analizar_sentimiento(texto)

            palabras = detectar_palabras(texto)

            r["puntaje"] = puntaje
            r["sentimiento"] = sentimiento
            r["palabras"] = palabras

            resultados_guardados.add(url)

            resultados_finales.append(r)


    return resultados_finales

def buscar_google_rss(tema, dias=7):

    resultados = []

    consulta = urllib.parse.quote(
        f"{tema} when:{dias}d"
    )

    url = (
        "https://news.google.com/rss/search?"
        f"q={consulta}&hl=es&gl=MX&ceid=MX:es"
    )

    noticias = feedparser.parse(url)


    print("\nGoogle RSS")
    print("Consulta:", tema)
    print("Resultados:", len(noticias.entries))


    for noticia in noticias.entries:

        resultado = {

            "fecha":
                datetime.now().strftime("%Y-%m-%d %H:%M"),

            "tema":
                tema,

            "consulta":
                f"Google RSS {tema}",

            "fuente":
                "Google News RSS",

            "puntaje":
                0,

            "sentimiento":
                "NEUTRAL",

            "palabras":
                tema,

            "titulo":
                noticia.get("title", ""),

            "descripcion":
                noticia.get("description", ""),

            "url":
                noticia.get("link", "")
        }


        resultados.append(resultado)


    return resultados