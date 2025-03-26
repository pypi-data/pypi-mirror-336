from setuptools import setup, find_packages

setup(
    name='neuronnet',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    description='Библиотека для коллективного обучения нейросетей с использованием оптимизатора Adam, L2-регуляризации и мини-пакетов.',
    author='Umar',
    author_email='umarfrost2011@gmail.com',
    long_description=open('README.md').read() + "\n\nОбновления:\n- Добавлен оптимизатор Adam.\n- Включена L2-регуляризация.\n- Реализована обработка данных в мини-пакетах.",
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/NeuronNet',
)
