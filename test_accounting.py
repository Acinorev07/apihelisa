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

from apiFacturasQ10 import consultar_facturas
# Llamamos las facturas 

facturas = consultar_facturas()

print(facturas)