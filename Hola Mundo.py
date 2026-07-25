from dis import spec_op
import os
print("hola mundo")
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://www.lngalliance.com/about-us"
r = requests.get(url)

#r = requests.get('https://www.lngalliance.com/about-us', allow_redirects = False)
#r = requests.get('https://www.lngalliance.com/about-us')
print(r.status_code)
#print(dir(r))
#print(help(r))
#print(r.text)
soup = BeautifulSoup(r.content, "html.parser")
soup = BeautifulSoup(r.text, "html.parser")
#print(soup.prettify())

titulo = soup.find("title",  )
if titulo:
    print(titulo.text)
else:
    print("No se encontró la etiqueta <title>")


fakepythontitle = soup.find('title')
print(fakepythontitle)


#fakepythonparagyaphs = soup.find_all('p')
#print(fakepythonparagyaphs)

imagenes = soup.find_all("img")

print(f"Se encontraron {len(imagenes)} imágenes\n")

for img in imagenes:
    print(img)

    os.makedirs("imagenes", exist_ok=True)

    for i, img in enumerate(soup.find_all("img"), start=1):
        src = img.get("src")

        if src:
            img_url = urljoin(url, src)

            try:
                img_data = requests.get(img_url).content

                with open(f"imagenes/imagen_{i}.jpg", "wb") as f:
                    f.write(img_data)

                print(f"Descargada: {img_url}")

            except Exception as e:
                print(f"Error descargando {img_url}: {e}")