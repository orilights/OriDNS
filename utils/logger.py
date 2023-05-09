import sys
from loguru import logger

logger.remove(handler_id=None)

logger.add(sys.stdout, level='INFO')
logger.add('./logs/dh_{time}.log', level='DEBUG', encoding='utf-8')
