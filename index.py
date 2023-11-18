import os
import sys
from sitran import *
from datetime import datetime
# bangente
from Bangente.classes.Historico import Historico
from utils.sftp import sftp
# paso 2
from classes.Historico import getHistoricoPagoList
from classes.LoteBanco import clearLoteXBanco
from utils.db import GetCuentaDebito, GetMontoBPLAZA, GetMontoBVC,  conectar, getCodigoAllSwift, getTranredBangente, saveFile
from utils.excel import make_report_excel
from utils.lote import new_lote
# bangente
from classes.HistoricoBangete import getHistoricoPago_Bangete
from Bangente.variables import *
from Bangente.utils.writeFile import writeFileBangente
# bvc
from utils.BVC.writeFile import writeFileBVC, writeFileBVC_Afiliado
# plaza
from utils.PLAZA.WriteFile import writeFilePlaza
# from utils.PLAZA.writeFileold import FilePlaza

ahora = datetime.now()

afiliado_in = sys.argv[1]
reportBeginFile = sys.argv[2]
server_in = sys.argv[3]
database_in = sys.argv[4]
username_in = sys.argv[5]
password_in = sys.argv[6]
afi = sys.argv[7]
strDate = ahora.strftime("%y%m%d")
op = 1

if len(sys.argv) > 8:
    strDate = sys.argv[8]
    op = sys.argv[9]


if afi != '720' and afi != '722' and afi != '872':
    print('no existe ese afiliado')
    sys.exit()

rutaArchivo = 'Paso2'

# strDate = datetime.now().strftime("%y%m%d") if len(
#     sys.argv) <= 9 else sys.argv[10]

print('afiliado_in:', afiliado_in)
print('server:', server_in)
print('db:', database_in)
print('username:', username_in)
print('password:', password_in)
print('Ruta', rutaArchivo)
print('afi:', afi)
print('fecha:', strDate)
print('op:', op)

# Log
log_file = os.path.join(os.getcwd(), 'log', "logApp.txt")
os.makedirs(rutaArchivo, exist_ok=True)

date = datetime.now()
with open(log_file, "w") as log:
    cnxn = conectar(server_in, database_in, username_in, password_in)
    # Crea la carpeta para los registros
    rutaArchivo = os.path.join(rutaArchivo, strDate)
    os.makedirs(rutaArchivo, exist_ok=True)

    # Crear carpeta para los excel
    rutaExcel = os.path.join(rutaArchivo, 'Excel')
    os.makedirs(rutaExcel, exist_ok=True)
    if (cnxn):
        print("PROCESO INICIADO -----------------------------------------------")
        dateNow = datetime.strptime(
            date.strftime('%Y-%m-%d'), '%Y-%m-%d')

        # obtener la cuenta debito
        cuentaDebito = '0000001040107160107199659'
        if afi == '720' or afi == '722':
            cuentaDebito = GetCuentaDebito(cnxn, afi)

        # crear el nombre de los archivos y buscar el primer lote
        lotefile = dateNow.strftime('%y%m%d')
        fecha_objeto = dateNow.strftime('%y%m%d')
        if database_in.upper() != 'MILPAGOS' or afi == '872':
            day = datetime.now().day
            month = datetime.now().month
            dayS = str(day).zfill(2)
            monthS = str(month).zfill(2)

            valueafiliado = reportBeginFile
            lotefile = str(valueafiliado) + monthS + dayS

        numeroLote = new_lote(
            cnxn, lotefile)

        print('lote:', numeroLote)

        if (afi == '872'):

            cnxnSitran = conectar(
                host_sitran, db_sitran, username_sitran, password_sitran)

            if (cnxnSitran):
                print('Contected Sitran')
                numeroLote = new_lote(
                    cnxnSitran, lotefile)
                print('Bangente', numeroLote)
                hoy = ahora.strftime("%y%m%d")

                print('Hoy:', hoy)
                print('Date:', strDate)

                fecha = datetime.strptime(hoy, "%y%m%d")
                dateBangente = datetime.now().replace(
                    year=fecha.year, month=fecha.month, day=fecha.day)

                # Log
                print("Connected to DB")
                result = Historico.getHistoricoPagoList(strDate, cnxn, op)
                # Get Historico

                print(len(result))

                if len(result):
                    print('Number of records: ', len(result))

                    day = datetime.now().day
                    month = datetime.now().month
                    dayS = str(day).zfill(2)
                    monthS = str(month).zfill(2)

                    numeroLote += 1

                    nombre_archivo = lotefile + str(numeroLote).zfill(2)

                    print('Today:', ahora)
                    print('Date run:', dateBangente)

                    # Ficheros
                    nombre_base = fecha.strftime("%Y%m%d") + "PAGOS"
                    nombre_archivo_bangente = (
                        nombre_base + str(numeroLote).zfill(2))
                    fichero = os.path.join(
                        rutaArchivo, nombre_archivo_bangente + ".txt")

                    if os.path.exists(fichero):
                        os.remove(fichero)

                    # Generate excel from Historico
                    correlativo = str(numeroLote).zfill(2)
                    make_report_excel(
                        strDate, result, rutaArchivo, correlativo, 0)

                    # Generate Archivo for bangete txt
                    print(host_sitran, db_sitran,
                          username_sitran, password_sitran)
                    numeroLote, monto = writeFileBangente(result, dateBangente, fichero, numeroLote,
                                                          nombre_archivo, cnxn, log, afiliado_in, cnxnSitran)

                    if (numeroLote != -1):
                        saveFile('PagoProveedores Bangente', nombre_archivo_bangente + '.txt', database_in, monto,
                                 len(result), cnxnSitran)

                    # Pasar el archivo
                    if sftp(fichero, nombre_archivo_bangente + '.txt'):
                        print('Process completed SFTP!!')
                        # log.write(" Error: " + 'Process completed!!' + "\n")
                    else:
                        print('Process error SFTP!!')
                        # log.write(" Error: " + "Process error SFTP!!" + "\n")
        if afi == '720':
            clearLoteXBanco(cnxn, dateNow)
            result = getHistoricoPagoList(strDate, cnxn, afi)  # Get Historico
            # obtener los codigos swift
            list_switf = getCodigoAllSwift(cnxn)
            # Obtener totos los datos de la base de datos
            montoarchivo = GetMontoBVC(cnxn)
            rif, cuentaDebitoBangente = getTranredBangente(cnxn)
            resultBangente = getHistoricoPago_Bangete(
                strDate, cnxn, cuentaDebitoBangente, rif)

            # reportBeginFile: str
            print('BVC', 'maximo monto:', montoarchivo)
            if len(result) > 0:
                numeroLote = writeFileBVC(cnxn, log, result, cuentaDebito, float(
                    montoarchivo), rutaArchivo, afiliado_in, strDate,  numeroLote, lotefile, fecha_objeto, list_switf)

            print('BVC -> Bangentea', len(resultBangente))
            if len(resultBangente) > 0:
                numeroLote = writeFileBVC_Afiliado(cnxn, log, resultBangente, cuentaDebito, float(montoarchivo),
                                                   rutaArchivo, afiliado_in,  strDate, numeroLote, lotefile, fecha_objeto, list_switf)

        elif afi == '722':
            clearLoteXBanco(cnxn, dateNow)
            result = getHistoricoPagoList(strDate, cnxn, afi)  # Get Historico
            if len(result) > 0:
                montoarchivo = GetMontoBPLAZA(cnxn)
                print('PLAZA', 'maximo monto:', montoarchivo)
                numeroLote = writeFilePlaza(cnxn, log, result, cuentaDebito, float(
                    montoarchivo), rutaArchivo, afiliado_in, strDate,  numeroLote, lotefile, fecha_objeto)

        if numeroLote > 0:
            print(
                "PROCESO FINALIZADO -----------------------------------------------")
        else:
            if (numeroLote != -1):
                print("No hay registros.")
                print('PROCESO FINALIZADO ---------------------------------------------')
            log.write(str(datetime.now()) + " Error: " +
                      "No records found" + "\n")
    else:
        print("Error connecting to DB")

fin = datetime.now()
duracion = fin - date
minutos = duracion.seconds // 60
segundos = duracion.seconds % 60

minutos_str = str(minutos).zfill(2)
segundos_str = str(segundos).zfill(2)

print("Total time: {}:{}".format(minutos_str, segundos_str))
