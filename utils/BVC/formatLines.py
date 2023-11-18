from datetime import datetime
from classes.Historico import Historico
from typing import Tuple
from utils.utilitis import delete_sings, delete_sings_email, get_codigo_swift, getTipoCuentaAbono, leftPad, rightPad, rounder


def getCabezeraBVC(nombre_archivo: str, cont: int, montoTotal: str, cuentaDebito: str, strDate: str) -> str:
    date_dt = datetime.strptime(strDate, '%y%m%d')
    date = date_dt.strftime('%Y%m%d')
    return (
        'D0U'
        + leftPad(str(nombre_archivo), 8, '0')
        + leftPad('', 16, '0')
        + '9'
        + date
        + leftPad(str(rounder(montoTotal)
                      ).replace(".", "").replace(",", ""), 15, '0')
        + leftPad(str(cont), 15, '0')
        + 'VES'
        + rightPad(str(cuentaDebito), 35, ' ')
        + rightPad('', 35, ' ')
        + leftPad(str(rounder(montoTotal)
                      ).replace(".", "").replace(",", ""), 15, '0')
        + 'VES'
        + rightPad('', 30, ' ')
        + '00000'
        + rightPad('', 307, ' ')
        + 'X'
    )


def getLine1BVC(registro: Historico, nombre_archivo: str) -> str:

    mail = delete_sings_email(registro.contMail)
    return (
        'D0U'
        + nombre_archivo
        + leftPad(str(registro.hisId), 8, '0')
        + leftPad('', 8, '0')
        + '4'
        + rightPad(mail, 129, ' ')
        + str(registro.comerRif[0])
        + leftPad(str(registro.comerRif[1:]), 16, '0')
        + rightPad('', 325, ' ')
        + 'X'
    )


def getLine2BVC(cnxn, registro: Historico, nombre_archivo: str, afiliado: str, cuentaDebito: str, list_switf, op: int) -> Tuple[str, str, str]:
    fecha_string = registro.hisFecha.strftime('%Y-%m-%d')
    hisFecha = fecha_string.split()[0]
    lotConceptoPago = str('Abono por concepto ' + afiliado + ' comercio: ' +
                          registro.comerRif.strip() + " " +
                          registro.hisLote.strip() + " " +
                          registro.aboTerminal.strip() + " " +
                          str(hisFecha))
    if op == 1:
        lotConceptoPago = str('Abono por concepto ' + afiliado + ' comercio: ' +
                              registro.comerRif.strip() + " " +
                              registro.aboCodAfi.strip() + " " +
                              str(hisFecha))

    tipoCuentaAbono = getTipoCuentaAbono(
        registro.aboCodBanco)

    codigoSwift = get_codigo_swift(str(registro.aboNroCuenta[0:4]), list_switf)

    comerDesc = delete_sings(registro.comerDesc)
    return (
        'D0U'
        + nombre_archivo
        + leftPad(str(registro.hisId), 8, '0')
        + leftPad('', 8, '0')
        + '5'
        + leftPad(str(rounder(registro.hisAmountTotal)
                      ).replace(".", "").replace(",", ""), 15, '0')
        + rightPad(comerDesc, 60, ' ')
        + tipoCuentaAbono
        + rightPad('', 17, ' ')
        + '000'
        + rightPad('', 4, ' ')
        + rightPad(str(registro.aboNroCuenta), 35, ' ')
        + 'VESVES'
        + rightPad('', 28, ' ')
        + rightPad(str(lotConceptoPago), 105, ' ')
        + rightPad('', 6, ' ')
        + rightPad(codigoSwift, 12, ' ')
        + 'BIC'
        + rightPad(' ', 132, ' ')
        + rightPad(leftPad(cuentaDebito,
                           25, '0'), 35, ' ')
        + rightPad('', 9, ' ')
        + 'X'
    ), tipoCuentaAbono, lotConceptoPago
