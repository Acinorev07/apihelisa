from hooks.configuracion_APIs import obtener_url
from hooks.date import dateMillisec
from api.helisa.route import POST

def obtener_saldos_cuenta():


    url = obtener_url(
                "helisa",
                "thirdPartyFromAccount"
            )
    
    # Epoch en milisegundos
    fecha_consulta = input(
        "Fecha de consulta (DD-MM-YYYY, ENTER = hoy): "
    )
                    
    date = dateMillisec(fecha_consulta)
    
    # Pedir al usuario la cuenta contable a consultar
    cuenta = input("cuenta contable: ")
                
    # IMPORTANTE:
    # La firma se calcula sobre ESTE STRING exacto.
    json_data = (
        '{"date":' + str(date) +
        ',"account":"' + cuenta + '"}'
    )
    
    print("Estamos en la opción 2 url: ",url)
    print("Estamos en la opción 2 json_data: ",json_data)
    
    response = POST(
        url, 
        json_data
        )
    
                    
    
    if response is not None:

        return response