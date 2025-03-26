from setuptools import setup, find_packages

setup(
    name='anf',
    version='1.0.0',
    description='Layout tasks with async and flower',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
    ],
    keywords='async flower task job',
    url='https://github.com/LL-Ling/anf.git',
    author='LL-Ling',
    author_email='1309399041@qq.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    include_package_data=False,
    zip_safe=False
)
