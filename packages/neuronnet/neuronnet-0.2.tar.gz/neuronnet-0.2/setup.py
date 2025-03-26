from setuptools import setup, find_packages

setup(
    name='neuronnet',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    description='Библиотека для коллективного обучения нейросетей',
    author='Umar',
    author_email='umarfrost2011@gmail.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/NeuronNet',
)
