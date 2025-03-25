from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
]

setup(
    name='InfinityMath',
    version='0.0.2',
    description='The math module where you can sum numbers, make functions and other things',
    long_description=(open('README.md').read() if 'README.md' else '') + '\n\n' + (open('CHANGELOG.md').read() if 'CHANGELOG.md' else ''),
    long_description_content_type='text/markdown',
    url='https://github.com/SlackBaker/better_math.git',
    author='Ostap Dziubyk',
    author_email='your-email@example.com',
    license='MIT',
    classifiers=classifiers,
    keywords='math, better_math, calculations, InfinityMath, XMath',
    packages=find_packages(),
    install_requires=['numpy', 'scipy', 'matplotlib', 'cmath'],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'infinitymath=infinitymath.cli:main',
            'infinitymath-version=infinitymath:show_version',
        ],
    },
)
