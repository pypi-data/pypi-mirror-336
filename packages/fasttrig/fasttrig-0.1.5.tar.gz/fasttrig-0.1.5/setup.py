from setuptools import setup, find_packages

setup(
    name='fasttrig',
    version='0.1.5',
    description='Fast sine/cosine/tangent approximation using fourth degree polynomials',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Yinyin Xiang',
    author_email='realannaxiang@gmail.com',
    url='https://github.com/gnaixanna/fasttrig',
    packages=find_packages(),
    install_requires=['numpy'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)