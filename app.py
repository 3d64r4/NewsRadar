from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from NewsFinder import buscar_menciones


app = FastAPI()


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_methods=["*"],

    allow_headers=["*"]

)



@app.get("/buscar")
def buscar(
    dias:int = 7,
    temas:str = None
):

    try:

        #resultados = buscar_menciones(
         #   dias,
          #  temas
        #)

        resultados = buscar_menciones(
            dias,
            temas
        )

        print("TIPO RESULTADO:", type(resultados))
        print("VALOR:", resultados)

        return {

            "total": len(resultados),

            "resultados": resultados

        }


    except Exception as e:

        print("ERROR:", e)

        return {

            "error": str(e)

        }