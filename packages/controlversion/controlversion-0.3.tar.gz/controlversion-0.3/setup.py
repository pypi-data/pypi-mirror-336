from setuptools import setup,find_packages

readme = open("./README.md", "r")

version = '0.3'

setup(
    name='controlversion',
    packages=find_packages('src'),  # this must be the same as the name above
    package_dir={'': 'src'},
    version=version,
    description='Esta es la descripcion de mi paquete',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='David Flores',
    author_email='',
    # use the URL to the github repo
    url='https://github.com/BlackByted/ControlVersion',
    download_url='https://github.com/BlackByted/ControlVersion/tarball/0.1',
    keywords=['testing', 'logging', 'example'],
    classifiers=[ ],
    license='MIT',
    include_package_data=True,
    install_requires=[
        'GitPython==3.1.44',
        'python-gitlab==5.6.0'
    ]
)