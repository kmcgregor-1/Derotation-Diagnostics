from setuptools import setup
import py2app

APP = ['derotation_app.py']
OPTIONS = {
    'argv_emulation':True,
    'iconfile':'icon.icns'
}

setup(
    app = APP,
    options = {'py2app':OPTIONS},
    setup_requires=['py2app']
)
