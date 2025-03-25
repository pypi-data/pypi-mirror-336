from setuptools import setup, find_packages

setup(
    name='unifiedfinder',
    version='1.1.0',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'selenium',
        'requests'
    ],
    author='Trollparts',
    description='A unified scraping helper combining BeautifulSoup and Selenium utilities.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Trollparts/unifiedfinder',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)