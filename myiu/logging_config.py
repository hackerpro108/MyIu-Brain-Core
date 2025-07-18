import logging, sys
_is_configured = False
def setup_logging():
    global _is_configured
    if _is_configured: return
    log_format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format, datefmt="%Y-%m-%d %H:%M:%S", stream=sys.stdout)
    _is_configured = True
    logging.getLogger("myiu.init").info("Hệ thống logging đã được thiết lập.")
def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
