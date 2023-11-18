from io import TextIOWrapper
from classes.Historico import Historico
from classes.LoteBanco import init__cabezera, saveLoteCabecera
from classes.LoteDetalle import init__line1, init__line2
from utils.BVC.formatLines import getCabezeraBVC, getLine1BVC, getLine2BVC
from utils.utilitis import leftPad, rounder


def saveRegistroBVCFile(cnxn,  # conecion
                        nombre_archivo: str,  # nombre file
                        file: TextIOWrapper,  # file
                        afiliado: str,  # afilido
                        registro: Historico,  # registro
                        cuentaDebito: str,  # numero cuenta
                        list_switf,  # lista de codigos switf
                        op: int  # si es afiliado o terminal
                        ):
    linea1 = getLine1BVC(registro, nombre_archivo)
    linea2, tipoCuentaAbono, lotConceptoPago = getLine2BVC(cnxn, registro, nombre_archivo,
                                                           afiliado, cuentaDebito, list_switf, op)
    loteDetalle1 = init__line1(
        "D0U",
        nombre_archivo,
        registro.hisId,
        4,
        registro.contMail,
        registro.comerRif,
        rounder(registro.hisAmountTotal)
    )

    loteDetalle2 = init__line2(
        "D0U",
        nombre_archivo,
        registro.hisId,
        5,
        rounder(registro.hisAmountTotal),
        registro.comerDesc,
        tipoCuentaAbono,
        registro.aboNroCuenta,
        "VES",
        "VES",
        lotConceptoPago,
        "",
        "BIC",
        000,
        00,
        leftPad(cuentaDebito, 25, '0')
    )

    file.writelines([linea1.strip() + '\n', linea2.strip() + '\n'])

    # saveLoteDetalles(cnxn, loteDetalle1, loteDetalle2)


def saveCabezeraFile(cnxn, nombre_archivo, cont, cumulativeAmount, cuentaDebito, fecha_objeto, file, nroAfiliado):
    cabecera = getCabezeraBVC(
        nombre_archivo, cont, cumulativeAmount, cuentaDebito, fecha_objeto)
    loteCabecera = init__cabezera(
        cont-1, cuentaDebito, fecha_objeto, cumulativeAmount, nombre_archivo)
    file.write(cabecera)
    # guarda en DB
    saveLoteCabecera(loteCabecera, nroAfiliado, cnxn)
