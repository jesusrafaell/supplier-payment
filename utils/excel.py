import os
import pandas as pd
from typing import List
from datetime import datetime
from classes.Historico import Historico
from utils.utilitis import leftPad


def make_report_excel(date: str, resultList: List[Historico], rutaArchivo: str, correlativo: str, op: int):
    fileName = os.path.join(rutaArchivo, 'Excel',
                            str(date) + correlativo + ".xlsx")
    print('Create Excel', fileName, 'afi:',
          resultList[0].aboCodAfi, 'totalR:', len(resultList))
    try:
        if op == 1:
            header = ["Numero Pago a Proveedor", "RIF", "Beneficiario",
                      "Banco Beneficiario", "Cuenta Beneficiario", "Concepto", "Monto", "Afiliado"]
        else:
            header = ["Numero Pago a Proveedor", "RIF", "Beneficiario",
                      "Banco Beneficiario", "Cuenta Beneficiario", "Concepto", "Monto", "Terminal"]

        data = get_data(resultList, op)
        write_excel(data, header, fileName)
        print('Excel creado', fileName)
    except Exception as e:
        print('make_report_excel', e)


def get_data(resultList: List[Historico], op: int):
    data = []
    for registro in resultList:
        hisFecha = registro.hisFecha.date().isoformat()
        row = [
            leftPad(str(registro.hisId), 8, '0'),
            str(registro.comerRif),
            registro.comerDesc.strip(),
            registro.aboCodBanco,
            registro.aboNroCuenta,
            f"Abono por concepto MilPagos comercio: {registro.aboCodAfi} {registro.comerRif.strip()} {registro.hisLote.strip()} {registro.aboTerminal.strip()} {hisFecha}",
            registro.hisAmountTotal,
            registro.aboCodAfi if op == 1 else registro.aboTerminal
        ]
        data.append(row)
    return data


def write_excel(data: List[List], header: List[str], filename: str):
    try:
        df = pd.DataFrame(data, columns=header)
        with pd.ExcelWriter(filename, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)

    except Exception as e:
        print('write_excel', e)
