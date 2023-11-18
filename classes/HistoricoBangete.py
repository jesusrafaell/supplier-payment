import pyodbc
from typing import List, Tuple

from classes.Historico import Historico
from utils.utilitis import getHistoricoTranred


def getHistoricoPago_Bangete(fecha: str, cnxn: pyodbc.Connection, cuentaDebito: str, rif: str) -> List[Historico]:
    SPsql = f"EXEC SP_consultaHistoricoPago_p '{fecha}', 3, ''"
    cursor = cnxn.cursor().execute(SPsql)
    historicos = get_historicosBangete(cursor, cuentaDebito, rif)
    cursor.close()
    return historicos


def get_historicosBangete(cursor: pyodbc.Connection, cuentaDebito: str, rif: str) -> List[Historico]:
    column_names = [column[0] for column in cursor.description]
    results = []
    while True:
        result = cursor.fetchone()
        if result is None:
            break
        result_dict = {}
        for i in range(len(column_names)):
            result_dict[column_names[i]] = result[i]
        results.append(result_dict)

    historicos = []
    for row in results:
        historico = getHistoricoTranred(cuentaDebito, rif)
        historico.aboCodAfi = row['aboCodAfi']
        historico.hisAmountTotal = float(row['TotalAmount'])
        historico.hisFecha = row['UltimaFechaEjecucion']
        historico.hisFechaEjecucion = row['UltimaFechaEjecucion']
        historico.hisFechaProceso = row['UltimaFechaProceso']
        historicos.append(historico)

    print('Total Afiliados bangente ->', len(results))
    return historicos
