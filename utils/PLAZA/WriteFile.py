from typing import List
from datetime import datetime
import traceback
from utils.excel import make_report_excel
from utils.lote import new_loteInterno
from classes.Historico import Historico
from utils.PLAZA.PLAZA import saveCabezeraPlazaFile, saveRegistroPlazaFile


def writeFilePlaza(cnxn, log, arr: List[Historico], cuentaDebito: str, montoarchivo: float, rutaArchivo, afiliado: str, date_str: str, numeroLote: str, lotefile: str, fecha_objeto: str) -> int:
    try:
        nombre_archivo, fichero, correlativo, numeroLote = new_loteInterno(
            numeroLote, lotefile, rutaArchivo)

        cumulativeAmount = 0.0
        contFiles = 0
        cont = 0
        nroRegistro = 0
        nroAfiliado = arr[0].aboCodAfi
        initExcel = 0

        # Abrir fichero
        print('primer lote:', numeroLote)
        file = open(fichero, "w", encoding='utf-8')
        for registro in arr:
            if cumulativeAmount + registro.hisAmountTotal > montoarchivo or nroAfiliado != registro.aboCodAfi:
                saveCabezeraPlazaFile(cnxn, nombre_archivo, nroRegistro, cumulativeAmount,
                                      cuentaDebito, fecha_objeto, file, nroAfiliado)
                contFiles += 1

                print(nroAfiliado, 'lote', numeroLote, 'registros:', nroRegistro,
                      'Monto file:', cumulativeAmount, 'rompe sumandole', registro.hisAmountTotal)

                nombre_archivo, fichero, new_correlativo, numeroLote = new_loteInterno(
                    numeroLote, lotefile, rutaArchivo)

                if nroAfiliado != registro.aboCodAfi:
                    make_report_excel(
                        date_str, arr[initExcel:cont], rutaArchivo, correlativo, 0)
                    nroAfiliado = registro.aboCodAfi
                    initExcel = cont
                    correlativo = new_correlativo

                # cerrar el archivo anterior
                file.close()
                # Abrir el nuevo fichero
                cumulativeAmount = 0.0
                nroRegistro = 0
                file = open(fichero, "w", encoding='utf-8')

            cumulativeAmount += registro.hisAmountTotal
            saveRegistroPlazaFile(cnxn, nombre_archivo, file,
                                  afiliado, registro, cuentaDebito)

            cont += 1
            nroRegistro += 1

        # ultima cabezera del ultimo file
        # print(nroAfiliado, 'Monto final:', cumulativeAmount,
        #       'lote', numeroLote, 'registros:', nroRegistro)
        saveCabezeraPlazaFile(cnxn, nombre_archivo, nroRegistro, cumulativeAmount,
                              cuentaDebito, fecha_objeto, file, nroAfiliado)

        file.close()
        make_report_excel(
            date_str, arr[initExcel:cont], rutaArchivo, correlativo, 0)

        return numeroLote
    except Exception as e:
        print("Error", e)
        error_message = traceback.format_exc()
        log.write("Error writefile: " + str(e) + "\n" + error_message + '\n')
        return -1
