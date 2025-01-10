# Inicia el servidor de backend:
    uvicorn backend:app --reload

# Para generar los distintos archivos con el scraper hay que pasar los valores en el body:
-----------------------------------------------------------------------------------------
Método: POST
URL: 127.0.0.1:8000/scraper/generate_pd
BODY(raw): 
{
  "files": [
    {
      "filename": "Grado",
      "title": "Facultad de Humanidades - UNCa",
      "subtitle": "Oferta Académica de Grado",
      "url": "https://huma.unca.edu.ar/oferta-academica/grado"
    },
    {
      "filename": "Posgrado",
      "title": "Facultad de Humanidades - UNCa",
      "subtitle": "Oferta Académica de Posgrado",
      "url": "https://huma.unca.edu.ar/oferta-academica/posgrado"
    },
    {
      "filename": "Diplomaturas",
      "title": "Facultad de Humanidades - UNCa",
      "subtitle": "Oferta Académica de Diplomaturas",
      "url": "https://huma.unca.edu.ar/oferta-academica/diplomaturas"
    }   
  ]
}
