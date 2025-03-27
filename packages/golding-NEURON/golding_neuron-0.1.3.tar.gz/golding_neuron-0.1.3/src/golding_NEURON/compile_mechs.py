import subprocess
import logging
from .fileaccess import get_package_path

# Set up logging
logger = logging.getLogger(__name__)
def main():
    logger.info("Compiling mechanisms")
    subprocess.run(["nrnivmodl",get_package_path("mechanisms")])
    logger.info("Mechanisms compiled successfully")
if __name__ == "__main__":
    main()
