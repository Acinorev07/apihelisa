# Testear que la partida doble se cumpla
# from services.accounting import validar_asiento
from decimal import Decimal


# movimientos = [
#     {
#         "cuenta": "11201001",
#         "naturaleza": "D",
#         "valor": "397000"
#     },
#     {
#         "cuenta": "13050537",
#         "naturaleza": "C",
#         "valor": "384808"
#     },
#     {
#         "cuenta": "28150609",
#         "naturaleza": "C",
#         "valor": "12692"
#     },
#     {
#         "cuenta": "110505",
#         "naturaleza": "D",
#         "valor": "500"
#     }
# ]

# resultado = validar_asiento(movimientos)

# print(resultado)



# Testear que el saldo de una factura se halle correctamente
# from services.accounting import calcular_saldo_pendiente

# # Caso 1: pago completo
# saldo = calcular_saldo_pendiente(
#     valor_factura=2797000,
#     descuento=200000,
#     abonos_capital=2597000
# )
# print("Pago completo:", saldo)

# # Caso 2: pago parcial
# saldo = calcular_saldo_pendiente(
#     valor_factura=2797000,
#     descuento=200000,
#     abonos_capital=597000
# )
# print("Pago parcial:", saldo)

# # Caso 3: no hay abonos
# saldo = calcular_saldo_pendiente(
#     valor_factura=2797000,
#     descuento=200000,
#     abonos_capital=0
# )
# print("Sin abonos:", saldo)


# Testear que la se forme el asiento contable de cada factura de forma correcta segun sus parametros

from services.accounting import generar_asiento_factura
from services.accounting import convertir_a_movimientos_helisa
from datetime import date
import json

from services.accounting import construir_documento_helisa

# factura = {
#     "numero": "00003413",
#     "valor": "2797000",
#     "descuento": "200000",
#     "cuenta_cartera": "13050537",
#     "pagos": [
#         {
#             "recibo": "RC001",
#             "cuenta": "11201001",
#             "valor": "597000",
#         }
#     ],
# }

# factura = {
#     "numero": "00003413",
#     "nit": "900123456",  # Ejemplo ficticio
#     "centro_costo": "061002",
#     "usuario": 1,
#     "valor": "2797000",
#     "descuento": "200000",
#     "cuenta_cartera": "13050537",
#     "pagos": [
#         {
#             "recibo": "RC001",
#             "cuenta": "11201001",
#             "valor": "597000"
#         }
#     ]
# }

# factura = {
#     "Numero_factura": "string",
#     "Consecutivo_factura": 0,
#     "Consecutivo_resolucion": 0,
#     "Numero_resolucion": "string",
#     "Prefijo_resolucion": "string",
#     "Fecha_factura": "string",
#     "Fecha_resolucion": "string",
#     "Fecha_anulacion": "string",
#     "Consecutivo_periodo": 0,
#     "Nombre_periodo": "string",
#     "Valor_total": 0,
#     "Codigo_estudiante": "string",
#     "Nombre_completo_estudiante": "string",
#     "Numero_identificacion_estudiante": "string",
#     "Consecutivo_tercero": 0,
#     "Nombre_completo_tercero": "string",
#     "Numero_identificacion_tercero": "string",
#     "Observaciones": "string",
#     "Codigo_cajero": "string",
#     "Numero_identificacion_cajero": "string",
#     "Nombre_cajero": "string",
#     "Valor_pagado": 0,
#     "Valor_pendiente": 0,
#     "Estado_factura": "string",
#     "Anulada": False,
#     "Justificacion_anulacion": "string",
#     "Paz_y_salvo": False,
#     "Direccion_factura": "string",
#     "Telefono_factura": "string",
#     "Codigo_municipio_factura": "string",
#     "Productos": [{
#         "Consecutivo_periodo": 0,
#         "Nombre_periodo": "string",
#         "Codigo_producto": "string",
#         "Nombre_producto": "string",
#         "Valor_unidad": 0,
#         "Cantidad": 0,
#         "Consecutivo_descuento": 0.366641743483103,
#         "Nombre_descuento": "string",
#         "Valor_descuento": 0,
#         "Consecutivo_impuesto": 0.585762213020101,
#         "Nombre_impuesto": "string",
#         "Porcentaje_impuesto": 0,
#         "Valor_impuesto": 0,
#         "Valor_a_pagar": 0
#     }],
#     "Notas_credito": [{
#         "Consecutivo_nota_credito": 0,
#         "Consecutivo_nota_credito_factura": 0,
#         "Numero_nota_credito": 0,
#         "Fecha": "string",
#         "Valor": 0,
#         "Observaciones": "string",
#         "Estado_nota_credito": "string",
#         "Valor_disponible": 0
#     }],
#     "Retenciones": [{
#         "Consecutivo_retencion_factura": 0,
#         "Consecutivo_factura": 0,
#         "Consecutivo_retencion": 0,
#         "Fecha": "string",
#         "Valor": 0,
#         "Codigo_cajero": "string"
#     }],
#     "Pagos": [{
#         "Numero_recibo_pago": 0,
#         "Fecha_pago": "string",
#         "Valor": 0,
#         "Estado_pago": "string"
#     }]
# }




# resultado = generar_asiento_factura(factura)

# print("\n--- CONTROL DEL ASIENTO ---")
# print("Factura:", resultado.get("factura"))
# print("Saldo pendiente:", resultado.get("saldo_pendiente"))

# movimientos_auxiliares = [
#     m for m in resultado.get("movimientos", [])
#     if m.get("cuenta") == "28150609"
# ]

# print("Cantidad de movimientos 28150609:",
#       len(movimientos_auxiliares))

# for movimiento in movimientos_auxiliares:
#     print(
#         movimiento["cuenta"],
#         movimiento["naturaleza"],
#         movimiento["valor"]
#     )

# print("Validación:", resultado.get("validacion"))
# print("--- FIN DEL CONTROL ---\n")

#***************************************************************************************************
#  Aqui creamos un documento valido para helisa, solo debemos modificarlo segun las reglas_contables

# if "movimientos" not in resultado:
#     print("Error:", resultado["mensaje"])
# else:
#     print("\nMovimientos contables:")

#     for movimiento in resultado["movimientos"]:
#         naturaleza = movimiento["naturaleza"]
#         valor = movimiento["valor"]

#         print(
#             f"Cuenta: {movimiento['cuenta']} | "
#             f"Naturaleza: {naturaleza} | "
#             f"Valor: ${valor:,.0f}"
#         )

#     if "movimientos" in resultado:
#         transacciones = convertir_a_movimientos_helisa(
#             resultado,
#             factura
#         )

#         for transaccion in transacciones:
#             print(
#                 transaccion["account"],
#                 transaccion["nature"]["tag"],
#                 transaccion["value"],
#                 transaccion["idThirdParty"]
#             )

#         print("\n--- CONTROL COMPLETO DE LA CONVERSIÓN ---")

#         print("Cantidad original:", len(resultado["movimientos"]))
#         print("Cantidad convertida:", len(transacciones))

#         for i, transaccion in enumerate(transacciones, start=1):
#             print(
#                 f"{i}. Cuenta={transaccion['account']} | "
#                 f"Naturaleza={transaccion['nature']['tag']} | "
#                 f"Valor={transaccion['value']} | "
#                 f"NIT={transaccion['idThirdParty']}"
#             )

#         print("--- FIN DEL CONTROL ---\n")
#     else:
#         print("Error:", resultado["mensaje"])

#     print("\nSaldo pendiente:", resultado["saldo_pendiente"])
#     print("Validación:", resultado["validacion"]["mensaje"])
#     print("¿Está balanceado?:", resultado["validacion"]["valido"])


# documento = construir_documento_helisa(
#     asiento=resultado,
#     factura=factura,
#     fecha=date(2026, 10, 11),
#     tipo_documento="NIED"  # Solo ejemplo: confirma el código real
# )

# print("\nDocumento completo para Helisa:")
# print(json.dumps(
#     documento,
#     indent=4,
#     ensure_ascii=False
# ))

# ****************************************************************************************************

# from utils.apiFacturasQ10 import consultar_facturas
# Llamamos las facturas 

# facturas = consultar_facturas()

# print(facturas)

# from hooks.configuracion_APIs import obtener_url
# from hooks.date import dateMillisec
# from api.q10.route import GET
# from api.helisa.route import GET_TERCERO
# import json


# url = obtener_url(
#     "q10",
#     "facturas"
# )

# parametros = {
#     'Fecha_inicio':'2026-10-15',
#     'Fecha_fin':'2026-10-15',
#     'offset':0,
#     'Limit': 100
# }

# response = GET(url, params = parametros)

# if response is not None:
#     print("\nCódigo HTTP:", response.status_code)
#     print("\nRespuesta de Q10:")

#     try:

        # respuesta = json.dumps(
        #     response.json(),
        #     indent=4,
        #     ensure_ascii=False,
        # )

        # print(respuesta)

        # datos = response.json()

        # print("Cantidad de facturas:", len(datos))

        
        # cedulas = []

        # no_existe = []

        # for factura in datos:

            # numero = factura["Numero_factura"]
            # nombre = factura["Nombre_completo_estudiante"]
            # valor = factura["Valor_total"]
            # estado = factura["Estado_factura"]

            # print(
            #     f"Factura: {numero} | "
            #     f"Estudiante: {nombre} | "
            #     f"Valor: ${valor:,.0f} | "
            #     f"Estado: {estado}"
            # )

            # # Recorrer los productos de esta factura
            # for producto in factura["Productos"]:
            #     print(
            #         "Producto:", producto["Nombre_producto"],
            #         "| Código:", producto["Codigo_producto"],
            #         "| Valor:", producto["Valor_a_pagar"]
            #     )

            # # Recorrer los pagos de esta factura
            # for pago in factura["Pagos"]:
            #     print(
            #         "Recibo:", pago["Numero_recibo_pago"],
            #         "| Fecha:", pago["Fecha_pago"],
            #         "| Valor:", pago["Valor"],
            #         "| Estado:", pago["Estado_pago"]
            #     )

#             id_tercero = factura["Numero_identificacion_estudiante"]

#             if id_tercero is not "null":
#                  cedulas.append(id_tercero)


#         print(cedulas)


#         fecha = parametros["Fecha_inicio"]
#         year = "2026" 
#         date = dateMillisec(fecha)
#         for di in cedulas:
#             payload = f"{year}|{di}|{date}"

#             response = GET_TERCERO(
#                 url, 
#                 payload,
#                 year,
#                 di,
#                 date
#                 )
            
#             if response is not None:
#                 print("\nCódigo HTTP:", response.status_code)
#                 print("\nRespuesta de Helisa:")

#                 try:
            
#                      resp =  json.dumps(
#                             response.json(),
#                             indent=4,
#                             ensure_ascii=False,
#                         )

#                      if resp is None:
#                           no_existe.append(resp)
        
#                 except ValueError:
#                     print(response.text)



        
#     except ValueError:
#             print(response.text)

# else:

#     print("errrroooor")



from hooks.configuracion_APIs import obtener_url
from hooks.date import dateMillisec
from api.q10.route import GET
from api.helisa.route import GET_TERCERO
from datetime import datetime
import json


# -----------------------------------------
# 1. Consultar facturas de Q10
# -----------------------------------------

url_q10 = obtener_url("q10", "facturas")
url_helisa = obtener_url("helisa", "thirdParty2_0")

parametros = {
    "Fecha_inicio": "2026-10-23",
    "Fecha_fin": "2026-10-23",
    "Offset": 0,
    "Limit": 100,
}

response_q10 = GET(url_q10, params=parametros)

if response_q10 is None:
    print("No se recibió respuesta de Q10.")
    raise SystemExit

if response_q10.status_code != 200:
    print("Error consultando Q10:", response_q10.status_code)
    print(response_q10.text)
    raise SystemExit

try:
    datos = response_q10.json()
except ValueError:
    print("Q10 no devolvió un JSON válido.")
    print(response_q10.text)
    raise SystemExit

if not isinstance(datos, list):
    print("La respuesta de Q10 no es una lista de facturas.")
    raise SystemExit


print("Cantidad de facturas:", len(datos))


# -----------------------------------------
# 2. Extraer cédulas únicas
# -----------------------------------------

cedulas = set()

for factura in datos:
    id_tercero = factura.get("Numero_identificacion_estudiante")

    if id_tercero is not None:
        id_tercero = str(id_tercero).strip()

        if id_tercero and id_tercero.lower() != "null":
            cedulas.add(id_tercero)

print("Cantidad de cédulas únicas:", len(cedulas))


# -----------------------------------------
# 3. Preparar los parámetros de Helisa
# -----------------------------------------

fecha = parametros["Fecha_inicio"]

# Si dateMillisec espera DD-MM-YYYY, convertimos la fecha.
# fecha_helisa = datetime.strptime(fecha, "%Y-%m-%d").strftime("%d-%m-%Y")

year = datetime.strptime(fecha, "%Y-%m-%d").year
date = dateMillisec(fecha)

no_existe = []
errores_consulta = []


# -----------------------------------------
# 4. Consultar cada cédula en Helisa
# -----------------------------------------

for di in sorted(cedulas):

    payload = f"{year}|{di}|{date}"

    respuesta_helisa = GET_TERCERO(
        url_helisa,
        payload,
        year,
        di,
        date
    )

    if respuesta_helisa is None:
        errores_consulta.append({
            "cedula": di,
            "motivo": "No se recibió respuesta de Helisa"
        })
        continue

    codigo = respuesta_helisa.status_code

    if codigo == 204:
        # La documentación indica que no hay resultados.
        no_existe.append(di)
        continue

    if codigo != 200:
        errores_consulta.append({
            "cedula": di,
            "codigo_http": codigo,
            "respuesta": respuesta_helisa.text
        })
        continue

    try:
        resultado = respuesta_helisa.json()
    except ValueError:
        errores_consulta.append({
            "cedula": di,
            "motivo": "Helisa no devolvió un JSON válido",
            "respuesta": respuesta_helisa.text
        })
        continue

    # Una lista vacía indica que no se encontraron registros.
    if isinstance(resultado, list) and len(resultado) == 0:
        no_existe.append(di)
    else:
        print(f"Cédula {di}: respuesta recibida; revisar resultado.")


# -----------------------------------------
# 5. Mostrar el resumen
# -----------------------------------------

print("\n========== RESUMEN ==========")
print("Cédulas consultadas:", len(cedulas))
print("Cédulas no encontradas:", len(no_existe))
print("Consultas con errores:", len(errores_consulta))

print("\nCédulas que no aparecen en Helisa:")

for di in no_existe:
    print(di)

if errores_consulta:
    print("\nConsultas que necesitan revisión:")
    print(json.dumps(
        errores_consulta,
        indent=4,
        ensure_ascii=False
    ))
