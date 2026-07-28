import requests

API_KEY = "c6addadee87b40f8b698d27523a809b5"

busqueda = '( "Amigo LNG" OR "AMIGO GNL" OR "Amigo GNL" OR "proyecto Amigo" )'

url = "https://newsapi.org/v2/everything"

params = {
    "q": busqueda,
    "sortBy": "publishedAt",
    "pageSize": 20,
    "apiKey": API_KEY
}

respuesta = requests.get(url, params=params)

print("URL consultada:")
print(respuesta.url)

datos = respuesta.json()

print("Resultados:", datos.get("totalResults"))

if datos["status"] == "ok":
    for noticia in datos["articles"]:
        print("-" * 60)
        print(noticia["title"])
        print(noticia["source"]["name"])
        print(noticia["url"])
else:
    print(datos)