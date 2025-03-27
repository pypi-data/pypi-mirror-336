import logging 
from logging.handlers import TimedRotatingFileHandler
from .fileaccess import get_package_path

logging.basicConfig(
    filename="golding_NEURON.log",
    filemode="a",
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
rotate_handler = TimedRotatingFileHandler(f'{get_package_path("logs")}/golding_NEURON.log', backupCount=3, when='D', interval=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotate_handler.setFormatter(formatter)
logging.getLogger().addHandler(rotate_handler)