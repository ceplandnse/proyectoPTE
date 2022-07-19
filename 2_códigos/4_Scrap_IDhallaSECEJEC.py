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
# tiempo de espera para cargar URL
timeout=10
#
# ----------------------------------------------- #

# nombre del archivo
FILE_OUTPUT = 'ID_ENTIDAD_SECEJEC.xlsx'

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

#revisar en unos meses para determinar si siguen sin tener info de sec_ejec
#estos son los casos en los que no tenía información de sec_ejec o, si lo tenía, no identificaba a ninguna UE
BBDD.loc[(BBDD['id_entidad']=="10197"),'sec_ejec']=12
BBDD.loc[(BBDD['id_entidad']=="10198"),'sec_ejec']=1471
BBDD.loc[(BBDD['id_entidad']=="10201"),'sec_ejec']=1703
BBDD.loc[(BBDD['id_entidad']=="10204"),'sec_ejec']=1699
BBDD.loc[(BBDD['id_entidad']=="10205"),'sec_ejec']=1472
BBDD.loc[(BBDD['id_entidad']=="10208"),'sec_ejec']=1465
BBDD.loc[(BBDD['id_entidad']=="10212"),'sec_ejec']=1469
BBDD.loc[(BBDD['id_entidad']=="10213"),'sec_ejec']=1702
BBDD.loc[(BBDD['id_entidad']=="10231"),'sec_ejec']=1474
BBDD.loc[(BBDD['id_entidad']=="10233"),'sec_ejec']=12
BBDD.loc[(BBDD['id_entidad']=="10242"),'sec_ejec']=1704
BBDD.loc[(BBDD['id_entidad']=="10600"),'sec_ejec']=301313
BBDD.loc[(BBDD['id_entidad']=="10808"),'sec_ejec']=300550
BBDD.loc[(BBDD['id_entidad']=="11021"),'sec_ejec']=300754
BBDD.loc[(BBDD['id_entidad']=="11095"),'sec_ejec']=301017
BBDD.loc[(BBDD['id_entidad']=="12886"),'sec_ejec']=1288
BBDD.loc[(BBDD['id_entidad']=="13289"),'sec_ejec']=875
BBDD.loc[(BBDD['id_entidad']=="13296"),'sec_ejec']=1686
BBDD.loc[(BBDD['id_entidad']=="13362"),'sec_ejec']=12
BBDD.loc[(BBDD['id_entidad']=="13363"),'sec_ejec']=12
BBDD.loc[(BBDD['id_entidad']=="13648"),'sec_ejec']=810
BBDD.loc[(BBDD['id_entidad']=="13734"),'sec_ejec']=1210
BBDD.loc[(BBDD['id_entidad']=="13753"),'sec_ejec']=869
BBDD.loc[(BBDD['id_entidad']=="13830"),'sec_ejec']=892
BBDD.loc[(BBDD['id_entidad']=="13843"),'sec_ejec']=818
BBDD.loc[(BBDD['id_entidad']=="13992"),'sec_ejec']=1683
BBDD.loc[(BBDD['id_entidad']=="14060"),'sec_ejec']=892
BBDD.loc[(BBDD['id_entidad']=="14062"),'sec_ejec']=892
BBDD.loc[(BBDD['id_entidad']=="14214"),'sec_ejec']=921
BBDD.loc[(BBDD['id_entidad']=="14250"),'sec_ejec']=1398
BBDD.loc[(BBDD['id_entidad']=="14278"),'sec_ejec']=1684
BBDD.loc[(BBDD['id_entidad']=="14280"),'sec_ejec']=1404
BBDD.loc[(BBDD['id_entidad']=="14287"),'sec_ejec']=1395
BBDD.loc[(BBDD['id_entidad']=="14307"),'sec_ejec']=1375
BBDD.loc[(BBDD['id_entidad']=="15325"),'sec_ejec']=1517
BBDD.loc[(BBDD['id_entidad']=="15326"),'sec_ejec']=1403
BBDD.loc[(BBDD['id_entidad']=="15331"),'sec_ejec']=1513
BBDD.loc[(BBDD['id_entidad']=="15346"),'sec_ejec']=988
BBDD.loc[(BBDD['id_entidad']=="15350"),'sec_ejec']=1378
BBDD.loc[(BBDD['id_entidad']=="15353"),'sec_ejec']=1643
BBDD.loc[(BBDD['id_entidad']=="15354"),'sec_ejec']=1493
BBDD.loc[(BBDD['id_entidad']=="16358"),'sec_ejec']=1618
BBDD.loc[(BBDD['id_entidad']=="16364"),'sec_ejec']=1308
BBDD.loc[(BBDD['id_entidad']=="16374"),'sec_ejec']=1483
BBDD.loc[(BBDD['id_entidad']=="16383"),'sec_ejec']=1524
BBDD.loc[(BBDD['id_entidad']=="16399"),'sec_ejec']=1505
BBDD.loc[(BBDD['id_entidad']=="17400"),'sec_ejec']=1339
BBDD.loc[(BBDD['id_entidad']=="17409"),'sec_ejec']=1537
BBDD.loc[(BBDD['id_entidad']=="17415"),'sec_ejec']=896
BBDD.loc[(BBDD['id_entidad']=="17504"),'sec_ejec']=1377
BBDD.loc[(BBDD['id_entidad']=="17506"),'sec_ejec']=1386
BBDD.loc[(BBDD['id_entidad']=="18611"),'sec_ejec']=1434
BBDD.loc[(BBDD['id_entidad']=="18612"),'sec_ejec']=1248
BBDD.loc[(BBDD['id_entidad']=="18613"),'sec_ejec']=1610
BBDD.loc[(BBDD['id_entidad']=="18617"),'sec_ejec']=1686
BBDD.loc[(BBDD['id_entidad']=="18624"),'sec_ejec']=1518
BBDD.loc[(BBDD['id_entidad']=="18632"),'sec_ejec']=1436
BBDD.loc[(BBDD['id_entidad']=="18659"),'sec_ejec']=1600
BBDD.loc[(BBDD['id_entidad']=="18664"),'sec_ejec']=301284
BBDD.loc[(BBDD['id_entidad']=="18667"),'sec_ejec']=1355
BBDD.loc[(BBDD['id_entidad']=="18673"),'sec_ejec']=1525
BBDD.loc[(BBDD['id_entidad']=="18674"),'sec_ejec']=1599
BBDD.loc[(BBDD['id_entidad']=="18675"),'sec_ejec']=1656
BBDD.loc[(BBDD['id_entidad']=="18684"),'sec_ejec']=934
BBDD.loc[(BBDD['id_entidad']=="18689"),'sec_ejec']=724
BBDD.loc[(BBDD['id_entidad']=="18691"),'sec_ejec']=1676
BBDD.loc[(BBDD['id_entidad']=="18692"),'sec_ejec']=1538
BBDD.loc[(BBDD['id_entidad']=="18708"),'sec_ejec']=1523
BBDD.loc[(BBDD['id_entidad']=="18721"),'sec_ejec']=1353
BBDD.loc[(BBDD['id_entidad']=="18730"),'sec_ejec']=1606
BBDD.loc[(BBDD['id_entidad']=="18734"),'sec_ejec']=1379
BBDD.loc[(BBDD['id_entidad']=="18786"),'sec_ejec']=301884
BBDD.loc[(BBDD['id_entidad']=="18818"),'sec_ejec']=1701
BBDD.loc[(BBDD['id_entidad']=="18823"),'sec_ejec']=1440
BBDD.loc[(BBDD['id_entidad']=="18827"),'sec_ejec']=1540
BBDD.loc[(BBDD['id_entidad']=="18837"),'sec_ejec']=1542
BBDD.loc[(BBDD['id_entidad']=="18840"),'sec_ejec']=1453
BBDD.loc[(BBDD['id_entidad']=="18849"),'sec_ejec']=1325
BBDD.loc[(BBDD['id_entidad']=="18854"),'sec_ejec']=1325
BBDD.loc[(BBDD['id_entidad']=="19857"),'sec_ejec']=1726
BBDD.loc[(BBDD['id_entidad']=="19858"),'sec_ejec']=1348
BBDD.loc[(BBDD['id_entidad']=="22865"),'sec_ejec']=1514
BBDD.loc[(BBDD['id_entidad']=="22869"),'sec_ejec']=1718
BBDD.loc[(BBDD['id_entidad']=="26886"),'sec_ejec']=1387
BBDD.loc[(BBDD['id_entidad']=="35906"),'sec_ejec']=1389

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