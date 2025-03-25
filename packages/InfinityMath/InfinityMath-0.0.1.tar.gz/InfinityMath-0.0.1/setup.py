from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',  # Краще використовувати стандартну ліцензію
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
]

setup(
    name='InfinityMath',
    version='0.0.1',
    description='Basic math module',
    long_description=(open('README.md').read() if 'README.md' else '') + '\n\n' + (open('CHANGELOG.md').read() if 'CHANGELOG.md' else ''),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/better_math',  # Замініть на реальне посилання
    author='Ostap Dziubyk',
    author_email='your-email@example.com',  # Додай свою пошту або прибери цей параметр
    license='MIT',  # Використай стандартну ліцензію
    classifiers=classifiers,
    keywords='math, better_math, calculations',
    packages=find_packages(),
    install_requires=['numpy', 'scipy', 'matplotlib'],  # Додано залежності
    python_requires='>=3.6',  # Вказано мінімальну версію Python
)