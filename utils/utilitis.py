import datetime
from typing import List, Tuple, Union
import unicodedata
from classes.Historico import Historico
import re


def rounder(num: float):
    if num.is_integer():
        return str(int(num)) + '.00'
    else:
        return "{:.2f}".format(num)


def convierteFechaSql(fecha):
    df = datetime.datetime.strptime(fecha, '%d-%m-%Y')
    fechaSql = df.date()
    return fechaSql


def getFechaActual():
    ahora = datetime.datetime.now()
    formateador = ahora.strftime('%d-%m-%Y')
    return formateador


def getFechaActualSql():
    ahora = datetime.datetime.now()
    fechaSql = ahora.date()
    return fechaSql


def getHoraActual():
    ahora = datetime.datetime.now()
    formateador = ahora.strftime('%H:%M:%S')
    return formateador


def sumarFechasDias(fecha, dias):
    fecha = fecha + datetime.timedelta(days=dias)
    return fecha


def restarFechasDias(fecha, dias):
    fecha = fecha - datetime.timedelta(days=dias)
    return fecha


def diferenciasDeFechas(fechaInicial, fechaFinal):
    fechaInicial = datetime.datetime.strptime(
        str(fechaInicial), '%Y-%m-%d')
    fechaFinal = datetime.datetime.strptime(str(fechaFinal), '%Y-%m-%d')
    diferencia = fechaFinal - fechaInicial
    dias = diferencia.days
    return dias


def deStringToDate(fecha):
    fechaEnviar = datetime.datetime.strptime(fecha, '%d-%m-%Y')
    return fechaEnviar.date()


def get_dataBanco(historicos: List[Historico]) -> Tuple[str, str]:
    comerRif = historicos[0].comerRifBanco
    nro_cuenta = historicos[0].aboNroCuentaBanco
    return comerRif, nro_cuenta


def get_rif_prefix(rif_prefix) -> str:
    tipoDoc = "01"
    if rif_prefix == "V":
        tipoDoc = "01"
    elif rif_prefix in ["P", "J"]:
        tipoDoc = "02"
    elif rif_prefix == "E":
        tipoDoc = "08"
    return tipoDoc


def getTipoCuentaAbono(value: str) -> str:
    if value == "0104":
        return "1"
    else:
        return "3"


def convierteFechaSql(fecha: str) -> Union[None, datetime.date]:
    try:
        fechaUtil = datetime.strptime(fecha, '%d-%m-%Y')
    except ValueError:
        return None

    fechaSql = fechaUtil.date()

    return fechaSql


def rightPad(string: str, length: int, fill_char: str) -> str:
    if len(string) > length:
        return string[:length]
    else:
        return string + (fill_char * (length - len(string)))


def leftPad(string: str, longitud: int, caracter: str) -> str:
    # Convierte el número a una cadena de texto y rellena con el carácter especificado
    cadena_rellena = str(string).rjust(longitud, caracter)

    # Si la cadena resultante es más larga que la longitud especificada, cártala
    if len(cadena_rellena) > longitud:
        cadena_rellena = cadena_rellena[:longitud]

    return cadena_rellena


def getHistoricoTranred(cuentaDebito: str, rif: str) -> Historico:
    correoTranred = 'tranred@tranred.com.ve'
    registroTranred = Historico()
    registroTranred.hisId = '1'
    registroTranred.hisLote = '1'
    registroTranred.aboCodComercio = 0
    registroTranred.aboTerminal = '00000000'
    registroTranred.aboCodBanco = cuentaDebito[0:4]
    registroTranred.aboNroCuenta = cuentaDebito
    registroTranred.aboNroCuentaBanco = cuentaDebito
    registroTranred.aboTipoCuenta = ''
    registroTranred.comerDesc = 'TRANRED'
    registroTranred.comerTipoPer = 2
    registroTranred.comerRif = rif
    registroTranred.comerRifBanco = ''
    registroTranred.contNombres = "TRANRED"
    registroTranred.contApellidos = "CA"
    registroTranred.contTelefLoc = ""
    registroTranred.contTelefMov = ""
    registroTranred.contMail = correoTranred
    registroTranred.hisAmountTotal = 0.00
    registroTranred.hisFecha = datetime.datetime.now()
    return registroTranred


def delete_sings(cadena: str):
    cadena_normalizada = unicodedata.normalize('NFKD', cadena)
    cadena_sin_especiales = re.sub(r'[^\w\s]', '', cadena_normalizada)
    return cadena_sin_especiales


def delete_sings_email(cadena: str):
    cadena_normalizada = unicodedata.normalize('NFKD', cadena)
    cadena_sin_especiales = re.sub(r'[^a-zA-Z0-9\s]', '', cadena_normalizada)
    return cadena_sin_especiales


def get_codigo_swift(banco: str, list_switf) -> str:
    for row in list_switf:
        if row[0] == banco:
            return row[2]  # Retorna el valor del campo banSwift

    return ""  # Si no se encuentra el banco, retorna una cadena vacía
