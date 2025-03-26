from setuptools import setup, find_packages

setup(
    name='NeuronNet',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    description='Библиотека для коллективного обучения нейросетей',
    author='Твое Имя',
    author_email='your.email@example.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/NeuronNet',
)
