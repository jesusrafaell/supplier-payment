import os
from typing import Tuple
from utils.db import getNumeroLote


def new_lote(cnxn, lotefile: str,) -> Tuple[str, str, str, int]:
    return int(getNumeroLote("D0U", lotefile, cnxn))


def new_loteInterno(numeroLote: int, lotefile: str, rutaArchivo: str) -> Tuple[str, str, str, int]:
    numeroLote = numeroLote + 1
    correlativo = str(numeroLote).zfill(2)
    nombre_archivo = lotefile + correlativo
    fichero = os.path.join(rutaArchivo, nombre_archivo + ".txt")
    if os.path.exists(fichero):
        os.remove(fichero)
    return nombre_archivo, fichero, correlativo, numeroLote
