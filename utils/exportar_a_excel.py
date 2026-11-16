
from hooks.obtener_archivo_json import cargar_archivo
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from pathlib import Path
from datetime import datetime
from hooks.obtener_estudiante_tercero import obtener_estudiante_tercero

def convertir_fecha(fecha):
    if not fecha:
        return None

    try:

        return datetime.fromisoformat(
            fecha.replace("Z", "+00:00")
        )

    except (ValueError, AttributeError):
        return fecha

    
    


def exportar_a_excel(
        facturas,
        nombre_archivo="reporte/todas_las_facturas_(4).xlsx"
        ):

    try:
        if not facturas:
            print("No hay facturas para exportar")
            return {
                "mensaje":"No hay facturas para exportar",
                "status":400
            }

        libro = Workbook()
        # resumen = libro.active
        # resumen.title = "Resumen"

        columnas = [
            "Fecha",
            "Nombre",
            "Codigo Producto",
            "Nombre Producto",
            "Numero Factura",
            "Valor Unidad",
            "Valor Total",
            "Valor Descuento",
            "Valor a pagar",
            "Notas credito",
            "Pagos",
            "Periodo"
        ]

        color = PatternFill(
            fill_type = "solid",
            fgColor="398C78"
        )
        fuente = Font(bold=True, color = "FFFFFF")

        nombre_hoja = "Pendientes (4)"

        
        hoja = libro.active
        hoja.title = nombre_hoja 
        hoja.append(columnas)

        for celda in hoja[1]:
            celda.fill = color
            celda.font = fuente
            celda.alignment = Alignment(horizontal="center")

        for factura in facturas:

            nombre = obtener_estudiante_tercero(
                                     "Nombre_completo_estudiante",
                                     "Nombre_completo_tercero",
                                     factura
                                )

            valor = factura.get("Valor_total") or 0
            for producto in factura["Productos"]:
                
                hoja.append([
                    convertir_fecha(factura.get("Fecha_factura")),
                    nombre,
                    producto.get("Codigo_producto"),
                    producto.get("Nombre_producto"),
                    factura.get("Numero_factura"),
                    producto.get("Valor_unidad"),
                    valor,
                    producto.get("Valor_descuento"),
                    producto.get("Valor_a_pagar"),
                    len(factura["Notas_credito"]),
                    len(factura["Pagos"]),
                    producto.get("Nombre_periodo")

                ])

        for fila in range(2, hoja.max_row + 1):
            hoja.cell(fila, 1).number_format = "dd/mm/yyyy hh:mm:ss"
            hoja.cell(fila, 6).number_format = '"$"#,##0.00'
            hoja.cell(fila, 7).number_format = '"$"#,##0.00'
            hoja.cell(fila, 8).number_format = '"$"#,##0.00'

        anchos = [22, 75, 50, 75, 15, 30, 30, 30, 30, 10, 10, 20 ]

        for indice, ancho in enumerate(anchos, start=1):
            hoja.column_dimensions[
                get_column_letter(indice)
            ].width = ancho


        hoja.auto_filter.ref = hoja.dimensions
        hoja.freeze_panes = "A2"


        ruta = Path(nombre_archivo)
        ruta.parent.mkdir(parents=True, exist_ok=True)

        libro.save(ruta)    


        print("\n=========== EXCEL GENERADO =============")   
        print(f"Archivo: {ruta.resolve()}")
        print(f"Facturas: {len(facturas)}")
        

    except Exception as e:

       print(f"Error generando excel: {e}")
       return {
           "mensaje":"Error generando excel",
           "status":400
       }

    print(len(facturas))






if __name__ == "__main__":

    facturas = cargar_archivo(
            "todas_las_facturas_q10_(4).json"
        )
    exportar_a_excel(facturas=facturas)