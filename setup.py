from setuptools import setup

from lettherebe import __version__

setup(
    version=__version__,
    url="https://github.com/LetThereBe/lettherebe",
    name="lettherebe-web",
    description='LetThereBe web app',
    packages=['lettherebe-web'],
    install_requires=['lettherebe', 'flask', 'flask_wtf'],
    license='BSD',
    author="Mayeul d'Avezac, Ilektra Christidi, Alice Harpole, David Perez Suarez, Thomas Robitaille, Sinan Shi",
    author_email="thomas.robitaille@gmail.com",
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
    ],
)
