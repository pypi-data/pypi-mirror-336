from setuptools import setup

setup(
    name='llm-flexquant',
    version='0.0.1',
    description='a python library that lets you quantize any layer your llm',
    url='https://github.com/vlgiitr/llm-flexquant',
    author='VLG',
    author_email='vlg.acm@iitr.ac.in',
    license='Apache-2.0',
    packages=['llm-flexquant'],
    install_requires=[
        'torch>=2.0.0',
        'transformers>=4.36.0',
        'datasets>=2.15.0',
        'numpy>=1.24.0',
        'tqdm>=4.65.0',
        'accelerate>=0.26.0',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
    ],
)