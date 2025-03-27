import logging
from pathlib import Path
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pytoos")

def remove_py_file(file_path: str, confirm: bool = False) -> bool:
    """
    Безопасно удаляет .py-файл.
    
    Args:
        file_path: Путь к файлу
        confirm: Запрашивать подтверждение
        
    Returns:
        bool: Успешно ли удалён файл
        
    Examples:
        >>> remove_py_file("old_script.py")
    """
    try:
        path = Path(file_path).with_suffix(".py")
        
        if not path.exists():
            logger.error(f"Файл {path} не найден.")
            return False
            
        if confirm:
            response = input(f"Удалить файл {path}? [y/N]: ")
            if response.lower() != 'y':
                logger.info("Удаление отменено.")
                return False
                
        os.remove(path)
        logger.info(f"Файл {path} успешно удалён.")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка удаления: {e}")
        return False