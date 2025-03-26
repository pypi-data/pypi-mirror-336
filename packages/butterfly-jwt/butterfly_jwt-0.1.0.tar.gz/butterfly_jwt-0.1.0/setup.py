from setuptools import setup, find_namespace_packages

setup(
    name='butterfly-jwt',
    version='0.1.0',
    description='A lightweight, pure Python JWT implementation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/butterfly-jwt',
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',
    keywords='jwt token authentication',
    extras_require={
        'test': [
            'pytest',
        ],
    },
)