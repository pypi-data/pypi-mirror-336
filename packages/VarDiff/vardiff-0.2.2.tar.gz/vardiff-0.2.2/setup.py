from setuptools import setup, find_packages

setup(
    name='VarDiff',
    version='0.2.2',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[],
    description='A Python package for comparing variables and files.',
    author='QTI',
    author_email='kohanmathersmcgonnell@gmail.com',
    license='MIT',
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
