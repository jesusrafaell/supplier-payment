import pyodbc
from classes.LoteBanco import LotesBanco
from classes.LoteDetalle import LoteDetalle


def execute_stored_procedure(cnxn: pyodbc.Connection, stored_procedure):
    result = cnxn.cursor().execute(stored_procedure)
    row = result.fetchone()
    return row[0]


def GetMontoBPLAZA(cnxn: pyodbc.Connection) -> str:
    return execute_stored_procedure(cnxn, "EXEC GetMontoBPLAZA")


def GetMontoBVC(cnxn: pyodbc.Connection) -> str:
    return execute_stored_procedure(cnxn, "EXEC GetMontoBVC")


def GetCuentaDebito(cnxn: pyodbc.Connection, afi: str) -> str:
    SPsql = f'EXEC SP_GetCuentaDebito {afi}'
    result = cnxn.cursor().execute(SPsql)
    row = result.fetchone()
    return row[0]


def getCodigoAllSwift(cnxn: pyodbc.Connection):
    SPsql = f"SELECT * FROM Bancos"
    cursor = cnxn.cursor().execute(SPsql)
    codigos_swift = []
    for row in cursor.fetchall():
        # print(row)
        codigos_swift.append(row)
    return codigos_swift


def conectar(server, database, username, password):
    try:
        conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                                  server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        print('Conncted:', server, database, username, password)
        return conexion
    except Exception as e:
        print("Error al conectar a la base de datos", e)
        return None


def getNumeroLote(compania: str, fecha: str, cnxn: pyodbc.Connection):
    sql = f"select ISNULL( MAX(SUBSTRING(lotNumLote,7,2)) , 0) as lote from Lotesxbanco where lotCodCompania = '{compania}' and SUBSTRING(lotNumLote,1,6) = '{fecha}'"
    print(sql)
    result = cnxn.cursor().execute(sql)
    res = result.fetchone()
    return res[0]


def getCuentaBanco(cnxn: pyodbc.Connection):
    return execute_stored_procedure(cnxn, "EXEC GetCuentaBanco")


def getDataBNC(cnxn: pyodbc.Connection) -> str:
    return execute_stored_procedure(cnxn, "EXEC GetDataBNC")


def getTranredBangente(cnxn: pyodbc.Connection):
    SPsql = "EXEC SP_GetTranredBangente"
    result = cnxn.cursor().execute(SPsql)
    row = result.fetchone()
    return row[1], row[0]


def saveFile(job, name, afiliado_in, monto, totalRegistros, cnxn: pyodbc.Connection):
    query = f"INSERT INTO Files_Generated (job, name, agregador, monto, total) VALUES ('{job}', '{name}', '{afiliado_in}', {monto}, {totalRegistros})"
    # print(query)

    cursor = cnxn.cursor()
    cursor.execute(query)
    cnxn.commit()


def saveLoteXBancoSitran(lote: LotesBanco, afiliado: str, cnxn: pyodbc.Connection):
    stmt = (
        "INSERT INTO LotesXBanco (lotCodCompania, lotNumLote, lotTipoRegistro, lotCodMonedaDeb, "
        + "lotCodMonedaCred, lotActividadEcom, lotMotivoOpe, lotCuentaDebito, lotFechaValor, lotMontoTotal, lotCantidadPagos, lotAfiliado, lotTipoArchivo,lotBanco)"
        + " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,1,0104)"
    )
    params = (
        lote.lotCodCompania,
        lote.lotNumLote,
        lote.lotTipoRegistro,
        lote.lotCodMonedaDeb,
        lote.lotCodMonedaCred,
        lote.lotActividadEcom,
        lote.lotMotivoOpe,
        lote.lotCuentaDebito,
        lote.lotFechaValor,
        lote.lotMontoTotal,
        lote.lotCantidadPagos,
        afiliado,
    )

    with cnxn.cursor() as cursor:
        cursor.execute(stmt, params)
        cnxn.commit()
