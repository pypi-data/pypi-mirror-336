import setuptools
from pathlib import Path

long_desc = Path("README.md").read_text("utf-8")
setuptools.setup(
    name="holamundoplayerfg",
    version="0.0.1",
    long_description=long_desc,
    packages=setuptools.find_packages(
        exclude=["mocks", "tests"]
    )
)


# Con este comando en la terminal, generamos la distribución que subiremos a Pypi
# Se crean las carpetas build y dist

# python setup.py sdist bdist_wheel


# Finalmente subimos el paquete a Pypi, ejecutando el siguiente comando
# pypi-AgEIcHlwaS5vcmcCJDFiZmY5YjBkLTUxMDEtNDQzZC1hMTk4LTM4NmIyNWRmYjZkMgACKlszLCJlYWNmYWNhMC01YjM2LTQ3ZmQtYjExYi05ZWU4ZTY5NjUzMTkiXQAABiBU42TUZWnUcIZyzRRyisCKLRqQIdd_9jtcmE17HRh0jg
