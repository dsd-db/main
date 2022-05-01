import os
import setuptools

r=lambda x:open(os.path.join(os.path.abspath(os.path.dirname(__file__)),x),'r').read()

setuptools.setup(
    name='db',
    version='0.0.5',
    description='Database - Happy Family.',
    py_modules=['db'],
    packages=setuptools.find_packages(),

    author='Xiangping DENG, Xiaoyang BAI',
    author_email='1484706725@qq.com',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    project_urls={
        "Source": "https://liyu.utad.pt/happy-family/main",
    },
    keywords='database db',
    python_requires='>=3.7',
)
