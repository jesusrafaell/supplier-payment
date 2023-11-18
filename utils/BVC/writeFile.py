from typing import List
from utils.BVC.BVC import saveCabezeraFile, saveRegistroBVCFile
import traceback
from utils.excel import make_report_excel
from utils.lote import new_loteInterno
from classes.Historico import Historico


def writeFileBVC(cnxn, log, arr: List[Historico], cuentaDebito: str, montoarchivo: float, rutaArchivo, afiliado: str, date_str: str, numeroLote: str, lotefile: str, fecha_objeto: str, list_switf) -> int:
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
                saveCabezeraFile(cnxn, nombre_archivo, nroRegistro, cumulativeAmount,
                                 cuentaDebito, fecha_objeto, file, nroAfiliado)
                contFiles += 1

                # print(nroAfiliado, 'lote', numeroLote, 'registros:', nroRegistro,
                #       'Monto file:', cumulativeAmount, 'rompe sumandole', registro.hisAmountTotal)

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
            saveRegistroBVCFile(cnxn, nombre_archivo, file,
                                afiliado, registro, cuentaDebito, list_switf, 0)

            cont += 1
            nroRegistro += 1

        # ultima cabezera del ultimo file
        # print(nroAfiliado, 'Monto final:', cumulativeAmount,
        #       'lote', numeroLote, 'registros:', nroRegistro)
        saveCabezeraFile(cnxn, nombre_archivo, nroRegistro, cumulativeAmount,
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


def writeFileBVC_Afiliado(cnxn, log, arr: List[Historico], cuentaDebito: str, montoarchivo: float, rutaArchivo, afiliado: str,  date_str: str, numeroLote: int, lotefile: str, fecha_objeto: str, list_switf) -> int:
    try:
        nombre_archivo, fichero, correlativo, numeroLote = new_loteInterno(
            numeroLote, lotefile, rutaArchivo)

        make_report_excel(date_str, arr, rutaArchivo, correlativo, 1)

        contFiles = 0
        cont = 0

        file = open(fichero, "w", encoding='utf-8')
        hisId = 0
        nroAfiliado = arr[0].aboCodAfi

        acumulative = 0.0
        print("Comenzar en el lote", numeroLote)
        while len(arr):

            for registro in arr:
                hisId += 1
                registro.hisId = str(hisId)
                registro.aboCodAfi = registro.aboCodAfi
                nroAfiliado = registro.aboCodAfi
                cont += 1

                if acumulative + registro.hisAmountTotal > montoarchivo:
                    contFiles += 1
                    aux = registro.hisAmountTotal
                    sustra = montoarchivo - acumulative
                    registro.hisAmountTotal = sustra
                    acumulative += sustra
                    saveRegistroBVCFile(cnxn, nombre_archivo, file,
                                        afiliado, registro, cuentaDebito, list_switf, 1)
                    saveCabezeraFile(cnxn, nombre_archivo, cont, acumulative,
                                     cuentaDebito, fecha_objeto, file, registro.aboCodAfi)
                    # print('save Registro', hisId, 'remove', registro.hisId,
                    #       registro.aboCodAfi, registro.hisAmountTotal)
                    nombre_archivo, fichero, correlativo, numeroLote = new_loteInterno(
                        numeroLote, lotefile, rutaArchivo)
                    # cerrar el file anterior
                    file.close()
                    # fin de cada files
                    # el registro le cada dinero
                    registro.hisAmountTotal = aux - sustra
                    # Abrir el nuevo fichero
                    file = open(fichero, "w", encoding='utf-8')

                    # print('Monto execito:', acumulative, 'new lote',
                    #       numeroLote, 'registros:', cont)
                    # numero de regisros en 0 por cada archivo
                    cont = 0
                    acumulative = 0.00
                    # salte del for y vuelve a recorrer para crear un nuevo archivo
                    break
                else:
                    saveRegistroBVCFile(cnxn, nombre_archivo, file,
                                        afiliado, registro, cuentaDebito, list_switf, 1)
                    # print('save Registro', hisId, 'remove', registro.hisId,
                    #       registro.aboCodAfi, registro.hisAmountTotal)
                    acumulative += registro.hisAmountTotal
                    # remover registro guardado
                    arr.remove(registro)

        saveCabezeraFile(cnxn, nombre_archivo, cont, acumulative,
                         cuentaDebito, fecha_objeto, file, nroAfiliado)

        # print(nroAfiliado, 'Monto Fin:', acumulative,
        #       'lote', numeroLote, 'registros:', cont)

        return numeroLote
    except Exception as e:
        print("Error", e)
        error_message = traceback.format_exc()
        log.write("Error: " + str(e) + "\n" + error_message + '\n')
        return -1
