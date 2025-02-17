from loguru import logger
import sys
import os

# Создаем папку для логов (если её нет)
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Удаляем стандартный логгер (чтобы избежать дублирования)
logger.remove()

# Настраиваем логирование в консоль с цветами
logger.add(
    sys.stderr, 
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "{name}:{line} | "
           "<level>{level: <8}</level> | "
           "<level>{message}</level>",
    colorize=True,
    level="DEBUG"
)

# Логирование в файл (архивируем при достижении 5 MB)
logger.add(
    f"{LOG_DIR}/app.log", 
    rotation="5 MB", 
    compression="zip", 
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{line} - {message}",
    level="INFO"
)

# Готовый логгер для использования в других модулях
log = logger

