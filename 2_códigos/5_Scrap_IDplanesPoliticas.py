"""
1. Descripción:
    Script que scrapea la web PTE para obtener los documentos y links del apartado 'PLANES Y POLÍTICAS' de la pestaña 'Planeamiento y Organización'
2. Inputs:
    Listado id_entidad
3. Outputs:
    Excel con los campos: "id_entidad", "Institución", "Tipo_de_Instrumento", "Instrumento" y "Link"
4. Supuesto:
    El listado de id_entidad contiene todas las entidades del PTE
"""

# importación de librerías
import requests
import time
import pandas as pd
import re
from bs4 import BeautifulSoup
from datetime import date

# para contabilizar tiempo de demora
start = time.time() # inicia toma de tiempo
today = date.today() # graba día de hoy
d1 = today.strftime("%d_%m_%Y") # da formato

# ----------------- MODIFICABLE
#
# ruta de data scrap
PATH_INPUT = 'C:/Users/ARON SANTA CRUZ/Documents/ceplan/github/proyectoPTE/1_data/2_scrap/'
# nombre del archivo
FILE_OUTPUT = 'PyP_{}.xlsx'.format(d1)
# tiempo de espera para cargar URL
timeout=10
#
# -----------------------------

BBDD = pd.DataFrame() # se crea dataframe vacía para almacenar info
file_xlsx = PATH_INPUT + 'ID_ENTIDAD_TOTAL.xlsx' # ruta y nombre de listado id_entidad
df_xlsx = pd.read_excel(file_xlsx) # lee el excel con el listado id_entidad
entidades = df_xlsx['id_entidad'].tolist() # convierte la columna 'id_entidad' en una lista

# bucle 'for' para todos los elementos de la lista de entidades
for entidad in entidades:
    titInst = [] # crea listas vacías para almacenar info scrapeada
    links = []
    # construye link a explorar (es como entrar al PTE y cliquear la pestaña 'Planeamiento y organización')
    web1 = "https://www.transparencia.gob.pe/enlaces/pte_transparencia_enlaces.aspx?id_entidad="
    web2 = "&id_tema=5"
    URL = web1+str(entidad)+web2
    noConectadoInternet=True # variable para evitar que un corte de internet detenga la ejecución
    # bucle 'while' para que repita el código hasta que noConectadoInternet sea falso
    while (noConectadoInternet):
        # 'try' evita que un error detenga la ejecución
        try:
            reqs = requests.get(URL,timeout=timeout,headers={'Connection':'close'}) # explora el link
            print(entidad) # imprime el id_entidad en la consola
            # si llega a este punto, noConectadoInternet será falso y el while ya no se repetirá
            # esto significa que el requests se pudo ejecutar mientras había conexión
            noConectadoInternet=False
        except (requests.ConnectionError, requests.Timeout):
            noConectadoInternet=True # noConectadoInternet será verdadero para que el while se repita 1 vez más
            print('No conectado. Intentando conectarse...') # mensaje alerta
            print(entidad)
    content = reqs.text # pasa a 'texto' el contenido obtenido por el requests
    soup = BeautifulSoup(content, 'html.parser') # contenido es "partido" en secciones con bs
#    nameInstSucio = soup.find_all("h2", {"class": "esp-title-00"}) # nombre sucio de la institución
#    nameInst = nameInstSucio[0].get_text() # nombre limpio de la institución
    # bucle para todos los elementos 'li' encontrados en el contenido
    for h in soup.findAll('li'):
        a = h.find('a') # dentro de los elementos 'li', buscar el elemento 'a' que contiene texto
        # 'try' evita que un error detenga la ejecución
        try:
            # el elemento 'onmouseover' solo se encuentra en ciertos títulos y subtítulos
            if 'onmouseover' in a.attrs:
                titulo1 = a.get('onmouseover') # el texto dentro del elemento 'onmouseover'
                # solo los títulos 'Instrumentos de Gestión' y 'Planes y Políticas' nos interesan
                if ('Instrumentos de Gestión' in titulo1) or ('Planes y Políticas' in titulo1):
                    titulo1 = titulo1[22:] # es como en excel el EXTRAE(x,23,.)
                    listaTitulo1 = titulo1.split("</b>") # el texto se parte en '</b>'
                    titulo1 = listaTitulo1[0] # la 1ra parte de lo partido es el título
                    titInst.append(titulo1) # se almacena en la lista el título obtenido
                    links.append('') # no se tiene link por lo que se almacena un vacío
            # los títulos y subtítulos que también están en el PTE
            if ('Auditoría' in a.get_text()) or ('Información Adicional' in a.get_text()) or ('AUDITORÍA' in a.get_text()) or ('INFORMACIÓN ADICIONAL' in a.get_text()):
                titulo2 = a.get_text() # guardamos el texto
                titulo2 = re.sub(' +',' ',titulo2) # eliminamos los posibles dobles espacios
                titInst.append(titulo2) # se almacena en la lista el título obtenido
                links.append('') # no se tiene link por lo que se almacena un vacío
            # los links está dentro del elemento 'href'
            if 'href' in a.attrs:
                tit_url = a.get('href') # solo me quedo con el contenido del 'href'
                if 'Javascript: pte_js_enviar_Link' in tit_url:
                    listaURL = tit_url.split(",'") # se parte el texto
                    tit_url2 = listaURL[1] # la 2da parte contiene el nombre del instrumento
                    tit_url2 = tit_url2.replace("'", "") # se remplaza el ' para que no produzca errores
                    url_link = listaURL[2] # la 3ra parte contiene el link del instrumento
                    url_link = url_link.replace("'", "") # se remplaza el ' para que no produzca errores
                    titInst.append(tit_url2) # se almacena en la lista el nombre del instrumento
                    links.append(url_link) # se almacena en la lista el link del instrumento
        # si ocurre un error, pasa no más
        except:
            pass
    df1 = pd.DataFrame(list(zip(titInst, links)),columns =['Instrumento', 'Link']) # convierte listas en dataframe
    df1['Tipo_de_Instrumento'] = None # crea una columna
    # el nombre del instrumento es copiado en el tipo de instrumento solo si es título o subtítulo
    df1.loc[(df1['Instrumento'] == 'Instrumentos de Gestión') | (df1['Instrumento'] == 'Planes y Políticas') | (df1['Instrumento'] == 'Recomendaciones de Auditoría') | (df1['Instrumento'] == 'RECOMENDACIONES DE AUDITORÍA') | (df1['Instrumento'] == 'Información Adicional') | (df1['Instrumento'] == 'INFORMACIÓN ADICIONAL'), 'Tipo_de_Instrumento'] = df1['Instrumento']
    # se llena hacia abajo la información de tipo de instrumento
    df1['Tipo_de_Instrumento'] = df1['Tipo_de_Instrumento'].mask(df1['Tipo_de_Instrumento'].eq('')).ffill()
    # se filtra y solo nos quedamos con el tipo de instrumento 'Planes y Políticas'
    df1 = df1[df1['Tipo_de_Instrumento'] == 'Planes y Políticas']
    df1 = df1[df1['Tipo_de_Instrumento'] != df1['Instrumento']] # elimina casos: título es igual al tipo de instrumento
#    df1['Institución'] = nameInst # se guarda nombre de institución en el dataframe
    df1['id_entidad'] = entidad # se guarda el id_entidad
    BBDD = BBDD.append(df1) # se apendea todo lo guardado a la BBDD
#BBDD = BBDD[["id_entidad", "Institución", "Tipo_de_Instrumento", "Instrumento", "Link"]] # ordena las variables
BBDD = BBDD[["id_entidad", "Tipo_de_Instrumento", "Instrumento", "Link"]] # ordena las variables
BBDD.to_excel('{}{}'.format(PATH_INPUT,FILE_OUTPUT),index=False,sheet_name='BD') # exporta excel
# para contabilizar tiempo de demora
end = time.time() # fin de toma de tiempo
nseconds = end-start # calcula tiempo (segundos)
nseconds=int(nseconds) # se pasa a enteros
print('Segundos transcurridos:',nseconds) # imprime segundos de demora