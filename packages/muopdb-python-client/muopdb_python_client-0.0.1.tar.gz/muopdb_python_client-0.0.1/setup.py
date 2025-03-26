from setuptools import setup, find_packages

setup(
    name='muopdb-python-client',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'grpcio>=1.59.0',
        'grpcio-tools>=1.59.0',
        'protobuf>=4.25.1',
        'openai',
        'google-genai',
        'voyageai',
        'ollama',
        'dotenv',
        'sentence-transformers>=2.2.2',
        'transformers>=4.30.0',
        'torch>=2.0.0',
    ],
    author='Tech Care Coaching',
    author_email='info@techcarecoaching.com',
    description='A python package to connect with muopdb, an inhouse vector db',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/chauvm/muopdb_python_client',
    license="MIT",  # Corrected line
    python_requires='>=3.6',
)