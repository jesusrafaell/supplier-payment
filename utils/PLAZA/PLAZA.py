from io import TextIOWrapper
from classes.Historico import Historico
from classes.LoteBanco import init__cabezera, saveLoteCabecera
from classes.LoteDetalle import init__line1, init__line2, saveLoteDetalles
from utils.PLAZA.formatLines import getDetailPlaza
from utils.utilitis import getTipoCuentaAbono, leftPad, rounder


def saveRegistroPlazaFile(cnxn,  # conecion
                          nombre_archivo: str,  # nombre file
                          file: TextIOWrapper,  # file
                          afiliado: str,  # afilido
                          registro: Historico,  # registro
                          cuentaDebito: str,  # numero cuenta
                          ):

    fecha_string = registro.hisFecha.strftime('%Y-%m-%d')
    hisFecha = fecha_string.split()[0]
    linea1 = getDetailPlaza(registro)
    lotConceptoPago = str('Abono por concepto ' + afiliado + ' comercio: ' +
                          registro.comerRif.strip() + " " +
                          registro.hisLote.strip() + " " +
                          registro.aboTerminal.strip() + " " +
                          str(hisFecha))

    tipoCuentaAbono = getTipoCuentaAbono(
        registro.aboCodBanco)

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

    file.writelines([linea1.strip() + '\n'])

    saveLoteDetalles(cnxn, loteDetalle1, loteDetalle2)


def saveCabezeraPlazaFile(cnxn, nombre_archivo, cont, cumulativeAmount, cuentaDebito, fecha_objeto, file, nroAfiliado):
    loteCabecera = init__cabezera(
        cont-1, cuentaDebito, fecha_objeto, cumulativeAmount, nombre_archivo)
    # guarda en DB
    saveLoteCabecera(loteCabecera, nroAfiliado, cnxn)
