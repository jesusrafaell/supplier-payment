from datetime import datetime
from classes.Historico import Historico
from typing import Tuple
from utils.utilitis import delete_sings, delete_sings_email, get_codigo_swift, getTipoCuentaAbono, leftPad, rightPad, rounder


def getCabezeraPlaza(nombre_archivo: str, cont: int, montoTotal: str, cuentaDebito: str, strDate: str) -> str:
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


def getDetailPlaza(registro: Historico) -> str:
    fecha_string = registro.hisFecha.strftime('%Y-%m-%d')
    hisFecha = fecha_string.split()[0]
    lotConceptoPago = str(
        "Abono GSComputer: " +
        registro.comerRif.strip() + " " +
        registro.hisLote.strip() + " " +
        registro.aboTerminal.strip() + " " +
        str(hisFecha)
    )
    return (
        "J00003103756"  # Rif empresa origen tranred //12
        + leftPad(str(registro.comerDesc.strip()), 50, ' ')
        + str(registro.comerRif[0])  #
        + leftPad(str(registro.comerRif[1:].strip()), 11, '0')
        + leftPad(str(registro.contMail.strip()), 50, ' ')
        + 'CC'  
        + leftPad(str(registro.aboNroCuenta), 20, '0')
        + leftPad(str(rounder(registro.hisAmountTotal)
                      ).replace(".", "").replace(",", ""), 17, '0')
        + rightPad(lotConceptoPago, 140, ' ')
        + leftPad(str(registro.contTelefMov), 11, '0')
    )
