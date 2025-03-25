from setuptools import setup, find_packages

setup(
    name="pixhawk-lib",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "dronekit>=2.9.2",
        "pymavlink>=2.4.40",
        "pyserial"
    ],
)