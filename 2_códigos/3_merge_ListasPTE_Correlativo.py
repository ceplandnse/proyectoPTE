"""
1. Descripción:
    Script que hace merge entre los ID_ENTIDAD de las listas (ver 1_previoScrap_ListasPTE.py) y del correlativo (ver 2_previoScrap_Correlativo.py). Elabora un excel con los id_entidad y el nombre de la entidad final
2. Inputs:
    ID_ENTIDAD_LISTAS_{}.xlsx
    ID_ENTIDAD_CORRELATIVO_{}.xlsx
3. Outputs:
    Excel con los campos: "id_entidad" y "name_entidad"
4. Supuesto:
    NaN
"""

# importación de librerías
import time
import pandas as pd

# para contabilizar tiempo de demora
start = time.time()

# ----------------- MODIFICABLE ----------------- #
#
# ruta de data interna
PATH_INSIDE = 'C:/Users/ARON SANTA CRUZ/Documents/ceplan/github/proyectoPTE/1_data/1_interna/'
# ruta de data scrap
PATH_INPUT = 'C:/Users/ARON SANTA CRUZ/Documents/ceplan/github/proyectoPTE/1_data/2_scrap/'
# ruta de resultados
PATH_RESULT = 'C:/Users/ARON SANTA CRUZ/Documents/ceplan/github/proyectoPTE/3_resultados/'
#
# ----------------------------------------------- #

# nombre del archivo
FILE_OUTPUT = 'ID_ENTIDAD_TOTAL.xlsx'

# lee el excel con el listado id_entidad
df_listas=pd.read_excel(PATH_INPUT+'ID_ENTIDAD_LISTAS_21_06_2022.xlsx')
df_listas=df_listas.rename(columns={'name_entidad':'ne_listas'})

# lee el excel con el listado id_entidad
df_correlativo=pd.read_excel(PATH_INPUT+'ID_ENTIDAD_CORRELATIVO_21_06_2022.xlsx')
df_correlativo=df_correlativo.rename(columns={'name_entidad':'ne_correlativo'})

# merge entre las 2 dataframe
df_total=pd.merge(df_listas, df_correlativo, how="outer", on=["id_entidad"])

# todo pasa a mayusculas
df_total['ne_listas']=df_total['ne_listas'].str.upper()
df_total['ne_correlativo']=df_total['ne_correlativo'].str.upper()

# limpia dobles espacios
df_total['ne_listas']=df_total['ne_listas'].str.replace(' +', ' ')
df_total['ne_correlativo']=df_total['ne_correlativo'].str.replace(' +', ' ')

# limpia espacios al inicio o al final
df_total=df_total.replace(r"^ +| +$", r"", regex=True)

# verifica los casos en los que los nombres segun lista y los nombres segun correlativo difieren
df_total.loc[(df_total['ne_listas']!=df_total['ne_correlativo']) & (df_total['ne_listas'].notnull()) & (df_total['ne_correlativo'].notnull()),'compara']='Diferentes'
df_dif=df_total[df_total['compara']=='Diferentes'] # checa si todo ok

# elimina df de verificacion
del df_dif
del df_total['compara']

# armamos la columna name_entidad con los valores de correlativo y lista
df_total['name_entidad']=df_total['ne_correlativo']
df_total.loc[(df_total['ne_correlativo'].isnull()) & (df_total['ne_correlativo'].notnull()),'name_entidad']=df_total['ne_listas']

# elimina columnas temporales
del df_total['ne_listas']
del df_total['ne_correlativo']

# exporta excel
df_total.to_excel(PATH_INPUT+FILE_OUTPUT,index=False,sheet_name='BD')