// Cambiar esta dirección cuando tengas tu backend en Render

//const API_URL =
//"https://TU-BACKEND.onrender.com/buscar";

//const API_URL =
//"http://localhost:8000/buscar";

const API_URL =
"https://newsradar-8ihl.onrender.com/buscar";

async function buscar(){


    const dias =
    document.getElementById("dias").value;


    const temas =
    document.getElementById("temas").value;



    const estado =
    document.getElementById("estado");


    const resultados =
    document.getElementById("resultados");



    estado.innerHTML =
    "Buscando información...";

    resultados.innerHTML="";



    try{


        const respuesta =
        await fetch(

            API_URL +
            "?dias=" +
            dias +
            "&temas=" +
            encodeURIComponent(temas)

        );



        if(!respuesta.ok){

            throw new Error(
                "Error del servidor"
            );

        }



        const datos =
        await respuesta.json();



        mostrarResultados(datos);




    }

    catch(error){


        estado.innerHTML =
        "Error conectando con el backend";


        console.error(error);


    }



}





function mostrarResultados(datos){


const estado =
document.getElementById("estado");


const resumen =
document.getElementById("resumen");


const contenedor =
document.getElementById("resultados");

contenedor.innerHTML = "";

   let lista =
Array.isArray(datos.resultados)
?
datos.resultados
:
[];

let negativos = lista.filter(
r => r.sentimiento === "NEGATIVO"
).length;


let positivos = lista.filter(
r => r.sentimiento === "POSITIVO"
).length;


let neutrales = lista.filter(
r => r.sentimiento === "NEUTRAL"
).length;

    estado.innerHTML =

    "Resultados encontrados: "
    +
    lista.length;

    resumen.innerHTML = `


<div class="tarjeta total">

<b>${lista.length}</b>

<br>

Total

</div>



<div class="tarjeta rojo">

<b>${negativos}</b>

<br>

Negativos

</div>



<div class="tarjeta gris">

<b>${neutrales}</b>

<br>

Neutrales

</div>



<div class="tarjeta verde">

<b>${positivos}</b>

<br>

Positivos

</div>


`;



    if(lista.length===0){

        contenedor.innerHTML =
        "<p>No se encontraron resultados.</p>";

        return;

    }



    lista.forEach(resultado=>{


        let clase =
        "neutral";



        if(
            resultado.sentimiento
            ===
            "NEGATIVO"
        ){

            clase="negativo";

        }



        if(
            resultado.sentimiento
            ===
            "POSITIVO"
        ){

            clase="positivo";

        }




        contenedor.innerHTML += `


       <div class="resultado ${clase}">


            <h3>
            ${resultado.titulo || ""}
            </h3>


            <div class="info">

            <b>Fuente:</b>
            ${resultado.fuente || ""}

            </div>



            <div class="info">

            <b>Puntaje:</b>
            ${resultado.puntaje || ""}

            </div>



            <div class="info ${clase}">

            <b>Sentimiento:</b>
            ${resultado.sentimiento || "N/A"}

            </div>



            <p>

            ${resultado.descripcion || ""}

            </p>



            <a
            href="${resultado.url}"
            target="_blank">

            Abrir fuente original

            </a>



        </div>


        `;


    });


}