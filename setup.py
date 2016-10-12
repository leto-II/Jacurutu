from setuptools import setup

setup(
        name='Jacarutu',
        version='0.1',
        url='https://github.com/dymurray/jacarutu',
        author='Dylan Murray',
        install_requires=[
            'project-free-tv',
            'pychromecast',
            'cast',
            'docopt',
            'beautifulsouyp4',
         ],
        entry_points={
            'console_scripts': [
                'jacarutu = jacarutu:main'
            ]
        },
)
