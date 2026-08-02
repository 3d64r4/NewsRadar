import requests
import csv
from datetime import datetime, timedelta


# =========================================
# CONFIGURACIÓN
# =========================================

temas = [

    "Amigo LNG",
    "Amigo GNL",
    "LNG Alliance",
    "Guaymas LNG",
    "Muthu Chezhian",
    "Sonora gas natural licuado",
    "terminal GNL Guaymas"

]


archivo_csv = "monitoreo_relevante_amigo_lng.csv"


API_KEY = "715dfb61405827045b71d8df255f988b6aa9acf5441ac3980cdfeb779c9efd02"


# =========================================
# PALABRAS DE CONTEXTO
# =========================================

palabras_importantes = [

    "amigo lng",
    "amigo gnl",
    "lng alliance",
    "guaymas",
    "sonora",
    "méxico",
    "mexico",
    "gas natural licuado",
    "gnl",
    "lng"

]


palabras_excluir = [

    "empleo",
    "vacante",
    "amazon",
    "alibaba",
    "wikipedia",
    "pinterest"

]


# =========================================
# RANGO DE FECHAS
# =========================================

dias = int(
    input(
        "¿Cuántos días hacia atrás desea buscar?: "
    )
)


fecha_actual = datetime.now()

fecha_inicio = fecha_actual - timedelta(
    days=dias
)


fecha_google = fecha_inicio.strftime(
    "%Y-%m-%d"
)


fecha_busqueda = fecha_actual.strftime(
    "%Y-%m-%d %H:%M"
)


print("\n==============================")
print("MONITOREO AMIGO LNG")
print("==============================")
print("Periodo:", dias, "días")
print("Desde:", fecha_google)
print("==============================")



# =========================================
# CREAR CSV
# =========================================

with open(
    archivo_csv,
    "w",
    newline="",
    encoding="utf-8"
) as archivo:


    escritor = csv.writer(archivo)


    escritor.writerow([

        "Fecha búsqueda",
        "Días analizados",
        "Tema",
        "Fuente",
        "Puntaje",
        "Título",
        "Descripción",
        "URL"

    ])


    resultados_guardados = set()



    # =========================================
    # BUSCAR TEMAS
    # =========================================

    for tema in temas:


        print("\n")
        print("=" * 70)
        print("BUSCANDO:", tema)
        print("=" * 70)



        consultas = [

            f'"{tema}" Guaymas after:{fecha_google}',

            f'"{tema}" Sonora after:{fecha_google}',

            f'"{tema}" "gas natural licuado" after:{fecha_google}',

            f'"{tema}" site:facebook.com after:{fecha_google}',

            f'"{tema}" site:instagram.com after:{fecha_google}',

            f'"{tema}" site:x.com after:{fecha_google}',

            f'"{tema}" after:{fecha_google}'

        ]



        for consulta in consultas:


            parametros = {


                "engine": "google",

                "q": consulta,

                "hl": "es",

                "gl": "mx",

                "api_key": API_KEY

            }



            respuesta = requests.get(

                "https://serpapi.com/search",

                params=parametros

            )



            if respuesta.status_code != 200:

                print(
                    "Error API",
                    respuesta.status_code
                )

                continue



            datos = respuesta.json()



            resultados = datos.get(

                "organic_results",

                []

            )



            print(
                "Resultados encontrados:",
                len(resultados)
            )



            for resultado in resultados:



                titulo = resultado.get(

                    "title",

                    ""

                )


                snippet = resultado.get(

                    "snippet",

                    ""

                )


                url = resultado.get(

                    "link",

                    ""

                )



                texto = (

                    titulo +

                    " " +

                    snippet +

                    " " +

                    url

                ).lower()



                # -----------------------------
                # EXCLUSIONES
                # -----------------------------


                if any(

                    palabra in texto

                    for palabra in palabras_excluir

                ):

                    continue



                # -----------------------------
                # PUNTAJE DE RELEVANCIA
                # -----------------------------


                puntaje = 0



                for palabra in palabras_importantes:

                    if palabra in texto:

                        puntaje += 1



                if "amigo lng" in texto:

                    puntaje += 5


                if "guaymas" in texto:

                    puntaje += 3


                if "sonora" in texto:

                    puntaje += 2



                # Solo guardar resultados relevantes

                if puntaje < 5:

                    continue



                if url in resultados_guardados:

                    continue



                resultados_guardados.add(url)



                # Identificar fuente


                if "facebook.com" in url:

                    fuente = "Facebook"


                elif "instagram.com" in url:

                    fuente = "Instagram"


                elif "x.com" in url:

                    fuente = "X"


                elif "linkedin.com" in url:

                    fuente = "LinkedIn"


                else:

                    fuente = "Web"



                print("\nRESULTADO RELEVANTE")

                print("Fuente:", fuente)

                print("Puntaje:", puntaje)

                print("Título:", titulo)

                print("Descripción:", snippet)

                print("URL:", url)



                escritor.writerow([


                    fecha_busqueda,

                    dias,

                    tema,

                    fuente,

                    puntaje,

                    titulo,

                    snippet,

                    url


                ])




# =========================================
# RESUMEN
# =========================================


print("\n==============================")
print("FINALIZADO")
print("==============================")

print(
    "Archivo generado:",
    archivo_csv
)


print(

    "Resultados relevantes:",

    len(resultados_guardados)

)