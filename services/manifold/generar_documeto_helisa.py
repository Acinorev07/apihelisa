# from services.helisa.obtener_dcto_helisa import obtener_dcto_helisa
# from services.q10.obtener_recibo_pago_factura import obtener_recibo_pago_factura
# from services.q10.obtener_tercero import obtener_tercero
# from services.q10.obtener_estudiante import obtener_estudiante
# from hooks.validarDi import validar_documento_tercero
# from datetime import datetime
# from hooks.obtener_archivo_json import cargar_archivo
# from hooks.validarDi import validar_documento_tercero



# from datetime import datetime


# def obtener_movimientos_debito(
#     factura,
#     concepto,
#     doc_id,
#     centro_costo,
#     codigos_bancos
# ):
#     movimientos = []

#     fecha_factura = datetime.fromisoformat(
#         factura["Fecha_factura"]
#     ).date()

#     pagos = factura.get("Pagos") or []

#     for pago in pagos:

#         # Ignorar pagos anulados o con otro estado.
#         if pago.get("Estado_pago") != "Pagado":
#             continue

#         fecha_pago = pago.get("Fecha_pago")

#         if not fecha_pago:
#             continue

#         fecha_pago = datetime.fromisoformat(
#             fecha_pago
#         ).date()

#         # Solo pagos del mismo día de la factura.
#         if fecha_pago != fecha_factura:
#             continue

#         codigo_recibo = pago.get("Numero_recibo_pago")

#         if not codigo_recibo:
#             continue

#         recibo = obtener_recibo_pago_factura(
#             codigo_recibo
#         )

#         if not isinstance(recibo, dict):
#             continue

#         if recibo.get("Estado_pago") != "Pagado":
#             continue

#         fecha_recibo = recibo.get("Fecha_pago")

#         if not fecha_recibo:
#             continue

#         fecha_recibo = datetime.fromisoformat(
#             fecha_recibo
#         ).date()

#         if fecha_recibo != fecha_factura:
#             continue

#         # Verificar que el recibo corresponda a esta factura.
#         detalles = recibo.get("Detalles") or []

#         detalle_factura = next(
#             (
#                 detalle
#                 for detalle in detalles
#                 if str(detalle.get("Numero_factura"))
#                 == str(factura.get("Numero_factura"))
#             ),
#             None
#         )

#         if detalle_factura is None:
#             continue

#         for forma_pago in recibo.get("Formas_pago", []):

#             nombre_forma = (
#                 forma_pago.get("Nombre_forma_pago") or ""
#             ).strip().casefold()

#             valor = forma_pago.get("Valor", 0)

#             if nombre_forma == "efectivo":
#                 cuenta_debito = "110505"

#             elif nombre_forma in ("consignación", "consignacion"):
#                 # Aquí conservamos tu lógica de identificación
#                 # del banco mediante las observaciones.
#                 observaciones = factura.get("Observaciones") or ""
#                 observaciones = observaciones.upper()

#                 if "BCS" in observaciones:
#                     cuenta_debito = "11201002"
#                 else:
#                     cuenta_debito = "11201001"

#             else:
#                 continue

#             movimiento = {
#                 "nature": {
#                     "tag": "D"
#                 },
#                 "costCenter": centro_costo,
#                 "concept": concepto,
#                 "accountingClass": {
#                     "value": 2
#                 },
#                 "value": valor,
#                 "idThirdParty": doc_id,
#                 "account": cuenta_debito,
#                 "userCode": 1,
#                 "taxBase": 0
#             }

#             movimientos.append(movimiento)

#     return movimientos


# def generar_partida_doble(facturas):


#     errores_consulta = []


#     codigos_centro_costos = [
#             "E1",
#             "E2",
#             "E3",
#             "F1",
#             "F2",
#             "F3",
#             "SO1",
#             "SO2",
#             "SO3",
#             "PI1",
#             "PI2",
#             "PI3",
#             "AS1",
#             "AS2",
#             "AS3",
#             "DONACION",
#             "CF1",
#             "CF2",
#             "C1",
#             "C2",
#         ]


#     codigo_bancos = [
#          "BANCO",
#          "BCS"
#     ]


#     for factura in facturas:

            
#         numero_factura = factura.get("Numero_factura")

#         observaciones = factura.get("Observaciones")
        
#         lista_observaciones = observaciones.split("/")

#         limpia = [s.strip() for s in lista_observaciones]

#         for cod_centro_costo in codigos_centro_costos:
            
#             centro_costo_filtrado = [s for s in limpia if s == cod_centro_costo]

#             # Combertir lista a texto
#             cc = "".join(centro_costo_filtrado)
            

#         # Buscar la cuenta contable
#         cuenta_credito= producto_cuenta.get(codigo_producto)

#         if not cc:
#             cen_cost = "062001"

#         else:
#             cen_cost = centro_costo.get(cc)

#         nombre_estudiante = factura.get("Nombre_completo_estudiante")
#         nombre_tercero = factura.get("Nombre_completo_tercero")

#         # Si el campo de Nombre_completo_estudiante tiene información se ejecuta este bloque
#         if nombre_estudiante:
#                 print(f"Nombre estudiante: {nombre_estudiante}")

#                 estudiante_q10 = obtener_estudiante(
#                         codigo_estudiante=factura.get("Codigo_estudiante"),
#                         codigo_programa = ""
#                         )

#                 if not isinstance(estudiante_q10, dict):
#                     return {
#                         "status": 502,
#                         "mensaje": "No se pudo obtener la información del estudiante desde Q10."
#                     }

#                 if not estudiante_q10.get("Numero_identificacion"):
#                     return {
#                         "status": 422,
#                         "mensaje": "El estudiante no tiene número de identificación."
#                     }

#                 docuemento_identidad = estudiante_q10.get("Numero_identificacion_estudiante")

#                 doc_id = validar_documento_tercero(
#                      docuemento_identidad
#                 )



#                 primer_nombre = estudiante_q10.get("Primer_nombre")
#                 primer_apellido = estudiante_q10.get("Primer_apellido")
#                 partes = [
#                         primer_nombre,
#                         primer_apellido,
#                     ]

#                 nombre = " ".join(
#                         str(parte).strip()
#                         for parte in partes
#                         if parte is not None and str(parte).strip()
#                     )
                
#                 # Si el campo de Nombre_completo_tercero tiene información se ejecuta este bloque
#         elif nombre_tercero:
        
#                 print(f"Nombre tercero: {factura.get("Nombre_completo_tercero")}")
                    
#                 consecutivo_tercero = factura.get("Consecutivo_tercero")
        
#                 tercero_q10 = obtener_tercero(
#                         consecutivo_tercero
#                 )

#                 nombre = tercero_q10.get("Nombre_completo")
#                 docuemento_identidad = estudiante_q10.get("Numero_identificacion_tercero")

#                 doc_id = validar_documento_tercero(
#                      docuemento_identidad
#                 )
        
#                 if not isinstance(tercero_q10, dict):
#                     return {
#                         "status": 502,
#                         "mensaje": "No se pudo obtener la información del Tercero desde Q10."
#                     }
        
#                 if not tercero_q10.get("Numero_identificacion"):
#                     return {
#                         "status": 422,
#                         "mensaje": "El tercero no tiene número de identificación."
#                     }


#         partes_concepto = [
#                 nombre,
#                 numero_factura,
#                 centro_costo_filtrado
#         ]

#         concepto = "-".join(partes_concepto)


#         # Obtener los pagos de la factura
#         pagos = factura.get("Pagos", [])

#         # Validar que exista la lista de pagos
#         if pagos is None:
#             errores_consulta.append({
#                 "factura": numero_factura,
#                 "motivo": "La factura no contiene la clave Pagos."
#             })
#             continue

#         for pago in pagos:

#             if not isinstance(pago, dict):
#                 errores_consulta.append({
#                     "factura": numero_factura,
#                     "motivo": "Uno de los pagos tiene una estructura inválida."
#                 })
#                 continue

#             codigo_recibo = pago.get("Numero_recibo_pago")


#             if codigo_recibo is not None and str(codigo_recibo).strip():

#                 recibo_pago = obtener_recibo_pago_factura(codigo_recibo)

#                 for forma_pago in recibo_pago.get("Formas_pago",[]):

#                     nombre_forma_pago = forma_pago.get("Nombre_forma_pago")

#                     if nombre_forma_pago == "Consignacion":

#                         for codigo_banco in codigo_bancos:

#                             banco_filtrado = [s for s in limpia if s == codigo_banco]
                             
#                                # Combertir lista a texto
#                             banco = "".join(banco_filtrado)


#                         if banco == "BCS":

#                              cuenta_debito = "11201002"

#                         else:
#                              cuenta_debito = "11201001"

#                     elif nombre_forma_pago == "Efectivo":

#                          cuenta_debito = "110505"


#                     valor_pagado = forma_pago.get("Valor")

                            


                        
                              
                         

                         
                     
                        



#         contabilidad = cargar_archivo(
#                 "clasificacion_contable_productos.json"
#             )


#         producto_cuenta = contabilidad["producto-cuenta"]
#         centro_costo = contabilidad["centro_costos"]

#         for producto in factura.get("Productos", []):

#             codigo_producto = producto.get(
#                 "Codigo_producto", ""
#             )

#             valor_unidad = producto.get("Valor_unidad")

#             valor_descuento = producto.get("Valor_descuento")




#             if valor_descuento:

                 
#                 movimiento_debito = {
#                                 "nature": {
#                                     "tag": "D"
#                                 },

#                                 "costCenter": "",

#                                 "concept": concepto,

#                                 "accountingClass": {
#                                     "value": 2
#                                 },

#                                 "value": valor_pagado,

#                                 "idThirdParty": doc_id,

#                                 "account": cuenta_debito,

#                                 "userCode": 1,

#                                 "taxBase": 0
#                             },
#                 movimiento_debito_descuento =  {
#                                 "nature": {
#                                     "tag": "D"
#                                 },

#                                 "costCenter": cen_cost,

#                                 "concept": concepto,

#                                 "accountingClass": {
#                                     "value": 2
#                                 },

#                                 "value": valor_unidad,

#                                 "idThirdParty": doc_id,

#                                 "account": "41750103",

#                                 "userCode": 1,

#                                 "taxBase": 0
#                             }

#                 movimiento_credito =  {
#                                 "nature": {
#                                     "tag": "C"
#                                 },

#                                 "costCenter": cen_cost,

#                                 "concept": concepto,

#                                 "accountingClass": {
#                                     "value": 2
#                                 },

#                                 "value": valor_unidad,

#                                 "idThirdParty": doc_id,

#                                 "account": cuenta_credito,

#                                 "userCode": 1,

#                                 "taxBase": 0
#                             }

#                 return {
#                      "movimiento_credito":movimiento_credito,
#                      "movimiento_debito_descuento":movimiento_debito_descuento,
#                      "movimiento_debito":movimiento_debito,    
#                 }

#             else:

#                 movimiento_debito = {
#                                 "nature": {
#                                     "tag": "D"
#                                 },

#                                 "costCenter": "",

#                                 "concept": concepto,

#                                 "accountingClass": {
#                                     "value": 2
#                                 },

#                                 "value": valor_pagado,

#                                 "idThirdParty": doc_id,

#                                 "account": cuenta_debito,

#                                 "userCode": 1,

#                                 "taxBase": 0
#                             },
#                 movimiento_credito =  {
#                                 "nature": {
#                                     "tag": "C"
#                                 },

#                                 "costCenter": cen_cost,

#                                 "concept": concepto,

#                                 "accountingClass": {
#                                     "value": 2
#                                 },

#                                 "value": valor_unidad,

#                                 "idThirdParty": doc_id,

#                                 "account": cuenta_credito,

#                                 "userCode": 1,

#                                 "taxBase": 0
#                             }

#                 return {
#                      "movimiento_credito":movimiento_credito,
#                      "movimiento_debito":movimiento_debito,    
#                 }

                 
                 




# def generar_documento_helisa(facturas):

#     if not facturas:

#         print("No hay facturas para contabilizar")

#     fecha_original = facturas[0].get("Fecha_factura")

#     if not fecha_original:
#         raise ValueError("La factura no tiene fecha.")

#     fecha_documento = datetime.fromisoformat(
#         fecha_original
#     ).date()


#     transactions = []


#     fecha_inicial = "2026-11-01"
#     fecha_final = "2026-11-30"
#     tipo_documento = "NIED"
#     accounting_type = 0

#     historial_documento_helisa = obtener_dcto_helisa(
#         fecha_inicial=fecha_inicial,
#         fecha_final=fecha_final,
#         document_type=tipo_documento,
#         accounting_type=accounting_type
#     )

#     if not historial_documento_helisa:
#         print("No se encontraron documentos.")
#         return

#     # Extraemos la lista de documentos del diccionario.
#     documentos = historial_documento_helisa.get("documents", [])

#     if not documentos:
#         print("No se encontraron documentos.")
#         return

#     numero_documento = []

#     for registro in documentos:

#         numero = registro.get("document", {}).get("number")

#         if numero is not None:
#             numero_documento.append(numero)

#     if not numero_documento:
#         print("No se encontraron números de documentos.")
#         return

#     # Convertimos a entero para comparar los consecutivos numéricamente.
#     ultimo_documento = max(
#         numero_documento,
#         key=lambda numero: int(numero)
#     )

#     print("Último documento:", ultimo_documento)


#     siguiente_documento = str(int(ultimo_documento) + 1).zfill(8)

#     print("Último documento:", ultimo_documento)
#     print("Siguiente documento:", siguiente_documento)


#     contabilizacion = generar_partida_doble(facturas)

#     transactions.append(contabilizacion)
    


#     documento = {

#         "document": {

#             "date": {
#                  "day": fecha_documento.dia,
#                 "month": fecha_documento.mes,
#                 "year": fecha_documento.año
#             },
                       
#             "document": {
#                 "type": documento,
#                 "number": siguiente_documento
#             },

#             "transactions": transactions
#         }
#     }

#     return documento
        


# from datetime import datetime
# from calendar import monthrange
# import unicodedata

# from services.helisa.obtener_dcto_helisa import obtener_dcto_helisa
# from services.q10.obtener_recibo_pago_factura import (
#     obtener_recibo_pago_factura
# )
# from services.q10.obtener_tercero import obtener_tercero
# from services.q10.obtener_estudiante import obtener_estudiante

# from hooks.validarDi import validar_documento_tercero
# from hooks.obtener_archivo_json import cargar_archivo


# ---------------------------------------------------------
# FUNCIONES AUXILIARES
# ---------------------------------------------------------

# def convertir_fecha(fecha):
#     """Convierte una fecha ISO de Q10 en datetime.date."""
#     if not fecha:
#         raise ValueError("Se recibió una fecha vacía.")

#     return datetime.fromisoformat(
#         str(fecha).replace("Z", "+00:00")
#     ).date()


# def normalizar_texto(texto):
#     """Normaliza textos para comparar formas de pago."""
#     texto = str(texto or "").strip().casefold()

#     return "".join(
#         caracter
#         for caracter in unicodedata.normalize("NFD", texto)
#         if unicodedata.category(caracter) != "Mn"
#     )


# def obtener_centro_costo(factura, equivalencias):
#     """Busca el centro de costo en las observaciones."""

#     codigos_centro_costos = [
#         "E1", "E2", "E3",
#         "F1", "F2", "F3",
#         "SO1", "SO2", "SO3",
#         "PI1", "PI2", "PI3",
#         "AS1", "AS2", "AS3",
#         "DONACION",
#         "CF1", "CF2",
#         "C1", "C2"
#     ]

#     observaciones = factura.get("Observaciones") or ""

#     partes = [
#         parte.strip().upper()
#         for parte in observaciones.split("/")
#     ]

#     codigo_encontrado = next(
#         (
#             codigo
#             for codigo in codigos_centro_costos
#             if codigo in partes
#         ),
#         None
#     )

#     if codigo_encontrado is None:
#         return "062001", ""

#     centro = equivalencias.get(codigo_encontrado)

#     if not centro:
#         raise ValueError(
#             f"No existe equivalencia de centro de costos "
#             f"para {codigo_encontrado}."
#         )

#     return centro, codigo_encontrado


# def obtener_datos_tercero(factura):
#     """Obtiene nombre e identificación del estudiante o tercero."""

#     nombre_estudiante = factura.get(
#         "Nombre_completo_estudiante"
#     )

#     nombre_tercero = factura.get(
#         "Nombre_completo_tercero"
#     )

#     if nombre_estudiante:
#         estudiante = obtener_estudiante(
#             codigo_estudiante=factura.get("Codigo_estudiante"),
#             codigo_programa=""
#         )

#         if not isinstance(estudiante, dict):
#             raise ValueError(
#                 "No se pudo consultar el estudiante en Q10."
#             )

#         identificacion = (
#             estudiante.get("Numero_identificacion")
#             or estudiante.get("Numero_identificacion_estudiante")
#             or factura.get("Numero_identificacion_estudiante")
#         )

#         nombre = (
#             estudiante.get("Nombre_completo")
#             or nombre_estudiante
#         )

#     elif nombre_tercero:
#         tercero = obtener_tercero(
#             factura.get("Consecutivo_tercero")
#         )

#         if not isinstance(tercero, dict):
#             raise ValueError(
#                 "No se pudo consultar el tercero en Q10."
#             )

#         identificacion = (
#             tercero.get("Numero_identificacion")
#             or factura.get("Numero_identificacion_tercero")
#         )

#         nombre = (
#             tercero.get("Nombre_completo")
#             or nombre_tercero
#         )

#     else:
#         raise ValueError(
#             "La factura no tiene estudiante ni tercero identificado."
#         )

#     if not identificacion:
#         raise ValueError(
#             "El tercero no tiene número de identificación."
#         )

#     doc_id = validar_documento_tercero(identificacion)

#     if not doc_id:
#         raise ValueError(
#             "No fue posible validar la identificación del tercero."
#         )

#     return nombre, doc_id


# # ---------------------------------------------------------
# # OBTENER DÉBITOS DE LOS RECIBOS DE CAJA
# # ---------------------------------------------------------

# def obtener_movimientos_debito(
#     factura,
#     concepto,
#     doc_id
# ):
#     movimientos = []

#     fecha_factura = convertir_fecha(
#         factura.get("Fecha_factura")
#     )

#     observaciones = (
#         factura.get("Observaciones") or ""
#     ).upper()

#     # Conservamos tu identificación actual del banco.
#     cuenta_consignacion = (
#         "11201002"
#         if "BCS" in observaciones
#         else "11201001"
#     )

#     pagos = factura.get("Pagos") or []

#     for pago in pagos:

#         if not isinstance(pago, dict):
#             continue

#         # Ignorar pagos anulados y cualquier estado distinto de Pagado.
#         if pago.get("Estado_pago") != "Pagado":
#             continue

#         fecha_pago = pago.get("Fecha_pago")

#         if not fecha_pago:
#             continue

#         if convertir_fecha(fecha_pago) != fecha_factura:
#             continue

#         codigo_recibo = pago.get("Numero_recibo_pago")

#         if not codigo_recibo:
#             continue

#         recibo = obtener_recibo_pago_factura(
#             codigo_recibo
#         )

#         if not isinstance(recibo, dict):
#             raise ValueError(
#                 f"No se pudo consultar el recibo {codigo_recibo}."
#             )

#         if recibo.get("Estado_pago") != "Pagado":
#             continue

#         fecha_recibo = recibo.get("Fecha_pago")

#         if not fecha_recibo:
#             continue

#         if convertir_fecha(fecha_recibo) != fecha_factura:
#             continue

#         # Confirmar que el recibo corresponde a esta factura.
#         detalles = recibo.get("Detalles") or []

#         detalle_factura = next(
#             (
#                 detalle
#                 for detalle in detalles
#                 if str(detalle.get("Numero_factura"))
#                 == str(factura.get("Numero_factura"))
#             ),
#             None
#         )

#         if detalle_factura is None:
#             continue

#         formas_pago = recibo.get("Formas_pago") or []

#         for forma_pago in formas_pago:

#             nombre_forma = normalizar_texto(
#                 forma_pago.get("Nombre_forma_pago")
#             )

#             valor = float(
#                 forma_pago.get("Valor") or 0
#             )

#             if valor <= 0:
#                 continue

#             if nombre_forma == "efectivo":
#                 cuenta_debito = "110505"

#             elif nombre_forma == "consignacion":
#                 cuenta_debito = cuenta_consignacion

#             else:
#                 raise ValueError(
#                     f"Forma de pago no configurada: "
#                     f"{forma_pago.get('Nombre_forma_pago')}"
#                 )

#             movimientos.append({
#                 "nature": {
#                     "tag": "D"
#                 },
#                 "costCenter": "",
#                 "concept": concepto,
#                 "accountingClass": {
#                     "value": 2
#                 },
#                 "value": round(valor, 2),
#                 "idThirdParty": doc_id,
#                 "account": cuenta_debito,
#                 "userCode": 1,
#                 "taxBase": 0
#             })

#     return movimientos


# # ---------------------------------------------------------
# # GENERAR PARTIDA DOBLE
# # ---------------------------------------------------------

# def generar_partida_doble(facturas):

#     contabilidad = cargar_archivo(
#         "clasificacion_contable_productos.json"
#     )

#     producto_cuenta = contabilidad["producto-cuenta"]

#     equivalencias_centro = contabilidad["centro_costos"]

#     transactions = []
#     errores = []

#     for factura in facturas:

#         numero_factura = factura.get("Numero_factura")

#         try:

#             # 1. Obtener tercero.
#             nombre, doc_id = obtener_datos_tercero(
#                 factura
#             )

#             # 2. Obtener centro de costo.
#             centro_costo, codigo_cc = obtener_centro_costo(
#                 factura,
#                 equivalencias_centro
#             )

#             # 3. Construir concepto.
#             concepto = (
#                 f"{nombre}-{numero_factura}-{codigo_cc}"
#             )

#             # 4. Obtener débitos de los pagos válidos.
#             movimientos_debito = obtener_movimientos_debito(
#                 factura=factura,
#                 concepto=concepto,
#                 doc_id=doc_id
#             )

#             if not movimientos_debito:
#                 errores.append({
#                     "factura": numero_factura,
#                     "motivo": (
#                         "No tiene recibos pagados y válidos "
#                         "en la fecha de la factura."
#                     )
#                 })
#                 continue

#             total_pagado = round(
#                 sum(
#                     movimiento["value"]
#                     for movimiento in movimientos_debito
#                 ),
#                 2
#             )

#             productos = factura.get("Productos") or []

#             if not productos:
#                 errores.append({
#                     "factura": numero_factura,
#                     "motivo": "La factura no contiene productos."
#                 })
#                 continue

#             # 5. Preparar valores de productos.
#             datos_productos = []

#             for producto in productos:

#                 codigo_producto = producto.get(
#                     "Codigo_producto"
#                 )

#                 cuenta_credito = producto_cuenta.get(
#                     codigo_producto
#                 )

#                 if not cuenta_credito:
#                     raise ValueError(
#                         f"No existe cuenta contable para "
#                         f"el producto {codigo_producto}."
#                     )

#                 cantidad = float(
#                     producto.get("Cantidad") or 1
#                 )

#                 valor_unidad = float(
#                     producto.get("Valor_unidad") or 0
#                 )

#                 valor_bruto = round(
#                     valor_unidad * cantidad,
#                     2
#                 )

#                 descuento = float(
#                     producto.get("Valor_descuento") or 0
#                 )

#                 valor_neto = producto.get("Valor_a_pagar")

#                 if valor_neto is None:
#                     valor_neto = valor_bruto - descuento
#                 else:
#                     valor_neto = float(valor_neto)

#                 if valor_neto < 0 or descuento < 0:
#                     raise ValueError(
#                         f"Valores inválidos en producto "
#                         f"{codigo_producto}."
#                     )

#                 datos_productos.append({
#                     "cuenta": cuenta_credito,
#                     "bruto": valor_bruto,
#                     "descuento": descuento,
#                     "neto": valor_neto
#                 })

#             total_neto_factura = round(
#                 sum(
#                     producto["neto"]
#                     for producto in datos_productos
#                 ),
#                 2
#             )

#             if total_neto_factura <= 0:
#                 raise ValueError(
#                     "El valor neto de los productos es cero."
#                 )

#             if total_pagado > total_neto_factura + 0.01:
#                 raise ValueError(
#                     f"Los pagos del día ({total_pagado}) "
#                     f"superan el valor neto de la factura "
#                     f"({total_neto_factura})."
#                 )

#             # 6. Agregar los débitos de los recibos.
#             transactions.extend(
#                 movimientos_debito
#             )

#             # 7. Distribuir los valores pagados entre productos.
#             proporcion = (
#                 total_pagado / total_neto_factura
#             )

#             for producto in datos_productos:

#                 valor_neto_contabilizado = round(
#                     producto["neto"] * proporcion,
#                     2
#                 )

#                 descuento_contabilizado = round(
#                     producto["descuento"] * proporcion,
#                     2
#                 )

#                 valor_credito = round(
#                     valor_neto_contabilizado
#                     + descuento_contabilizado,
#                     2
#                 )

#                 # Débito del descuento, si existe.
#                 if descuento_contabilizado > 0:

#                     transactions.append({
#                         "nature": {
#                             "tag": "D"
#                         },
#                         "costCenter": centro_costo,
#                         "concept": concepto,
#                         "accountingClass": {
#                             "value": 2
#                         },
#                         "value": descuento_contabilizado,
#                         "idThirdParty": doc_id,
#                         "account": "41750103",
#                         "userCode": 1,
#                         "taxBase": 0
#                     })

#                 # Crédito de la cuenta del producto.
#                 if valor_credito > 0:

#                     transactions.append({
#                         "nature": {
#                             "tag": "C"
#                         },
#                         "costCenter": centro_costo,
#                         "concept": concepto,
#                         "accountingClass": {
#                             "value": 2
#                         },
#                         "value": valor_credito,
#                         "idThirdParty": doc_id,
#                         "account": producto["cuenta"],
#                         "userCode": 1,
#                         "taxBase": 0
#                     })

#         except Exception as error:

#             errores.append({
#                 "factura": numero_factura,
#                 "motivo": str(error)
#             })

#     # 8. Validar que los movimientos estén cuadrados.
#     total_debitos = round(
#         sum(
#             movimiento["value"]
#             for movimiento in transactions
#             if movimiento["nature"]["tag"] == "D"
#         ),
#         2
#     )

#     total_creditos = round(
#         sum(
#             movimiento["value"]
#             for movimiento in transactions
#             if movimiento["nature"]["tag"] == "C"
#         ),
#         2
#     )

#     return {
#         "transactions": transactions,
#         "errores": errores,
#         "total_debitos": total_debitos,
#         "total_creditos": total_creditos,
#         "cuadra": abs(total_debitos - total_creditos) <= 0.01
#     }


# # ---------------------------------------------------------
# # GENERAR DOCUMENTO HELISA
# # ---------------------------------------------------------

# def generar_documento_helisa(facturas):

#     if not facturas:
#         raise ValueError(
#             "No hay facturas para contabilizar."
#         )

#     # 1. Validar que todas las facturas tengan la misma fecha.
#     fechas = {
#         convertir_fecha(factura.get("Fecha_factura"))
#         for factura in facturas
#     }

#     if len(fechas) != 1:
#         raise ValueError(
#             "Las facturas no tienen una única fecha."
#         )

#     fecha_documento = fechas.pop()

#     # 2. Consultar consecutivos del mes de contabilización.
#     fecha_inicial = fecha_documento.replace(day=1)

#     ultimo_dia = monthrange(
#         fecha_documento.year,
#         fecha_documento.month
#     )[1]

#     fecha_final = fecha_documento.replace(
#         day=ultimo_dia
#     )

#     tipo_documento = "NIED"
#     accounting_type = 0

#     historial = obtener_dcto_helisa(
#         fecha_inicial=fecha_inicial.isoformat(),
#         fecha_final=fecha_final.isoformat(),
#         document_type=tipo_documento,
#         accounting_type=accounting_type
#     )

#     if not isinstance(historial, dict):
#         raise ValueError(
#             "No fue posible consultar los documentos de Helisa."
#         )

#     documentos = historial.get("documents") or []

#     if not documentos:
#         raise ValueError(
#             "No se encontraron documentos para consultar "
#             "el siguiente consecutivo."
#         )

#     numeros = []

#     for registro in documentos:

#         numero = (
#             registro.get("document", {}).get("number")
#         )

#         if numero is not None:
#             numeros.append(str(numero))

#     if not numeros:
#         raise ValueError(
#             "Helisa no devolvió números de documentos."
#         )

#     ultimo_documento = max(
#         numeros,
#         key=lambda numero: int(numero)
#     )

#     siguiente_documento = str(
#         int(ultimo_documento) + 1
#     ).zfill(8)

#     # 3. Generar todos los movimientos.
#     resultado = generar_partida_doble(
#         facturas
#     )

#     if resultado["errores"]:
#         raise ValueError(
#             "Hay facturas que no pudieron contabilizarse: "
#             f"{resultado['errores']}"
#         )

#     if not resultado["transactions"]:
#         raise ValueError(
#             "No se generaron movimientos contables."
#         )

#     # 4. Validar partida doble.
#     if not resultado["cuadra"]:
#         raise ValueError(
#             "El documento no está cuadrado. "
#             f"Débitos: {resultado['total_debitos']}; "
#             f"Créditos: {resultado['total_creditos']}."
#         )

#     # 5. Construir documento.
#     documento = {
#         "document": {
#             "date": {
#                 "day": fecha_documento.day,
#                 "month": fecha_documento.month,
#                 "year": fecha_documento.year
#             },
#             "document": {
#                 "type": tipo_documento,
#                 "number": siguiente_documento
#             },
#             "transactions": resultado["transactions"]
#         }
#     }

#     print("\nDocumento construido correctamente.")
#     print("Consecutivo:", siguiente_documento)
#     print("Fecha:", fecha_documento)
#     print("Facturas procesadas:", len(facturas))
#     print("Movimientos:", len(resultado["transactions"]))
#     print("Total débitos:", resultado["total_debitos"])
#     print("Total créditos:", resultado["total_creditos"])

#     return documento

# import calendar
# import unicodedata
# from datetime import datetime, date

# # ============================================================
# # FUNCIONES AUXILIARES
# # ============================================================

# def convertir_fecha(fecha):
#     """
#     Convierte una fecha ISO de Q10 en un objeto date.
#     """
#     if isinstance(fecha, date):
#         return fecha

#     if not fecha:
#         raise ValueError("No se recibió una fecha válida.")

#     return datetime.fromisoformat(
#         str(fecha).replace("Z", "+00:00")
#     ).date()


# def normalizar_texto(texto):
#     """
#     Elimina tildes y normaliza texto para facilitar búsquedas.
#     """
#     texto = str(texto or "").strip().upper()

#     return "".join(
#         caracter
#         for caracter in unicodedata.normalize("NFD", texto)
#         if unicodedata.category(caracter) != "Mn"
#     )


# def cargar_equivalencias():
#     """
#     Carga las equivalencias contables desde el JSON.
#     """
#     contabilidad = cargar_archivo(
#         "clasificacion_contable_productos.json"
#      )
    
#     return contabilidad


# def obtener_centro_costo(factura, equivalencias):
#     """
#     Busca el centro de costo en las observaciones.
#     Si no encuentra coincidencia, utiliza 062001.
#     """
#     observaciones = normalizar_texto(
#         factura.get("Observaciones", "")
#     )

#     centros = equivalencias.get("centro_costos", {})

#     for codigo, centro in centros.items():
#         codigo_normalizado = normalizar_texto(codigo)

#         if codigo_normalizado and codigo_normalizado in observaciones:
#             return str(centro)

#     return "062001"


# def obtener_datos_tercero(factura):
#     """
#     Obtiene los datos del estudiante o tercero de Q10.
#     """

#     consecutivo_tercero = factura.get("Consecutivo_tercero")

#     if consecutivo_tercero:
#         tercero = obtener_tercero(consecutivo_tercero)

#         if not tercero:
#             raise ValueError(
#                 f"No se encontró el tercero de la factura "
#                 f"{factura.get('Numero_factura')}."
#             )

#         nombre = (
#             tercero.get("Nombre_completo")
#             or tercero.get("Nombre_completo_tercero")
#             or factura.get("Nombre_completo_tercero")
#         )

#         identificacion = (
#             tercero.get("Numero_identificacion")
#             or tercero.get("Numero_identificacion_tercero")
#             or factura.get("Numero_identificacion_tercero")
#         )

#     else:
#         codigo_estudiante = factura.get("Codigo_estudiante")

#         estudiante = obtener_estudiante(codigo_estudiante)

#         if not estudiante:
#             raise ValueError(
#                 f"No se encontró el estudiante de la factura "
#                 f"{factura.get('Numero_factura')}."
#             )

#         nombre = (
#             estudiante.get("Nombre_completo")
#             or estudiante.get("Nombre_completo_estudiante")
#             or factura.get("Nombre_completo_estudiante")
#         )

#         identificacion = (
#             estudiante.get("Numero_identificacion")
#             or estudiante.get("Numero_identificacion_estudiante")
#             or factura.get("Numero_identificacion_estudiante")
#         )

#     if not identificacion:
#         raise ValueError(
#             f"La factura {factura.get('Numero_factura')} "
#             "no tiene identificación del tercero."
#         )

#     if not nombre:
#         nombre = "TERCERO SIN NOMBRE"

#     return nombre, str(identificacion)


# # ============================================================
# # DÉBITOS: PAGOS EFECTIVAMENTE REALIZADOS
# # ============================================================

# def obtener_movimientos_debito(factura, concepto, doc_id):
#     """
#     Obtiene los débitos de los recibos pagados el mismo día
#     de la factura.

#     Ignora recibos anulados y pagos de otras fechas.
#     """

#     movimientos = []

#     fecha_factura = convertir_fecha(
#         factura.get("Fecha_factura")
#     )

#     numero_factura = str(
#         factura.get("Numero_factura")
#     )

#     for pago in factura.get("Pagos", []):

#         if normalizar_texto(
#             pago.get("Estado_pago")
#         ) != "PAGADO":
#             continue

#         fecha_pago = convertir_fecha(
#             pago.get("Fecha_pago")
#         )

#         if fecha_pago != fecha_factura:
#             continue

#         numero_recibo = pago.get("Numero_recibo_pago")

#         if not numero_recibo:
#             raise ValueError(
#                 f"La factura {numero_factura} tiene "
#                 "un pago sin número de recibo."
#             )

#         recibo = obtener_recibo_pago_factura(numero_recibo)

#         if not recibo:
#             raise ValueError(
#                 f"No se pudo consultar el recibo {numero_recibo}."
#             )

#         if normalizar_texto(
#             recibo.get("Estado_pago")
#         ) != "PAGADO":
#             continue

#         fecha_recibo = convertir_fecha(
#             recibo.get("Fecha_pago")
#         )

#         if fecha_recibo != fecha_factura:
#             continue

#         # Confirmar que el recibo corresponde a esta factura.
#         detalles = recibo.get("Detalles", [])

#         corresponde = any(
#             str(detalle.get("Numero_factura")) == numero_factura
#             for detalle in detalles
#         )

#         if not corresponde:
#             continue

#         observaciones = normalizar_texto(
#             recibo.get("Observaciones")
#             or factura.get("Observaciones")
#         )

#         formas_pago = recibo.get("Formas_pago", [])

#         for forma in formas_pago:

#             nombre_forma = normalizar_texto(
#                 forma.get("Nombre_forma_pago", "")
#             )

#             nombre_cuenta = normalizar_texto(
#                 forma.get("Nombre_cuenta", "")
#             )

#             valor = float(
#                 forma.get("Valor", forma.get("Valor_pago", 0)) or 0
#             )

#             if valor <= 0:
#                 continue

#             if "EFECTIVO" in nombre_forma or "CAJA" in nombre_cuenta:
#                 cuenta = "110505"

#             elif (
#                 "BCS" in observaciones
#                 or "CAJA SOCIAL" in observaciones
#             ):
#                 cuenta = "11201002"

#             elif (
#                 "CONSIGNACION" in nombre_forma
#                 or "CONSIGNACION" in observaciones
#                 or "BAN" in observaciones
#             ):
#                 cuenta = "11201001"

#             else:
#                 raise ValueError(
#                     f"No se pudo identificar la cuenta contable "
#                     f"de la forma de pago '{nombre_forma}' "
#                     f"del recibo {numero_recibo}."
#                 )

#             movimientos.append({
#                 "nature": {"tag": "D"},
#                 "costCenter": "",
#                 "concept": concepto,
#                 "accountingClass": {"value": 2},
#                 "value": round(valor, 2),
#                 "idThirdParty": doc_id,
#                 "account": cuenta,
#                 "userCode": 1,
#                 "taxBase": 0
#             })

#     if not movimientos:
#         raise ValueError(
#             f"La factura {numero_factura} no tiene "
#             "pagos válidos el mismo día de su emisión."
#         )

#     return movimientos


# # ============================================================
# # GENERACIÓN DE MOVIMIENTOS CONTABLES
# # ============================================================

# def generar_partida_doble(facturas):

#     equivalencias = cargar_equivalencias()

#     producto_cuenta = equivalencias.get(
#         "producto-cuenta", {}
#     )

#     producto_cuenta_2 = equivalencias.get(
#         "producto-cuenta-2", {}
#     )

#     transactions = []
#     errores = []

#     total_debitos = 0.0
#     total_creditos = 0.0

#     for factura in facturas:

#         try:

#             numero_factura = str(
#                 factura.get("Numero_factura")
#             )

#             nombre, doc_id = obtener_datos_tercero(factura)

#             centro_costo = obtener_centro_costo(
#                 factura,
#                 equivalencias
#             )

#             observaciones = factura.get("Observaciones") or ""

#             concepto = (
#                 f"{nombre}-{numero_factura}-"
#                 f"{observaciones.split('/')[0].strip()}"
#             )

#             # ------------------------------------------------
#             # 1. GENERAR LOS DÉBITOS DEL RECIBO
#             # ------------------------------------------------

#             movimientos_debito = obtener_movimientos_debito(
#                 factura,
#                 concepto,
#                 doc_id
#             )

#             for movimiento in movimientos_debito:
#                 transactions.append(movimiento)

#                 total_debitos += movimiento["value"]

#             # ------------------------------------------------
#             # 2. PROCESAR LOS PRODUCTOS
#             # ------------------------------------------------

#             productos = factura.get("Productos", [])

#             if not productos:
#                 raise ValueError(
#                     f"La factura {numero_factura} no tiene productos."
#                 )

#             for producto in productos:

#                 codigo_producto = producto.get("Codigo_producto")

#                 valor_unidad = float(
#                     producto.get("Valor_unidad") or 0
#                 )

#                 cantidad = float(
#                     producto.get("Cantidad") or 0
#                 )

#                 valor_descuento = float(
#                     producto.get("Valor_descuento") or 0
#                 )

#                 valor_impuesto = float(
#                     producto.get("Valor_impuesto") or 0
#                 )

#                 valor_a_pagar = float(
#                     producto.get("Valor_a_pagar") or 0
#                 )

#                 cuenta_principal = producto_cuenta.get(
#                     codigo_producto
#                 )

#                 cuenta_secundaria = producto_cuenta_2.get(
#                     codigo_producto
#                 )

#                 if not cuenta_principal:
#                     raise ValueError(
#                         f"El producto {codigo_producto} "
#                         "no tiene cuenta contable principal."
#                     )

#                 # ============================================
#                 # CASO ESPECIAL: CGCR
#                 # ============================================

#                 if codigo_producto == "CGCR":

#                     if not cuenta_secundaria:
#                         raise ValueError(
#                             "El producto CGCR no tiene "
#                             "cuenta contable secundaria."
#                         )

#                     valor_servicio = valor_unidad * cantidad

#                     valor_iva = valor_impuesto

#                     total_producto = (
#                         valor_servicio + valor_iva
#                     )

#                     if round(total_producto, 2) != round(
#                         valor_a_pagar, 2
#                     ):
#                         raise ValueError(
#                             f"Factura {numero_factura}: "
#                             f"CGCR no cuadra. "
#                             f"Servicio + IVA = {total_producto}; "
#                             f"Valor a pagar = {valor_a_pagar}."
#                         )

#                     # Crédito del servicio: 28150701
#                     movimiento_servicio = {
#                         "nature": {"tag": "C"},
#                         "costCenter": centro_costo,
#                         "concept": concepto,
#                         "accountingClass": {"value": 2},
#                         "value": round(valor_servicio, 2),
#                         "idThirdParty": doc_id,
#                         "account": cuenta_principal,
#                         "userCode": 1,
#                         "taxBase": 0
#                     }

#                     transactions.append(movimiento_servicio)

#                     total_creditos += valor_servicio

#                     # Crédito del IVA: 28150702
#                     if valor_iva > 0:

#                         movimiento_iva = {
#                             "nature": {"tag": "C"},
#                             "costCenter": centro_costo,
#                             "concept": concepto,
#                             "accountingClass": {"value": 2},
#                             "value": round(valor_iva, 2),
#                             "idThirdParty": doc_id,
#                             "account": cuenta_secundaria,
#                             "userCode": 1,
#                             "taxBase": 0
#                         }

#                         transactions.append(movimiento_iva)

#                         total_creditos += valor_iva

#                     continue

#                 # ============================================
#                 # RESTO DE PRODUCTOS
#                 # ============================================

#                 valor_bruto = valor_unidad * cantidad

#                 valor_neto = valor_a_pagar

#                 # Conservar la lógica de descuentos.
#                 if valor_descuento > 0:

#                     movimiento_descuento = {
#                         "nature": {"tag": "D"},
#                         "costCenter": centro_costo,
#                         "concept": concepto,
#                         "accountingClass": {"value": 2},
#                         "value": round(valor_descuento, 2),
#                         "idThirdParty": doc_id,
#                         "account": "41750103",
#                         "userCode": 1,
#                         "taxBase": 0
#                     }

#                     transactions.append(movimiento_descuento)

#                     total_debitos += valor_descuento

#                     valor_credito = valor_neto + valor_descuento

#                 else:
#                     valor_credito = valor_neto

#                 if valor_credito > 0:

#                     movimiento_credito = {
#                         "nature": {"tag": "C"},
#                         "costCenter": centro_costo,
#                         "concept": concepto,
#                         "accountingClass": {"value": 2},
#                         "value": round(valor_credito, 2),
#                         "idThirdParty": doc_id,
#                         "account": cuenta_principal,
#                         "userCode": 1,
#                         "taxBase": 0
#                     }

#                     transactions.append(movimiento_credito)

#                     total_creditos += valor_credito

#         except Exception as error:

#             errores.append(
#                 f"Factura {factura.get('Numero_factura')}: {error}"
#             )

#     total_debitos = round(total_debitos, 2)
#     total_creditos = round(total_creditos, 2)

#     return {
#         "transactions": transactions,
#         "errores": errores,
#         "total_debitos": total_debitos,
#         "total_creditos": total_creditos,
#         "cuadra": total_debitos == total_creditos
#     }


# # ============================================================
# # GENERACIÓN DEL DOCUMENTO HELISA
# # ============================================================
# def generar_documento_helisa(facturas):

#     if not facturas:
#         raise ValueError(
#             "No hay facturas para contabilizar."
#         )

#     # 1. Validar que todas las facturas tengan la misma fecha.
#     fechas = {
#         convertir_fecha(factura.get("Fecha_factura"))
#         for factura in facturas
#     }

#     if len(fechas) != 1:
#         raise ValueError(
#             "Las facturas no tienen una única fecha."
#         )

#     fecha_documento = fechas.pop()

#     # 2. Consultar consecutivos del mes de contabilización.
#     fecha_inicial = fecha_documento.replace(day=1)

#     ultimo_dia = monthrange(
#         fecha_documento.year,
#         fecha_documento.month
#     )[1]

#     fecha_final = fecha_documento.replace(
#         day=ultimo_dia
#     )

#     tipo_documento = "NIED"
#     accounting_type = 0

#     historial = obtener_dcto_helisa(
#         fecha_inicial=fecha_inicial.isoformat(),
#         fecha_final=fecha_final.isoformat(),
#         document_type=tipo_documento,
#         accounting_type=accounting_type
#     )

#     if not isinstance(historial, dict):
#         raise ValueError(
#             "No fue posible consultar los documentos de Helisa."
#         )

#     documentos = historial.get("documents") or []

#     print(documentos[1])

#     if not documentos:
#         raise ValueError(
#             "No se encontraron documentos para consultar "
#             "el siguiente consecutivo."
#         )

#     numeros = []

#     for registro in documentos:

#         numero = (
#             registro.get("document", {}).get("number")
#         )

#         if numero is not None:
#             numeros.append(str(numero))

#     if not numeros:
#         raise ValueError(
#             "Helisa no devolvió números de documentos."
#         )

#     ultimo_documento = max(
#         numeros,
#         key=lambda numero: int(numero)
#     )

#     siguiente_documento = str(
#         int(ultimo_documento) + 1
#     ).zfill(8)

#     # 3. Generar todos los movimientos.
#     resultado = generar_partida_doble(
#         facturas
#     )

#     if resultado["errores"]:
#         raise ValueError(
#             "Hay facturas que no pudieron contabilizarse: "
#             f"{resultado['errores']}"
#         )

#     if not resultado["transactions"]:
#         raise ValueError(
#             "No se generaron movimientos contables."
#         )

#     # 4. Validar partida doble.
#     if not resultado["cuadra"]:
#         raise ValueError(
#             "El documento no está cuadrado. "
#             f"Débitos: {resultado['total_debitos']}; "
#             f"Créditos: {resultado['total_creditos']}."
#         )

#     # 5. Construir documento.
#     documento = {
#         "document": {
#             "date": {
#                 "day": fecha_documento.day,
#                 "month": fecha_documento.month,
#                 "year": fecha_documento.year
#             },
#             "document": {
#                 "type": tipo_documento,
#                 "number": siguiente_documento
#             },
#             "transactions": resultado["transactions"]
#         }
#     }

#     print("\nDocumento construido correctamente.")
#     print("Consecutivo:", siguiente_documento)
#     print("Fecha:", fecha_documento)
#     print("Facturas procesadas:", len(facturas))
#     print("Movimientos:", len(resultado["transactions"]))
#     print("Total débitos:", resultado["total_debitos"])
#     print("Total créditos:", resultado["total_creditos"])

#     return documento





from datetime import datetime
from calendar import monthrange
import unicodedata

from services.helisa.obtener_dcto_helisa import obtener_dcto_helisa
from services.q10.obtener_recibo_pago_factura import (
    obtener_recibo_pago_factura
)
from services.q10.obtener_tercero import obtener_tercero
from services.q10.obtener_estudiante import obtener_estudiante

from hooks.validarDi import validar_documento_tercero
from hooks.obtener_archivo_json import cargar_archivo


# ---------------------------------------------------------
# FUNCIONES AUXILIARES
# ---------------------------------------------------------

def convertir_fecha(fecha):
    """Convierte una fecha ISO de Q10 en datetime.date."""
    if not fecha:
        raise ValueError("Se recibió una fecha vacía.")

    return datetime.fromisoformat(
        str(fecha).replace("Z", "+00:00")
    ).date()


def normalizar_texto(texto):
    """Normaliza textos para comparar formas de pago."""
    texto = str(texto or "").strip().casefold()

    return "".join(
        caracter
        for caracter in unicodedata.normalize("NFD", texto)
        if unicodedata.category(caracter) != "Mn"
    )


def obtener_centro_costo(factura, equivalencias):
    """Busca el centro de costo en las observaciones."""

    codigos_centro_costos = [
        "E1", "E2", "E3",
        "F1", "F2", "F3",
        "SO1", "SO2", "SO3",
        "PI1", "PI2", "PI3",
        "AS1", "AS2", "AS3",
        "DONACION",
        "CF1", "CF2",
        "C1", "C2"
    ]

    observaciones = factura.get("Observaciones") or ""

    partes = [
        parte.strip().upper()
        for parte in observaciones.split("/")
    ]

    codigo_encontrado = next(
        (
            codigo
            for codigo in codigos_centro_costos
            if codigo in partes
        ),
        None
    )

    if codigo_encontrado is None:
        return "062001", ""

    centro = equivalencias.get(codigo_encontrado)

    if not centro:
        raise ValueError(
            f"No existe equivalencia de centro de costos "
            f"para {codigo_encontrado}."
        )

    return centro, codigo_encontrado


def obtener_datos_tercero(factura):
    """Obtiene nombre e identificación del estudiante o tercero."""

    nombre_estudiante = factura.get(
        "Nombre_completo_estudiante"
    )

    nombre_tercero = factura.get(
        "Nombre_completo_tercero"
    )

    if nombre_estudiante:
        estudiante = obtener_estudiante(
            codigo_estudiante=factura.get("Codigo_estudiante"),
            codigo_programa=""
        )

        if not isinstance(estudiante, dict):
            raise ValueError(
                "No se pudo consultar el estudiante en Q10."
            )

        identificacion = (
            estudiante.get("Numero_identificacion")
            or estudiante.get("Numero_identificacion_estudiante")
            or factura.get("Numero_identificacion_estudiante")
        )

        nombre = (
            estudiante.get("Nombre_completo")
            or nombre_estudiante
        )

    elif nombre_tercero:
        tercero = obtener_tercero(
            factura.get("Consecutivo_tercero")
        )

        if not isinstance(tercero, dict):
            raise ValueError(
                "No se pudo consultar el tercero en Q10."
            )

        identificacion = (
            tercero.get("Numero_identificacion")
            or factura.get("Numero_identificacion_tercero")
        )

        nombre = (
            tercero.get("Nombre_completo")
            or nombre_tercero
        )

    else:
        raise ValueError(
            "La factura no tiene estudiante ni tercero identificado."
        )

    if not identificacion:
        raise ValueError(
            "El tercero no tiene número de identificación."
        )

    doc_id = validar_documento_tercero(identificacion)

    if not doc_id:
        raise ValueError(
            "No fue posible validar la identificación del tercero."
        )

    return nombre, doc_id


# ---------------------------------------------------------
# OBTENER DÉBITOS DE LOS RECIBOS DE CAJA
# ---------------------------------------------------------

def obtener_movimientos_debito(
    factura,
    concepto,
    doc_id
):
    movimientos = []

    fecha_factura = convertir_fecha(
        factura.get("Fecha_factura")
    )

    observaciones = (
        factura.get("Observaciones") or ""
    ).upper()

    # Conservamos tu identificación actual del banco.
    cuenta_consignacion = (
        "11201002"
        if "BCS" in observaciones
        else "11201001"
    )

    pagos = factura.get("Pagos") or []

    for pago in pagos:

        if not isinstance(pago, dict):
            continue

        # Ignorar pagos anulados y cualquier estado distinto de Pagado.
        if pago.get("Estado_pago") != "Pagado":
            continue

        fecha_pago = pago.get("Fecha_pago")

        if not fecha_pago:
            continue

        if convertir_fecha(fecha_pago) != fecha_factura:
            continue

        codigo_recibo = pago.get("Numero_recibo_pago")

        if not codigo_recibo:
            continue

        recibo = obtener_recibo_pago_factura(
            codigo_recibo
        )

        if not isinstance(recibo, dict):
            raise ValueError(
                f"No se pudo consultar el recibo {codigo_recibo}."
            )

        if recibo.get("Estado_pago") != "Pagado":
            continue

        fecha_recibo = recibo.get("Fecha_pago")

        if not fecha_recibo:
            continue

        if convertir_fecha(fecha_recibo) != fecha_factura:
            continue

        # Confirmar que el recibo corresponde a esta factura.
        detalles = recibo.get("Detalles") or []

        detalle_factura = next(
            (
                detalle
                for detalle in detalles
                if str(detalle.get("Numero_factura"))
                == str(factura.get("Numero_factura"))
            ),
            None
        )

        if detalle_factura is None:
            continue

        formas_pago = recibo.get("Formas_pago") or []

        for forma_pago in formas_pago:

            nombre_forma = normalizar_texto(
                forma_pago.get("Nombre_forma_pago")
            )

            valor = float(
                forma_pago.get("Valor") or 0
            )

            if valor <= 0:
                continue

            if nombre_forma == "efectivo":
                cuenta_debito = "110505"

            elif nombre_forma == "consignacion":
                cuenta_debito = cuenta_consignacion

            else:
                raise ValueError(
                    f"Forma de pago no configurada: "
                    f"{forma_pago.get('Nombre_forma_pago')}"
                )

            movimientos.append({
                "nature": {
                    "tag": "D"
                },
                "costCenter": "",
                "concept": concepto,
                "accountingClass": {
                    "value": "0"
                },
                "value": round(valor, 2),
                "idThirdParty": doc_id,
                "account": cuenta_debito,
                "userCode": 1,
                "taxBase": 0
            })

    return movimientos


# ---------------------------------------------------------
# GENERAR PARTIDA DOBLE
# ---------------------------------------------------------

def generar_partida_doble(facturas):

    contabilidad = cargar_archivo(
        "clasificacion_contable_productos.json"
    )

    producto_cuenta = contabilidad["producto-cuenta"]

    equivalencias_centro = contabilidad["centro_costos"]

    transactions = []
    errores = []

    for factura in facturas:

        numero_factura = factura.get("Numero_factura")

        try:

            # 1. Obtener tercero.
            nombre, doc_id = obtener_datos_tercero(
                factura
            )

            # 2. Obtener centro de costo.
            centro_costo, codigo_cc = obtener_centro_costo(
                factura,
                equivalencias_centro
            )

            # 3. Construir concepto.
            concepto = (
                f"{nombre}-{numero_factura}-{codigo_cc}"
            )

            # 4. Obtener débitos de los pagos válidos.
            movimientos_debito = obtener_movimientos_debito(
                factura=factura,
                concepto=concepto,
                doc_id=doc_id
            )

            if not movimientos_debito:
                errores.append({
                    "factura": numero_factura,
                    "motivo": (
                        "No tiene recibos pagados y válidos "
                        "en la fecha de la factura."
                    )
                })
                continue

            total_pagado = round(
                sum(
                    movimiento["value"]
                    for movimiento in movimientos_debito
                ),
                2
            )

            productos = factura.get("Productos") or []

            if not productos:
                errores.append({
                    "factura": numero_factura,
                    "motivo": "La factura no contiene productos."
                })
                continue

            # 5. Preparar valores de productos.
            datos_productos = []

            for producto in productos:

                codigo_producto = producto.get(
                    "Codigo_producto"
                )

                cuenta_credito = producto_cuenta.get(
                    codigo_producto
                )

                if not cuenta_credito:
                    raise ValueError(
                        f"No existe cuenta contable para "
                        f"el producto {codigo_producto}."
                    )

                cantidad = float(
                    producto.get("Cantidad") or 1
                )

                valor_unidad = float(
                    producto.get("Valor_unidad") or 0
                )

                valor_bruto = round(
                    valor_unidad * cantidad,
                    2
                )

                descuento = float(
                    producto.get("Valor_descuento") or 0
                )

                valor_neto = producto.get("Valor_a_pagar")

                if valor_neto is None:
                    valor_neto = valor_bruto - descuento
                else:
                    valor_neto = float(valor_neto)

                if valor_neto < 0 or descuento < 0:
                    raise ValueError(
                        f"Valores inválidos en producto "
                        f"{codigo_producto}."
                    )

                # ÚNICA INCORPORACIÓN:
                # Para CGCR se obtiene también el valor del impuesto.
                valor_impuesto = float(
                    producto.get("Valor_impuesto") or 0
                )

                datos_productos.append({
                    "codigo": codigo_producto,
                    "cuenta": cuenta_credito,
                    "bruto": valor_bruto,
                    "descuento": descuento,
                    "neto": valor_neto,
                    "impuesto": valor_impuesto
                })

            total_neto_factura = round(
                sum(
                    producto["neto"]
                    for producto in datos_productos
                ),
                2
            )

            if total_neto_factura <= 0:
                raise ValueError(
                    "El valor neto de los productos es cero."
                )

            if total_pagado > total_neto_factura + 0.01:
                raise ValueError(
                    f"Los pagos del día ({total_pagado}) "
                    f"superan el valor neto de la factura "
                    f"({total_neto_factura})."
                )

            # 6. Agregar los débitos de los recibos.
            transactions.extend(
                movimientos_debito
            )

            # 7. Distribuir los valores pagados entre productos.
            proporcion = (
                total_pagado / total_neto_factura
            )

            for producto in datos_productos:

                codigo_producto = producto["codigo"]

                # -------------------------------------------------
                # CONTABILIZACIÓN ESPECIAL PARA CGCR
                # -------------------------------------------------
                if codigo_producto == "CGCR":

                    # Valor del servicio: Valor_unidad * Cantidad.
                    valor_servicio = round(
                        producto["bruto"],
                        2
                    )

                    # Valor del impuesto informado por Q10.
                    valor_impuesto = round(
                        producto["impuesto"],
                        2
                    )

                    # Distribuir proporcionalmente si el pago es parcial.
                    valor_servicio_contabilizado = round(
                        valor_servicio * proporcion,
                        2
                    )

                    valor_impuesto_contabilizado = round(
                        valor_impuesto * proporcion,
                        2
                    )

                    # Crédito de la comisión de garantía de crédito.
                    if valor_servicio_contabilizado > 0:

                        transactions.append({
                            "nature": {
                                "tag": "C"
                            },
                            "costCenter": centro_costo,
                            "concept": concepto,
                            "accountingClass": {
                                "value": "0"
                            },
                            "value": valor_servicio_contabilizado,
                            "idThirdParty": doc_id,
                            "account": "28150701",
                            "userCode": 1,
                            "taxBase": 0
                        })

                    # Crédito del impuesto de la comisión.
                    if valor_impuesto_contabilizado > 0:

                        transactions.append({
                            "nature": {
                                "tag": "C"
                            },
                            "costCenter": centro_costo,
                            "concept": concepto,
                            "accountingClass": {
                                "value": "0"
                            },
                            "value": valor_impuesto_contabilizado,
                            "idThirdParty": doc_id,
                            "account": "28150702",
                            "userCode": 1,
                            "taxBase": 0
                        })

                    # CGCR ya fue contabilizado en sus dos cuentas.
                    continue

                # -------------------------------------------------
                # CONTABILIZACIÓN ORIGINAL PARA LOS DEMÁS PRODUCTOS
                # -------------------------------------------------

                valor_neto_contabilizado = round(
                    producto["neto"] * proporcion,
                    2
                )

                descuento_contabilizado = round(
                    producto["descuento"] * proporcion,
                    2
                )

                valor_credito = round(
                    valor_neto_contabilizado
                    + descuento_contabilizado,
                    2
                )

                # Débito del descuento, si existe.
                if descuento_contabilizado > 0:

                    transactions.append({
                        "nature": {
                            "tag": "D"
                        },
                        "costCenter": centro_costo,
                        "concept": concepto,
                        "accountingClass": {
                            "value": "0"
                        },
                        "value": descuento_contabilizado,
                        "idThirdParty": doc_id,
                        "account": "41750103",
                        "userCode": 1,
                        "taxBase": 0
                    })

                # Crédito de la cuenta original del producto.
                if valor_credito > 0:

                    transactions.append({
                        "nature": {
                            "tag": "C"
                        },
                        "costCenter": centro_costo,
                        "concept": concepto,
                        "accountingClass": {
                            "value": "0"
                        },
                        "value": valor_credito,
                        "idThirdParty": doc_id,
                        "account": producto["cuenta"],
                        "userCode": 1,
                        "taxBase": 0
                    })

        except Exception as error:

            errores.append({
                "factura": numero_factura,
                "motivo": str(error)
            })

    # 8. Validar que los movimientos estén cuadrados.
    total_debitos = round(
        sum(
            movimiento["value"]
            for movimiento in transactions
            if movimiento["nature"]["tag"] == "D"
        ),
        2
    )

    total_creditos = round(
        sum(
            movimiento["value"]
            for movimiento in transactions
            if movimiento["nature"]["tag"] == "C"
        ),
        2
    )

    return {
        "transactions": transactions,
        "errores": errores,
        "total_debitos": total_debitos,
        "total_creditos": total_creditos,
        "cuadra": abs(total_debitos - total_creditos) <= 0.01
    }


# ---------------------------------------------------------
# GENERAR DOCUMENTO HELISA
# ---------------------------------------------------------

def generar_documento_helisa(facturas):

    if not facturas:
        raise ValueError(
            "No hay facturas para contabilizar."
        )

    # 1. Validar que todas las facturas tengan la misma fecha.
    fechas = {
        convertir_fecha(factura.get("Fecha_factura"))
        for factura in facturas
    }

    if len(fechas) != 1:
        raise ValueError(
            "Las facturas no tienen una única fecha."
        )

    fecha_documento = fechas.pop()

    # 2. Consultar consecutivos del mes de contabilización.
    fecha_inicial = fecha_documento.replace(day=1)

    ultimo_dia = monthrange(
        fecha_documento.year,
        fecha_documento.month
    )[1]

    fecha_final = fecha_documento.replace(
        day=ultimo_dia
    )

    tipo_documento = "NIED"
    accounting_type = 0

    historial = obtener_dcto_helisa(
        fecha_inicial=fecha_inicial.isoformat(),
        fecha_final=fecha_final.isoformat(),
        document_type=tipo_documento,
        accounting_type=accounting_type
    )

    if not isinstance(historial, dict):
        raise ValueError(
            "No fue posible consultar los documentos de Helisa."
        )

    documentos = historial.get("documents") or []

    if not documentos:
        raise ValueError(
            "No se encontraron documentos para consultar "
            "el siguiente consecutivo."
        )

    numeros = []

    for registro in documentos:

        numero = (
            registro.get("document", {}).get("number")
        )

        if numero is not None:
            numeros.append(str(numero))

    if not numeros:
        raise ValueError(
            "Helisa no devolvió números de documentos."
        )

    ultimo_documento = max(
        numeros,
        key=lambda numero: int(numero)
    )

    siguiente_documento = str(
        int(ultimo_documento) + 1
    ).zfill(8)

    # 3. Generar todos los movimientos.
    resultado = generar_partida_doble(
        facturas
    )

    if resultado["errores"]:
        raise ValueError(
            "Hay facturas que no pudieron contabilizarse: "
            f"{resultado['errores']}"
        )

    if not resultado["transactions"]:
        raise ValueError(
            "No se generaron movimientos contables."
        )

    # 4. Validar partida doble.
    if not resultado["cuadra"]:
        raise ValueError(
            "El documento no está cuadrado. "
            f"Débitos: {resultado['total_debitos']}; "
            f"Créditos: {resultado['total_creditos']}."
        )

    # 5. Construir documento.
    documento = {
        "document": {
            "date": {
                "day": fecha_documento.day,
                "month": fecha_documento.month,
                "year": fecha_documento.year
            },
            "document": {
                "type": tipo_documento,
                "number": siguiente_documento
            },
            "transactions": resultado["transactions"]
        }
    }

    print("\nDocumento construido correctamente.")
    print("Consecutivo:", siguiente_documento)
    print("Fecha:", fecha_documento)
    print("Facturas procesadas:", len(facturas))
    print("Movimientos:", len(resultado["transactions"]))
    print("Total débitos:", resultado["total_debitos"])
    print("Total créditos:", resultado["total_creditos"])

    return documento
