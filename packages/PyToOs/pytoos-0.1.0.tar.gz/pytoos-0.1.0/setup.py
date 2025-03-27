from setuptools import setup, find_packages
import pathlib

# Чтение README.md для long_description
current_dir = pathlib.Path(__file__).parent
long_description = (current_dir / "README.md").read_text(encoding="utf-8")

setup(
    name="PyToOs",
    version="0.1.0",  
    description="PyToOs - библиотека которая позволяет управлять .py файлами. Позволяет создавать, редактировать, удалять .py файлы",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="mistertayodimon",
    author_email="dimondimonych1@outlook.com",
    url="https://github.com/mistertay0dimon",
    license="MIT",
    
    # Автоматическое включение всех пакетов
    packages=find_packages(include=["pytoos", "pytoos.*"]),
    
    # Зависимости (если есть)
    install_requires=[],  
    
    # Минимальная версия Python
    python_requires=">=3.6",
    
    # Классификаторы для PyPI
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
     # Опционально: консольные скрипты
    entry_points={
        "console_scripts": [
            "pytoos=pytoos.cli:main",  # Если будет CLI-интерфейс
        ],
    },
    
    # Включение не-Python файлов (если есть)
    include_package_data=True,
)