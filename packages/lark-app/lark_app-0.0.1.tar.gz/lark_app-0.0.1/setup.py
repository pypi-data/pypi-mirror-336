from setuptools import setup, find_packages

setup(
    name='Lark-App',
    version='0.0.1',
    description='Lark Messanger tool for Python',
    author='wontae.jeon',
    author_email='wontae@aidenlab.io',
    install_requires=['requests'],
    packages=find_packages(exclude=[]),
    keywords=['lark', 'incode8'],
    python_requires='>=3.8',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
