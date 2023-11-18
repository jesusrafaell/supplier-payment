import datetime
import pyodbc
from utils.utilitis import leftPad


class LotesBanco:
    def __init__(self):
        self.id = None
        self.lotCodCompania = None
        self.lotNumLote = None
        self.lotTipoRegistro = 0
        self.lotCodMonedaDeb = None
        self.lotCodMonedaCred = None
        self.lotActividadEcom = 0
        self.lotMotivoOpe = 0
        self.lotCuentaDebito = None
        self.lotFechaValor = None
        self.lotMontoTotal = None
        self.lotCantidadPagos = 0


def init__cabezera(cont: int, cuentaDebito: str, strDate: str, montoTotal: str, nombre_archivo: str):
    lote = LotesBanco()
    lote.lotActividadEcom = 00
    lote.lotCantidadPagos = str(cont)
    lote.lotCodCompania = "D0U"
    lote.lotCodMonedaCred = "VES"
    lote.lotCodMonedaDeb = "VES"
    lote.lotCuentaDebito = leftPad(cuentaDebito, 25, '0')
    lote.lotFechaValor = strDate
    lote.lotMontoTotal = montoTotal
    lote.lotMotivoOpe = 000
    lote.lotNumLote = nombre_archivo
    lote.lotTipoRegistro = 9
    return lote


def clearLoteXBanco(cnxn, fecha: datetime):
    fecha_string = fecha.strftime('%Y-%m-%d')
    fecha = fecha_string.split()[0]
    sqlClear = f"delete LotesXBanco where lotFechaValor = '{fecha}'"
    cnxn.cursor().execute(sqlClear)


def saveLoteCabecera(lote: LotesBanco, afiliado: str, cnxn: pyodbc.Connection):
    stmt = (
        "INSERT INTO LotesXbanco (lotCodCompania, lotNumLote, lotTipoRegistro, lotCodMonedaDeb, "
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
