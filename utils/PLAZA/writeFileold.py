import os
import traceback
from typing import List
from datetime import datetime
from utils.db import getNumeroLote, saveLoteCabecera, saveLoteDetalle
from classes.Historico import Historico
from classes.LoteBanco import LotesBanco
from classes.LoteDetalle import LoteDetalle
from utils.utilitis import getTipoCuentaAbono, leftPad, rightPad, rounder


class FilePlaza:
    def get_monto_total(arr: List[Historico]) -> int:
        # Get montototal del archivo
        montoTotal = 0
        for registro in arr:
            montoTotal += registro.hisAmountTotal
        return montoTotal

    def writeFileBPLAZA(cnxn, log, arr: List[Historico], ahora: datetime, cuentaDebito: str, montoarchivo: float, reportBeginFile: str, rutaArchivo) -> int:
        try:
            # 1 crea el primer archivo
            dayS = str(datetime.now().day).zfill(2)
            monthS = str(datetime.now().month).zfill(2)
            valueafiliado = reportBeginFile
            lotefile = str(valueafiliado) + monthS + dayS
            numeroLote = int(getNumeroLote("D0U", lotefile, cnxn)) + 1
            nombre_archivo = lotefile + str(numeroLote).zfill(2)
            fichero = os.path.join(rutaArchivo, nombre_archivo + ".txt")
            # crea el primer archivo
            if os.path.exists(fichero):
                os.remove(fichero)
            # 1
            # Codigo
            cumulativeAmount = float(0)
            cont = 1
            nroAfiliado = 0
            for registro in arr:
                cumulativeAmount += registro.hisAmountTotal

                # si cambia el afiliado
                if registro.aboCodAfi != registro.aboCodAfi:
                    nroAfiliado = registro.aboCodAfi

                # crea un nuevo archivo si pasa el monto
                if cumulativeAmount > montoarchivo:
                    # guarda la cabecera anterio
                    formatted_cabecera = ahora.strftime('%Y-%m-%d')
                    loteCabecera = LotesBanco()
                    loteCabecera.lotCodCompania = "D0U"
                    loteCabecera.lotNumLote = nombre_archivo
                    loteCabecera.lotTipoRegistro = 9
                    loteCabecera.lotCodMonedaCred = "VES"
                    loteCabecera.lotCodMonedaDeb = "VES"
                    loteCabecera.lotActividadEcom = 00
                    loteCabecera.lotMotivoOpe = 000
                    loteCabecera.lotCantidadPagos = cont
                    loteCabecera.lotCuentaDebito = leftPad(
                        cuentaDebito, 25, '0')
                    loteCabecera.lotFechaValor = formatted_cabecera
                    loteCabecera.lotMontoTotal = montoTotal
                    # insert
                    saveLoteCabecera(loteCabecera, nroAfiliado, cnxn)
                    # save cabecera
                    numeroLote = int(getNumeroLote(
                        "D0U", lotefile, cnxn)) + 1
                    nombre_archivo = lotefile + str(numeroLote).zfill(2)
                    fichero = os.path.join(
                        rutaArchivo, nombre_archivo + ".txt")
                    cumulativeAmount = float(0)
                    if os.path.exists(fichero):
                        os.remove(fichero)

                # sigue con el mismo registro
                with open(fichero, "a", encoding='utf-8') as file:
                    # formatted_time = ahora.strftime("%H%M%S")
                    loteDetalle2 = LoteDetalle()

                    montoTotal = registro.hisAmountTotal

                    lotConceptoPago = str(
                        "Abono GSComputer: " +
                        registro.comerRif.strip() + " " +
                        registro.hisLote.strip() + " " +
                        registro.aboTerminal.strip() + " " +
                        str(registro.hisFecha)
                    )

                    detail = (
                        "J00003103756"  # Rif empresa origen tranred //12
                        # Nombre beneficiario //50
                        + leftPad(str(registro.comerDesc.strip()), 50, ' ')
                        + str(registro.comerRif[0])  # Rif Type Doc
                        # Rif 11
                        + leftPad(str(registro.comerRif[1:].strip()), 11, '0')
                        # Correo beneficiario //50
                        + leftPad(str(registro.contMail.strip()), 50, ' ')
                        + 'CC'  # tipo de pago 2
                        + leftPad(str(registro.aboNroCuenta), 20, '0')
                        + leftPad(str(rounder(registro.hisAmountTotal)
                                      ).replace(".", "").replace(",", ""), 17, '0')
                        + rightPad(lotConceptoPago, 140, ' ')
                        + leftPad(str(registro.contTelefMov), 11, '0')
                    )

                    # Detail 1
                    loteDetalle1 = LoteDetalle.init__line1(
                        "D0U",
                        nombre_archivo,
                        registro.hisId,
                        4,
                        registro.contMail,
                        registro.comerRif,
                        rounder(registro.hisAmountTotal)
                    )

                    # insert
                    saveLoteDetalle(loteDetalle1, cnxn)

                    tipoCuentaAbono = getTipoCuentaAbono(
                        registro.aboCodBanco)

                    # Linea 2 save
                    loteDetalle2 = LoteDetalle.init__line2(
                        "D0U",
                        nombre_archivo,
                        registro.hisId,
                        5,
                        rounder(registro.hisAmountTotal),
                        registro.comerDesc,
                        tipoCuentaAbono,
                        registro.aboNroCuentaBanco,
                        "VES",
                        "VES",
                        lotConceptoPago,
                        "",
                        "BIC",
                        000,
                        00,
                        leftPad(cuentaDebito, 25, '0')
                    )

                    # insert
                    saveLoteDetalle(loteDetalle2, cnxn)

                    file.write(detail + "\n")
                    cont += 1
                    # end for

            # guarda el ultimo o el unico registro en la cabezera
            formatted_cabecera = ahora.strftime('%Y-%m-%d')
            loteCabecera = LotesBanco()
            loteCabecera.lotCodCompania = "D0U"
            loteCabecera.lotNumLote = nombre_archivo
            loteCabecera.lotTipoRegistro = 9
            loteCabecera.lotCodMonedaCred = "VES"
            loteCabecera.lotCodMonedaDeb = "VES"
            loteCabecera.lotActividadEcom = 00
            loteCabecera.lotMotivoOpe = 000
            loteCabecera.lotCantidadPagos = cont
            loteCabecera.lotCuentaDebito = leftPad(cuentaDebito, 25, '0')
            loteCabecera.lotFechaValor = formatted_cabecera
            loteCabecera.lotMontoTotal = montoTotal
            # insert
            saveLoteCabecera(loteCabecera, nroAfiliado, cnxn)
            print('Total registros', cont)
            return 1
        except Exception as e:
            # Captura cualquier excepción y escribe el mensaje de error en el archivo log.txt
            print("Error", e)
            error_message = traceback.format_exc()
            log.write("Error: " + str(e) + "\n" + error_message + '\n')
            return -1
