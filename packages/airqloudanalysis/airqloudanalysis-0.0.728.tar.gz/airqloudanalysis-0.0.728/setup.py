from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.728'
DESCRIPTION = 'This is used for analyzing the obtain from IoT AirQo devices'
# LONG_DESCRIPTION = 'This uses data from IoT AirQo devices to analyze the data and provide insights like sensor health, device uptime, data completeness, etc.'

# Setting up
setup(
    name="airqloudanalysis",
    version=VERSION,
    author="AirQo",
    author_email="<gibson@airqo.net>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'requests', 'pytz', 'python-dateutil', 'beautifulsoup4', 'matplotlib', 'seaborn', 'plotly', 'cufflinks'],
    keywords=['python', 'IoT', 'AirQo', 'data', 'analysis', 'insights'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ]
)