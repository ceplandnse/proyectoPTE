"""
1. Descripción:
    Script que scrapea la web PTE para obtener el código de UE (sec_ejec) para cada id_entidad
2. Inputs:
    Listado id_entidad
3. Outputs:
    Excel con los campos: "id_entidad" y "sec_ejec"
4. Supuesto:
    El listado de id_entidad contiene todas las entidades del PTE
"""

# importación de librerías
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

# para contabilizar tiempo de demora
start = time.time() # inicia toma de tiempo

# ----------------- MODIFICABLE ----------------- #
#
# ruta de data interna
PATH_INSIDE = 'C:/Users/ARON SANTA CRUZ/Documents/ceplan/github/proyectoPTE/1_data/1_interna/'
# ruta de data scrap
PATH_INPUT = 'C:/Users/ARON SANTA CRUZ/Documents/ceplan/github/proyectoPTE/1_data/2_scrap/'
# nombre del archivo
FILE_OUTPUT = 'ID_ENTIDAD_SECEJEC.xlsx'
# tiempo de espera para cargar URL
timeout=10
#
# ----------------- MODIFICABLE ----------------- #

BBDD = pd.DataFrame() # se crea dataframe vacía para almacenar info
file_xlsx = PATH_INPUT + 'ID_ENTIDAD_TOTAL.xlsx' # ruta y nombre de listado id_entidad
df_xlsx = pd.read_excel(file_xlsx) # lee el excel con el listado id_entidad
entidades = df_xlsx['id_entidad'].tolist() # convierte la columna 'id_entidad' en una lista

# bucle 'for' para todos los elementos de la lista de entidades
for entidad in entidades:
    # construye link a explorar (es como entrar al PTE y cliquear la pestaña 'Presupuesto')
    web1 = "https://www.transparencia.gob.pe/reportes_directos/pte_transparencia_info_finan.aspx?id_entidad="
    web2 = "&id_tema=19"
    URL = web1+str(entidad)+web2
    # crea listas vacías para almacenar info scrapeada
    id_entidad = []
    sec_ejec = []
#    name_entidad = []
    # variable para evitar que un corte de internet detenga la ejecución
    noConectadoInternet=True
    # bucle 'while' para que repita el código hasta que noConectadoInternet sea falso
    while (noConectadoInternet):
        # 'try' evita que un error detenga la ejecución
        try:
            reqs = requests.get(URL,timeout=timeout,headers={'Connection':'close'}) # explora el link
            print(entidad) # imprime el id_entidad en la consola
            # si llega a este punto, noConectadoInternet será falso y el while ya no se repetirá
            # esto significa que el requests se pudo ejecutar mientras había conexión
            noConectadoInternet=False
        # si hay algún error con la conexión se ejecuta este bloque
        except (requests.ConnectionError, requests.Timeout):
            noConectadoInternet=True # noConectadoInternet será verdadero para que el while se repita 1 vez más
            print('No conectado. Intentando conectarse...') # mensaje alerta
            print(entidad)
    content = reqs.text # pasa a 'texto' el contenido obtenido por el requests
    soup = BeautifulSoup(content, 'html.parser') # contenido es "partido" en secciones con bs
#    nameInstSucio = soup.find_all("h2", {"class": "esp-title-00"}) # nombre sucio de la institución
    # nombre de la institución
#    nameInst = ''
#    nameInst = nameInstSucio[0].get_text() # nombre limpio
    obj_link = soup.find("object") # el elemento de tipo 'object' contiene el cuadro de info presupuestal
    # nombre del sec_ejec
    secejec = ''
    secejec = obj_link.get('data') # nombre sucio
    secejec = secejec.replace('https://apps5.mineco.gob.pe/temp/pte/InformacionPresupuestal.aspx?sec_ejec=','') # nombre limpio
    id_entidad = [entidad] # se graba informacion de id_entidad
    sec_ejec = [secejec] # se graba informacion sec_ejec
#    name_entidad = [nameInst] # se graba nombre de la institucion
    # convierte listas en dataframe
#    df1 = pd.DataFrame(list(zip(id_entidad,sec_ejec,name_entidad)),columns=['id_entidad','sec_ejec','name_entidad'])
    df1 = pd.DataFrame(list(zip(id_entidad,sec_ejec)),columns=['id_entidad','sec_ejec'])
    BBDD = BBDD.append(df1) # se apendea todo lo guardado a la BBDD
BBDD['sec_ejec'] = BBDD['sec_ejec'].astype('int') # transforma a entero el string
df_UE=pd.read_excel(PATH_INSIDE+'UE_SIAF_2022_al_06.06.2022.xlsx',sheet_name='UE') # lee el excel con info UE
df_UE=df_UE.rename(columns={'EJECUTORA':'sec_ejec'}) # renombra columna sec_ejec
df_final=pd.merge(BBDD, df_UE, on=["sec_ejec"], how='left') # merge entre data frames
df_final=df_final[~(df_final['sec_ejec'].isnull())]
del df_final['ANO_EJE']
del df_final['MONTO_PIA']
del df_final['MONTO_PIM']
df_final.to_excel('{}{}'.format(PATH_INPUT,FILE_OUTPUT),index=False,sheet_name='BD') # exporta excel

# para contabilizar tiempo de demora
end = time.time() # fin de toma de tiempo
nseconds = end-start # calcula tiempo (segundos)
nseconds=int(nseconds) # se pasa a enteros
print('Segundos transcurridos:',nseconds) # imprime segundos de demora