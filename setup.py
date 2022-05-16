from setuptools import find_packages, setup

setup(
    name='akithon',
    url='https://github.com/south1907/akithon',
    author='Heva',
    author_email='namph.soict@gmail.com',
    python_requires='>=3.7',
    version='0.1.1',
    license='MIT',
    description='Akinator client package python',
    packages=find_packages(exclude=[
        'akithon_*', 'tests*'
    ]),
    keywords='akinator api client library package chatbot magic'
)
