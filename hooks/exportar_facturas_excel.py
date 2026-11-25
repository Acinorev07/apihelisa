

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from pathlib import Path
from datetime import datetime


def convertir_fecha(fecha):
    if not fecha:
        return None

    try:
        return datetime.fromisoformat(
            fecha.replace("Z", "+00:00")
        )
    except (ValueError, AttributeError):
        return fecha


def exportar_facturas_por_cajero(
    facturas,
    nombre_archivo="reportes/facturas_por_cajero.xlsx"
):
    try:
        if not facturas:
            print("No hay facturas para exportar.")
            return None

        agrupadas = {}

        for factura in facturas:
            cajero = factura.get("Nombre_cajero") or "SIN CAJERO"

            agrupadas.setdefault(cajero, []).append(factura)

        libro = Workbook()
        resumen = libro.active
        resumen.title = "RESUMEN"

        encabezados = [
            "Cajero",
            "Cantidad de facturas",
            "Total facturado"
        ]

        resumen.append(encabezados)

        columnas = [
            "Fecha",
            "Factura",
            "Observaciones",
            "Periodo",
            "Total factura"
        ]

        color = PatternFill(
            fill_type="solid",
            fgColor="398C78"
        )

        fuente = Font(bold=True, color="FFFFFF")

        for celda in resumen[1]:
            celda.fill = color
            celda.font = fuente

        nombres_hojas = set()

        for cajero, registros in agrupadas.items():

            nombre_hoja = cajero[:31]
            base = nombre_hoja
            contador = 1

            while nombre_hoja in nombres_hojas:
                sufijo = f"_{contador}"
                nombre_hoja = base[:31-len(sufijo)] + sufijo
                contador += 1

            nombres_hojas.add(nombre_hoja)

            hoja = libro.create_sheet(nombre_hoja)
            hoja.append(columnas)

            for celda in hoja[1]:
                celda.fill = color
                celda.font = fuente
                celda.alignment = Alignment(horizontal="center")

            total_cajero = 0

            for factura in registros:

                valor = factura.get("Valor_total") or 0
                total_cajero += valor

                hoja.append([
                    convertir_fecha(factura.get("Fecha_factura")),
                    factura.get("Numero_factura"),
                    factura.get("Observaciones"),
                    factura.get("Nombre_periodo"),
                    valor
                ])

            for fila in range(2, hoja.max_row + 1):
                hoja.cell(fila, 1).number_format = "dd/mm/yyyy hh:mm:ss"
                hoja.cell(fila, 5).number_format = '"$"#,##0.00'

            anchos = [22, 15, 75, 18, 20]

            for indice, ancho in enumerate(anchos, start=1):
                hoja.column_dimensions[
                    get_column_letter(indice)
                ].width = ancho

            hoja.auto_filter.ref = hoja.dimensions
            hoja.freeze_panes = "A2"

            # Agregar información al resumen
            resumen.append([
                cajero,
                len(registros),
                total_cajero
            ])

        resumen.column_dimensions["A"].width = 40
        resumen.column_dimensions["B"].width = 25
        resumen.column_dimensions["C"].width = 22

        for fila in range(2, resumen.max_row + 1):
            resumen.cell(fila, 3).number_format = '"$"#,##0.00'

        resumen.auto_filter.ref = resumen.dimensions
        resumen.freeze_panes = "A2"

        ruta = Path(nombre_archivo)
        ruta.parent.mkdir(parents=True, exist_ok=True)

        libro.save(ruta)

        print("\n========== EXCEL GENERADO ==========")
        print(f"Archivo: {ruta.resolve()}")
        print(f"Cajeros: {len(agrupadas)}")
        print(f"Facturas: {len(facturas)}")

        return str(ruta.resolve())

    except Exception as e:
        print(f"Error generando Excel: {e}")
        return None

