from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pytoos")

def create_py_file(
    file_path: str, 
    content: str = "", 
    overwrite: bool = False
) -> bool:
    """
    Создает Python-файл с указанным содержимым.
    
    Args:
        file_path: Путь к файлу (с или без .py)
        content: Содержимое файла
        overwrite: Перезаписать если файл существует
        
    Returns:
        bool: Успешно ли создан файл
        
    Examples:
        >>> create_py_file("example.py", "print('Hello')")
        True
    """
    try:
        path = Path(file_path).with_suffix(".py")
        
        if path.exists() and not overwrite:
            logger.warning(f"Файл {path} уже существует. Используйте overwrite=True.")
            return False
            
        path.write_text(content, encoding="utf-8")
        logger.info(f"Файл {path} успешно создан.")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при создании файла: {e}")
        return False