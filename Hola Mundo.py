import requests
import csv
import os

from dotenv import load_dotenv

from datetime import datetime
from datetime import timedelta


# ==========================================
# CARGAR VARIABLES
# ==========================================

load_dotenv()

API_KEY = os.getenv("SERPAPI_KEY")

if not API_KEY:
    print("ERROR: No se encontró SERPAPI_KEY en el archivo .env")
    exit()


# ==========================================
# CONFIGURACIÓN
# ==========================================

temas = [

#    "Amigo LNG",
#    "Amigo GNL",
#    "LNG Alliance",
    "Guaymas LNG",
#  "Muthu Chezhian",
#    "Sonora gas natural licuado",
#    "terminal GNL Guaymas"


]


archivo_csv = "monitoreo_relevante_amigo_lng.csv"


# ==========================================
# PALABRAS IMPORTANTES
# ==========================================

palabras_importantes = [

    "amigo lng",
    "amigo gnl",
    "lng alliance",
    "guaymas",
    "sonora",
    "gas natural licuado",
    "gnl",
    "lng",
    "mexico",
    "méxico"

]


# ==========================================
# PALABRAS A IGNORAR
# ==========================================

palabras_excluir = [

    "vacante",
    "empleo",
    "linkedin jobs",
    "amazon",
    "alibaba",
    "mercadolibre",
    "pinterest",
    "wikipedia"

]


# ==========================================
# PALABRAS NEGATIVAS
# ==========================================

palabras_negativas = [

    "contaminación",
    "contamina",
    "contaminará",
    "rechazo",
    "protesta",
    "manifestación",
    "amparo",
    "demanda",
    "riesgo",
    "impacto ambiental",
    "suspensión",
    "oposición",
    "denuncia",
    "ecocidio"

]


# ==========================================
# PALABRAS POSITIVAS
# ==========================================

palabras_positivas = [

    "inversión",
    "empleos",
    "desarrollo",
    "crecimiento",
    "beneficio",
    "infraestructura",
    "expansión",
    "exportación",
    "energía"

]


# ==========================================
# DETECTAR FUENTE
# ==========================================

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


# ==========================================
# DETECTAR PALABRAS
# ==========================================

def detectar_palabras(texto):

    texto = texto.lower()

    encontradas = []

    for palabra in palabras_importantes:

        if palabra in texto:
            encontradas.append(palabra)

    return ", ".join(encontradas)


# ==========================================
# ANALIZAR SENTIMIENTO
# ==========================================

def analizar_sentimiento(texto):

    texto = texto.lower()

    positivo = 0
    negativo = 0

    for palabra in palabras_positivas:

        if palabra in texto:
            positivo += 1

    for palabra in palabras_negativas:

        if palabra in texto:
            negativo += 1

    if negativo > positivo:
        return "NEGATIVO"

    if positivo > negativo:
        return "POSITIVO"

    return "NEUTRAL"


# ==========================================
# CALCULAR PUNTAJE
# ==========================================

def calcular_puntaje(texto):

    texto = texto.lower()

    puntaje = 0

    for palabra in palabras_importantes:

        if palabra in texto:
            puntaje += 2

    if "amigo lng" in texto:
        puntaje += 6

    if "amigo gnl" in texto:
        puntaje += 6

    if "lng alliance" in texto:
        puntaje += 5

    if "guaymas" in texto:
        puntaje += 3

    if "sonora" in texto:
        puntaje += 2

    if "terminal" in texto:
        puntaje += 1

    return puntaje


# ==========================================
# PEDIR PERIODO
# ==========================================

dias = int(
    input(
        "¿Cuántos días hacia atrás desea buscar?: "
    )
)


fecha_actual = datetime.now()

fecha_inicio = fecha_actual - timedelta(days=dias)

fecha_google = fecha_inicio.strftime("%Y-%m-%d")

fecha_busqueda = fecha_actual.strftime("%Y-%m-%d %H:%M")


print()

print("=" * 60)
print("MONITOR DE MEDIOS - AMIGO LNG")
print("=" * 60)

print("Periodo:", dias, "días")
print("Desde:", fecha_google)

print("=" * 60)

resultados_guardados = set()



# ==========================================
# CREAR CSV
# ==========================================

with open(
    archivo_csv,
    "w",
    newline="",
    encoding="utf-8"
) as archivo:

    escritor = csv.writer(archivo)

    escritor.writerow([

        "Fecha búsqueda",
        "Periodo",
        "Fecha desde",
        "Tema",
        "Consulta",
        "Fuente",
        "Puntaje",
        "Sentimiento",
        "Palabras detectadas",
        "Título",
        "Descripción",
        "URL"

    ])

    # ==========================================
    # RECORRER TEMAS
    # ==========================================

    for tema in temas:

        print()
        print("=" * 70)
        print("BUSCANDO:", tema)
        print("=" * 70)

        consultas = [

            # Noticias generales
            f'"{tema}" after:{fecha_google}',

            # Región
            f'"{tema}" Guaymas after:{fecha_google}',

            f'"{tema}" Sonora after:{fecha_google}',

            f'"{tema}" México after:{fecha_google}',

            # Industria
            f'"{tema}" LNG after:{fecha_google}',

            f'"{tema}" GNL after:{fecha_google}',

            f'"{tema}" "gas natural licuado" after:{fecha_google}',

            # Redes sociales

            f'site:facebook.com "{tema}" after:{fecha_google}',

            f'site:instagram.com "{tema}" after:{fecha_google}',

            f'site:x.com "{tema}" after:{fecha_google}',

            f'site:twitter.com "{tema}" after:{fecha_google}',

            f'site:linkedin.com "{tema}" after:{fecha_google}',

            f'site:youtube.com "{tema}" after:{fecha_google}'

        ]

        # ==========================================
        # EJECUTAR CONSULTAS
        # ==========================================

        for consulta in consultas:

            print()
            print("Consulta:")
            print(consulta)

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

                print("ERROR:", error)

                continue

            if respuesta.status_code != 200:

                print("Error HTTP:", respuesta.status_code)

                continue

            datos = respuesta.json()

            resultados = datos.get(
                "organic_results",
                []
            )

            print("Resultados encontrados:", len(resultados))

            if len(resultados) == 0:
                continue

            # ==========================================
            # RECORRER RESULTADOS
            # ==========================================

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

                texto = (

                    titulo +
                    " " +
                    descripcion +
                    " " +
                    url

                ).lower()

                # Evitar URLs duplicadas

                if url in resultados_guardados:
                    continue

                # Ignorar páginas irrelevantes

                ignorar = False

                for palabra in palabras_excluir:

                    if palabra in texto:
                        ignorar = True
                        break

                if ignorar:
                    continue

                # Calcular puntaje

                puntaje = calcular_puntaje(texto)

                # Solo resultados relevantes

                if puntaje < 5:
                    continue

                resultados_guardados.add(url)

                fuente = detectar_fuente(url)

                sentimiento = analizar_sentimiento(texto)

                palabras = detectar_palabras(texto)

                # ==========================================
                # MOSTRAR RESULTADO
                # ==========================================

                print()
                print("=" * 70)
                print("RESULTADO RELEVANTE")
                print("=" * 70)

                print("Tema.............:", tema)
                print("Fuente...........:", fuente)
                print("Puntaje..........:", puntaje)
                print("Sentimiento......:", sentimiento)
                print("Palabras.........:", palabras)

                print("\nConsulta utilizada:")
                print(consulta)

                print("\nTítulo:")
                print(titulo)

                print("\nDescripción:")
                print(descripcion)

                print("\nEnlace:")
                print(url)

                # ==========================================
                # GUARDAR CSV
                # ==========================================

                escritor.writerow([

                    fecha_busqueda,

                    dias,

                    fecha_google,

                    tema,

                    consulta,

                    fuente,

                    puntaje,

                    sentimiento,

                    palabras,

                    titulo,

                    descripcion,

                    url

                ])

            print()
            print("-" * 70)
            print("Tema finalizado:", tema)
            print("-" * 70)



# ==========================================
# RESUMEN FINAL
# ==========================================

print()
print("=" * 70)
print("RESUMEN DEL MONITOREO")
print("=" * 70)

print("Fecha de búsqueda :", fecha_busqueda)
print("Periodo analizado :", dias, "días")
print("Desde             :", fecha_google)
print("Resultados únicos :", len(resultados_guardados))
print("Archivo generado  :", archivo_csv)

print()

# ==========================================
# CONTAR RESULTADOS POR FUENTE
# ==========================================

conteo_fuentes = {
    "Facebook": 0,
    "Instagram": 0,
    "X": 0,
    "LinkedIn": 0,
    "YouTube": 0,
    "Web": 0
}

try:

    with open(
        archivo_csv,
        newline="",
        encoding="utf-8"
    ) as archivo:

        lector = csv.DictReader(archivo)

        for fila in lector:

            fuente = fila["Fuente"]

            if fuente in conteo_fuentes:
                conteo_fuentes[fuente] += 1

except Exception as e:

    print("No fue posible generar estadísticas.")
    print(e)

print("=" * 70)
print("RESULTADOS POR FUENTE")
print("=" * 70)

for fuente, total in conteo_fuentes.items():

    print(f"{fuente:12} : {total}")

print()

print("=" * 70)
print("PROCESO FINALIZADO")
print("=" * 70)

if len(resultados_guardados) == 0:

    print("No se encontraron resultados relevantes.")

else:

    print(f"Se encontraron {len(resultados_guardados)} resultados relevantes.")

print()
print("CSV generado correctamente.")
print(os.path.abspath(archivo_csv))

print()
print("Puede abrir el archivo con Excel, LibreOffice o Google Sheets.")


