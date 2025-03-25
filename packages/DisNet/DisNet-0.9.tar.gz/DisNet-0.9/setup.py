from setuptools import setup, find_packages

setup(
    name="DisNet",
    author="WallCompany",
    version="0.9",
    packages=find_packages(),  # Нахождение всех пакетов в проекте
    install_requires=["discord"],  # Зависимости
    description="A Discord bot package",  # Описание
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Лицензия
        "Operating System :: OS Independent",
    ],
)
