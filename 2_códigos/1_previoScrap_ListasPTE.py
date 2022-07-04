"""
1. Descripción:
    Script que scrapea links agrupados en 6 listas del PTE y elabora un excel con los id_entidad y el nombre de la entidad
2. Inputs:
    NaN
3. Outputs:
    Excel con los campos: "id_entidad" y "name_entidad"
4. Supuesto:
    NaN
"""

# importación de librerías
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date

# para contabilizar tiempo de demora
start = time.time()
today = date.today()
d1 = today.strftime("%d_%m_%Y")

# ----------------- MODIFICABLE ----------------- #
#
# ruta de salida
PATH_OUTPUT = 'C:/Users/ARON SANTA CRUZ/Documents/ceplan/github/proyectoPTE/1_data/2_scrap/'
# nombre del archivo
FILE_OUTPUT = 'ID_ENTIDAD_LISTAS_{}.xlsx'.format(d1)
# tiempo de espera para cargar URL
timeout=10
#
# ----------------- MODIFICABLE ----------------- #

BBDD = pd.DataFrame() # se crea dataframe vacía para almacenar info
# se declaran los elementos del bucle (luego de inspección del PTE)
para_bucle = ['','?Tipo_Pod=1','?Tipo_Pod=2','?Tipo_Pod=4','?Tipo_Pod=5','?Tipo_Pod=7']
for web_add in para_bucle:
    # url raiz que siempre aparece en los links de las 6 listas
    web_core = 'https://www.transparencia.gob.pe/buscador/pte_transparencia_listado_entidades_poder.aspx'
    URL = web_core + web_add
    # variable para evitar que un corte de internet detenga la ejecución
    noConectadoInternet=True
    while (noConectadoInternet):
        try:
            reqs = requests.get(URL,timeout=timeout,headers={'Connection':'close'}) # explora el link
            noConectadoInternet=False
        except (requests.ConnectionError, requests.Timeout):
            noConectadoInternet=True # noConectadoInternet será verdadero para que el while se repita 1 vez más
            print('No conectado. Intentando conectarse...') # mensaje alerta
    content = reqs.text # pasa a 'texto' el contenido obtenido por el requests
    soup = BeautifulSoup(content, 'html.parser') # contenido es "partido" en secciones con bs
    id_entidad = [] # crea listas vacías para almacenar info scrapeada
    name_entidad = []
    # bucle para todos los elementos 'li' encontrados en el contenido
    for h in soup.findAll('li'):
        a = h.find('a') # dentro de los elementos 'li', buscar el elemento 'a' que contiene texto
        # 'try' evita que un error detenga la ejecución
        try:
            # los links está dentro del elemento 'href'
            if 'href' in a.attrs:
                url = a.get('href') # solo me quedo con el contenido del 'href'
                # si el link contiene la palabra 'id_entidad'
                if 'id_entidad=' in url:
                    _id=url.replace('../enlaces/pte_transparencia_enlaces.aspx?id_entidad=','') # elimina la cadena 'enlaces/...'
                    id_entidad.append(_id) # guarda el id_entidad encontrado
                    name_entidad.append(a.get_text()) # guarda el nombre de la entidad encontrado
        except:
            pass
    # convierte listas en dataframe
    df1 = pd.DataFrame(list(zip(id_entidad,name_entidad)),columns =['id_entidad','name_entidad'])
    BBDD = BBDD.append(df1) # se apendea todo lo guardado a la BBDD
BBDD['id_entidad'] = BBDD['id_entidad'].astype('int')
BBDD.to_excel('{}{}'.format(PATH_OUTPUT,FILE_OUTPUT),index=False,sheet_name='BD') # exporta excel
end = time.time() # para contabilizar tiempo de demora
nseconds = end-start
nseconds=int(nseconds)
print('Segundos transcurridos:',nseconds)