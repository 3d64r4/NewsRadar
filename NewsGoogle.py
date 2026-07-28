import feedparser
import urllib.parse
import csv
from datetime import datetime

temas = [
    "Amigo LNG",
    "Amigo GNL",
    "LNG Alliance",
    "Guaymas LNG",
    "Sonora gas natural licuado"
]

archivo_csv = "noticias_amigo_lng_ultima_semana.csv"

fecha_busqueda = datetime.now().strftime("%Y-%m-%d %H:%M")

# Guardar CSV
with open(archivo_csv, "w", newline="", encoding="utf-8") as archivo:

    escritor = csv.writer(archivo)

    escritor.writerow([
        "Fecha búsqueda",
        "Tema",
        "Título",
        "Fecha noticia",
        "URL"
    ])

    noticias_guardadas = set()

    for tema in temas:

        print("\n" + "=" * 70)
        print("BUSCANDO:", tema)
        print("=" * 70)

        # Buscar solo últimos 7 días
        consulta = urllib.parse.quote(f"{tema} when:7d")

        url = (
            f"https://news.google.com/rss/search?"
            f"q={consulta}&hl=es&gl=MX&ceid=MX:es"
        )

        noticias = feedparser.parse(url)

        print("Noticias encontradas:", len(noticias.entries))

        for noticia in noticias.entries:

            # Evitar duplicados por URL
            if noticia.link in noticias_guardadas:
                continue

            noticias_guardadas.add(noticia.link)

            print("\nTítulo:", noticia.title)
            print("Fecha:", noticia.published)
            print("URL:", noticia.link)

            escritor.writerow([
                fecha_busqueda,
                tema,
                noticia.title,
                noticia.published,
                noticia.link
            ])

print("\nArchivo creado:", archivo_csv)
print("Total noticias guardadas:", len(noticias_guardadas))