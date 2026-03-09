import extractor, transformador, cargador
import logging
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

logger = logging.getLogger("pipeline")
handler = logging.FileHandler("logs/pipeline.log", encoding="utf-8")
handler.setFormatter(logging.Formatter("%(asctime)s — %(levelname)s — %(message)s"))
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

def main():
    
        inicio = datetime.now()
        logger.info(f"Pipeline iniciado a las: {inicio}\n")
    
        # Extractor:
        ids = extractor.obtener_ids(200)
        items = extractor.extraer(list_ids=ids, cantidad=200)
        extractor.guardar(items)
        
        logger.info(f"Se han extraido {len(ids)} id's.")
        logger.info(f"Se han guardado {len(items)} sucios en data/raw/items.json")
        
        # Transformador:
        datos = transformador.leer_crudos()
        items_limpios = transformador.transformar(datos)
        transformador.guardar_limpios(items_limpios)
        
        logger.info(f"Se han transformado {len(datos)} posts sucios.")
        logger.info(f"Se han guardado {len(items_limpios)} posts limpios en data/processed/items.json.")
        
        # Cargador:
        data = cargador.leer_limpios()
        cargador.cargar_en_bd(items=data)
        
        logger.info(f"Se han cargado {len(data)} posts limpios en la base de datos.\n")
        
        finalizacion = datetime.now()
        duracion = finalizacion - inicio
        
        logger.info(f"Pipeline finalizado a las: {finalizacion}")
        logger.info(f"Duración del pipeline: {duracion}\n")
        

scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', hours=6)
def trabajo():
    main()

main()
scheduler.start()