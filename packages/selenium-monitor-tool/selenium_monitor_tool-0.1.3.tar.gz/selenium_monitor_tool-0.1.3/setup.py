from setuptools import setup, find_packages

setup(
    name="selenium-monitor-tool",
    version="0.1.3",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "selenium>=4.0.0",
        "psutil>=5.8.0",
        "matplotlib>=3.5.0",
        "PyQt6>=6.4.0",
        "coverage>=6.0",
        "requests>=2.28.0"
    ],
    entry_points={
        "console_scripts": [
            "selenium-monitor=selenium_monitor_tool.front:main"  # Cambiado a front.py
        ],
    },
    description="Herramienta para monitorear pruebas Selenium con generación de reportes e IA",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Giulianna Bortone, Isabela Espinoza",
    author_email="giubortone@gmail.com",
    url="https://github.com/tu-usuario/selenium-monitor-tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)