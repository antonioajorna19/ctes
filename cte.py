import requests
import os
import shutil


NOMBRE_ARCHIVO = "shipments.txt" #hus.txt o shipments.txt
FORMATO_ARCHIVO = "pdf" #pdf/xml
NOMBRE_CARPETA_DE_DESCARGA = "prueba" #ctes o CTES o como quieran

def Validating_HU(data:str):

    '''
    PRE:Recibimos el Dato, contamos las cantidades de digitos para identificar HU'S
    POST: 
    '''
    text = [char for char in data]

    if len(text) < 15 :
        IsHU = False
    else:
        IsHU = True
    
    return IsHU


def leer_archivo(nombre_archivo:str) ->None:
    """
    PRE:Se recibe el nombre del archivo a procesar.
    POST:Se retorna como lista los ids de CTES a procesar.
    """
    listado_hus = list()
    listado_shipments_limpios = list()

    with open(nombre_archivo,"r") as archivo:
        for linea in archivo:
            if not Validating_HU(linea.strip("\n")):
               listado_shipments_limpios.append(linea.strip("\n"))
            else:
                listado_hus.append(linea.strip("\n"))
        if listado_hus != 0:
            obtener_shipments_de_hus(listado_hus,listado_shipments_limpios)
    return listado_shipments_limpios



def obtener_ctes(listado_shipments:list, nombre_carpeta:str, shipments_sin_cte:list) ->None:
    """
    PRE:Recibimos como lista todos los shipments ademas de el nombre de la carpeta donde se descargaran las NF de los SH.
    POST:Al ser un procedimiento, se retorna un dato de tipo None.
    """
    #colocar los try correspondientes a la conexion con la api
    
    os.mkdir(nombre_carpeta)
    for id_shipment in listado_shipments:

        try:
            obtener_cte = requests.get(f"https://internal-api.mercadolibre.com/shipping-tax/gateway/shipments/{id_shipment}/download?doctype={FORMATO_ARCHIVO}&caller.id=admin&caller.scopes=admin")
            with open(f"{nombre_carpeta}\\{id_shipment}.{FORMATO_ARCHIVO}","wb") as cte_descargado:
                cte_descargado.write(obtener_cte.content)
        except Exception:
            shipments_sin_cte.append(id_shipment)
    
    print("Obteniendos notas fiscales")


def comprimir_carpeta(nombre_carpeta:str) ->None:
    """
    PRE:Se recibe el nombre de la carpeta a comprimir.
    POST:Una vez comprimida, se retorna un dato de tipo None, esto debido a ser un procedimiento.
    """

    shutil.make_archive(nombre_carpeta,"zip",nombre_carpeta)


def mostrar_shipments_sin_cte(shipments_sin_cte:list) ->None:

    '''PRE:OBTENEMOS LOS SHIPMENTS SIN CTE EN UNA LISTA.
       POST:AL SER UN PROCEDIMIENTO SE RETORNA UN DATO DE TIPO NONE.'''


    if len(shipments_sin_cte) == 0:
        print("se descargaron todos los ctes exitosamente")
    
    else:
        print("SHIPMENTS SIN CTES")
        for shipment in shipments_sin_cte:
            print(shipment)



def obtener_shipments_de_hus(listado_hus:list, listado_shipments:list) ->None:
    """
    PRE:Recibimos el listado de ctes y el de los shipments(vacio), buscamos obtener los shipments de estos ctes.
    POST:Una vez agregados los shipments de cada cte, se retorna un valor None, dado que es un procedimiento.
    """
    
    for hu_id in listado_hus:
        informacion_hu = requests.get(f"http://internal-api.mercadolibre.com/tms-mlb/outbounds/{hu_id}/internal")
        data_hu_formateada = informacion_hu.json()
        data_shipment = data_hu_formateada["shipments"]

        for shipment_id in data_shipment:
            listado_shipments.append(shipment_id["id"])
    
    print("Obteniendo shipments.")


def main() ->None:

    shipments_sin_cte = list()
    Listado_shipments = leer_archivo(NOMBRE_ARCHIVO)

    obtener_ctes(Listado_shipments,NOMBRE_CARPETA_DE_DESCARGA,shipments_sin_cte)
 
    comprimir_carpeta(NOMBRE_CARPETA_DE_DESCARGA)
    mostrar_shipments_sin_cte(shipments_sin_cte)
    print("Hemos finalizado")


main()
