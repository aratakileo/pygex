try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

PACKAGE_NAME = PACKAGE_ROOT = 'pygex'
PACKAGE_VER = open(f'{PACKAGE_ROOT}/core/info.py').read().split('\n')[0].split(' = ')[-1][1:-1]

packages = [PACKAGE_ROOT]
package_data = {
    PACKAGE_ROOT: ['resource/*/*']
}


def add_package(package_name: str):
    packages.append(PACKAGE_ROOT + '.' + package_name)
    package_data[PACKAGE_ROOT].append(package_name.replace('.', '/') + '/*.pyi')


add_package('gui')
add_package('gui.drawable')
add_package('core')


setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VER,
    packages=packages,
    package_data=package_data,
    url=f'https://github.com/teacondemns/{PACKAGE_NAME}',
    install_requires=['pygame-ce>=2.2.1'],
    license='MIT',
    author='Tea Condemns',
    author_email='tea.condemns@gmail.com',
    description='An extensive module of various tools and tools for creating a modern graphical interface '
                'for pygame-ce users.'
)
