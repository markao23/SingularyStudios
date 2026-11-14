import sys
sys.path.append('src')
from bot.main import setup_logging
setup_logging()
import logging
logging.info('Test info log')
logging.error('Test error log')
raise RuntimeError('Intentional exception for logging test')
