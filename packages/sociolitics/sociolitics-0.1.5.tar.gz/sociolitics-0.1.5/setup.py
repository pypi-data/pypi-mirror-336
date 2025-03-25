from setuptools import setup, find_packages

setup(
    name="sociolitics",               # Имя вашей библиотеки (уникальное на PyPI)
    version="0.1.5",                 # Версия
    author="Dmitry Pronin",               # Автор
    author_email="DDPronin003@yandex.ru",# Email автора
    description="Sociolit project analysis tools", 
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="", # Ссылка на репозиторий
    packages=find_packages(),        # Автоматический поиск пакетов
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9.7',         # Минимальная версия Python
    install_requires=[

            "pandas>=2.0.2",
            "numpy>=1.21.6",
            "scipy>=1.9.1",
            "scikit-learn>=1.0.2",
            "plotly>=5.9.0",
            "matplotlib>=3.5.2",
            "seaborn>=0.13.0", 
            "joblib>=1.4.2",
            "pymystem3>=0.2.0"

],
)