try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='pygex',
    version='0.2',
    packages=['pygex', 'pygex.gui'],
    url='https://github.com/teacondemns/pygex',
    install_requires=['Pillow>=9.0', 'pygame>=2.0'],
    license='MIT',
    author='Tea Condemns',
    author_email='tea.condemns@gmail.com',
    description='Extended library for pygame users.'
)
