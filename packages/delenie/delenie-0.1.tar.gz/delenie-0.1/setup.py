from setuptools import setup, find_packages

setup(
     name='delenie',
     version='0.1',
     packages=find_packages(),
     description='The libriary',
     long_description=open('README.md').read(),
     long_description_content_type='text/markdown',
     author='Maria',
     author_email='mary.plohotskaya@gmail.com',
     url='https://github.com/maryplohotskaya/delenie',
     classifiers=[
           'Programming Language :: Python :: 3',
           'License :: OSI Approved :: MIT License',
           'Operating System :: OS Independent',
     ],
     python_requires='>=3.6',
)