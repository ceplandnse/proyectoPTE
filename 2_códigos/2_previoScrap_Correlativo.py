"""
1. Descripción:
    Script que scrapea el PTE intentando con un correlativo del 0 al 39999* para el id_entidad y elabora un excel con los id_entidad y el nombre de la entidad
    * se coloca 39999 porque los id_entidad obtenidos en el scrap de las listas del PTE (ver 1_previoScrap_ListasPTE.py) son menores a 39999
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
FILE_OUTPUT = 'ID_ENTIDAD_CORRELATIVO_{}.xlsx'.format(d1)
# id inicio
ID_INICIO = 0
# id final
ID_FINAL = 39999
# tiempo de espera para cargar URL
timeout=10
#
# ----------------- MODIFICABLE ----------------- #

BBDD = pd.DataFrame() # se crea dataframe vacía para almacenar info
# bucle 'for' para el rango de correlativo definido
for entidad in range(ID_INICIO, ID_FINAL + 1):
    # construye link a explorar
    web1 = "https://www.transparencia.gob.pe/enlaces/pte_transparencia_enlaces.aspx?id_entidad="
    URL = web1+str(entidad)
    id_entidad = [] # crea listas vacías para almacenar info scrapeada
    name_entidad = []
    # variable para evitar que un corte de internet detenga la ejecución
    noConectadoInternet=True
    while (noConectadoInternet):
        try:
            reqs = requests.get(URL)  # explora el link
            noConectadoInternet=False
        except:
            noConectadoInternet=True # noConectadoInternet será verdadero para que el while se repita 1 vez más
            print('No conectado. Intentando conectarse...') # mensaje alerta
    content = reqs.text # pasa a 'texto' el contenido obtenido por el requests
    soup = BeautifulSoup(content, 'html.parser') # contenido es "partido" en secciones con bs
    nameInstSucio = soup.find_all("h2", {"class": "esp-title-00"}) # encuentra todos los elementos 'h2'
    nameInst = nameInstSucio[0].get_text() # transforma a texto el nombre de la institución
    # si el nombre de la institución no está en blanco (id_entidad válido), se ejecuta el guardado
    if (nameInst!=''):
        id_entidad = [entidad] # guarda los elementos en las listas
        name_entidad = [nameInst]
        # convierte listas en dataframe
        df1 = pd.DataFrame(list(zip(id_entidad,name_entidad)),columns=['id_entidad','name_entidad'])
        BBDD = BBDD.append(df1) # se apendea todo lo guardado a la BBDD
BBDD.to_excel('{}{}'.format(PATH_OUTPUT,FILE_OUTPUT),index=False,sheet_name='BD') # exporta excel
end = time.time() # para contabilizar tiempo de demora
nseconds = end-start
nseconds=int(nseconds)
print('Segundos transcurridos:',nseconds)