"""
1. Descripción:
    Script que hace merge entre 3 bases: Planes y Políticas (ver 5_Scrap_IDplanesPoliticas.py); nombre de la institución (3_merge_ListasPTE_Correlativo.py); SECEJEC (ver 4_Scrap_IDhallaSECEJEC.py). Elabora un excel con el nombre de la institución y los campos de Planes y Políticas
2. Inputs:
    PyP_{}.xlsx
    ID_ENTIDAD_SECEJEC.xlsx
    ID_ENTIDAD_TOTAL.xlsx
3. Outputs:
    Excel con los campos: "sec_ejec", variables de presupuesto y planes/políticas PTE
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
# ruta de data scrap
PATH_INPUT = 'C:/Users/ARON SANTA CRUZ/Documents/ceplan/github/proyectoPTE/1_data/2_scrap/'
# ruta de resultados
PATH_RESULT = 'C:/Users/ARON SANTA CRUZ/Documents/ceplan/github/proyectoPTE/3_resultados/'
# fecha de planes y politicas
FECHA_PyP = '01_07_2022'
#
# ----------------------------------------------- #

# nombre del archivo
FILE_OUTPUT = 'PLANES_POLITICAS_'+FECHA_PyP+'.xlsx'

# lee el excel
df_pp=pd.read_excel(PATH_INPUT+'PyP_'+FECHA_PyP+'.xlsx') # planes y políticas
df_se=pd.read_excel(PATH_INPUT+'ID_ENTIDAD_SECEJEC.xlsx') # sec_ejec
df_ne=pd.read_excel(PATH_INPUT+'ID_ENTIDAD_TOTAL.xlsx') # nombre de la entidad

# merge las datas
df_fin=pd.merge(df_pp,df_se,on=["id_entidad"],how='left') # merge entre data frames
df_fin=pd.merge(df_fin,df_ne,on=["id_entidad"],how='left') # merge entre data frames

# elimina datas usadas
del df_pp
del df_se
del df_ne

# ordena variables
df_fin=df_fin[['sec_ejec','TIPO_NG','TIPO_GN','SECTOR','SECTOR_NOMBRE','PLIEGO','PLIEGO_NOMBRE','EJECUTORA_NOMBRE','TIPO_MUNICIPALIDAD','DEPARTAMENTO_EJECUTORA','DEPARTAMENTO_EJECUTORA_NOMBRE','PROVINCIA_EJECUTORA','PROVINCIA_EJECUTORA_NOMBRE','DISTRITO_EJECUTORA','DISTRITO_EJECUTORA_NOMBRE','id_entidad','name_entidad','Tipo_de_Instrumento','Instrumento','Link']]

# ordena de menor a mayor los id_entidad
df_fin=df_fin.sort_values(by=['id_entidad'])

# renombra las columnas
df_fin.columns=['Código UE (sec_ejec)','Nivel de Gobierno','Gobierno Nacional','Código Sector','Nombre Sector','Código Pliego','Nombre Pliego','Nombre Ejecutora','Municipalidad','Código Dpto.','Nombre Departamento','Código Provincia','Nombre Provincia','Código Distrito','Nombre Distrito','Código PTE (id_entidad)','Nombre de Institución','Tipo de Instrumento','Instrumento','Link']

# exporta a excel
df_fin.to_excel('{}{}'.format(PATH_RESULT,FILE_OUTPUT),index=False,sheet_name='BD') # exporta excel