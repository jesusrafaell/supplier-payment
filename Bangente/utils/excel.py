import os
from typing import List
from datetime import datetime
import openpyxl
from Bangente.utils.utilitis import Util

from classes.Historico import Historico


class Excel:
    def make_report_excel(date: datetime, resultList: List[Historico], rutaArchivo):
        fecha = date.strftime("%Y%m%d")
        fileName = rutaArchivo + "\\" + fecha + '_1' + ".xlsx"

        i = 1
        while True:
            fileName = rutaArchivo + "\\" + fecha + \
                '_' + str(i).zfill(2) + ".xlsx"
            fichero = os.path.join(rutaArchivo, fileName)

            if os.path.exists(fichero):
                # El archivo existe, intentar con el siguiente número
                i += 1
            else:
                # El archivo no existe, utilizar este nombre
                break

        header = ["Numero Pago a Proveedor", "RIF", "Beneficiario",
                  "Banco Beneficiario", "Cuenta Beneficiario", "Concepto", "Monto", "Terminal"]
        title = "ArchivoPagoAComercios"

        try:
            write_excel(resultList, header, fileName)
        except Exception as e:
            print(e)


def write_excel(data: List[Historico], header, filename):
    try:
        wb = openpyxl.Workbook()
        sheet = wb.active

        sheet.append(header)

        for registro in data:
            row = [
                Util.leftPad(str(registro.hisId), 8, '0'),
                str(registro.comerRif),
                registro.comerDesc.strip(),
                registro.aboCodBanco,
                registro.aboNroCuenta,
                "Abono por concepto MilPagos comercio: " +
                registro.comerRif.strip() + " " +
                registro.hisLote.strip() + " " +
                registro.aboTerminal.strip() + " " +
                str(registro.hisFecha),
                registro.hisAmountTotal,
                registro.aboTerminal
            ]
            sheet.append(row)

        wb.save(filename)

    except Exception as e:
        print(e)
