import logging
from pathlib import Path
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pytoos")

def edit_py_file(
    file_path: str,
    new_content: str,
    line: Optional[int] = None,
    mode: str = "append"
) -> bool:
    """
    Редактирует существующий .py-файл.
    
    Args:
        file_path: Путь к файлу
        new_content: Новый код для вставки
        line: Номер строки (для mode='insert')
        mode: Режим ('append', 'prepend', 'insert', 'replace')
        
    Returns:
        bool: Успешно ли выполнено редактирование
        
    Examples:
        >>> edit_py_file("script.py", "x = 42", mode="prepend")
    """
    try:
        path = Path(file_path)
        if not path.exists():
            logger.error(f"Файл {path} не найден.")
            return False
            
        if path.suffix != ".py":
            logger.warning(f"Файл {path} не является .py-файлом.")
            
        with open(path, 'r+', encoding='utf-8') as f:
            lines = f.readlines()
            
            if mode == "insert" and line:
                if 0 < line <= len(lines):
                    lines.insert(line - 1, new_content + "\n")
                else:
                    logger.error(f"Недопустимый номер строки: {line}")
                    return False
                    
            elif mode == "prepend":
                lines.insert(0, new_content + "\n")
                
            elif mode == "replace":
                lines = [new_content + "\n"]
                
            else:  # append
                lines.append(new_content + "\n")
                
            f.seek(0)
            f.writelines(lines)
            
        logger.info(f"Файл {path} успешно отредактирован (режим: {mode}).")
        return True
        
    except Exception as e:
        logger.error(f"Ошибка редактирования: {e}")
        return False