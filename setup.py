# setup.py

from setuptools import setup, find_packages

setup(
    name='myutils',
    version='0.1.0',
    description='나만의 유틸리티 모음',
    author='이여름',
    author_email='esummer.lee@email.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'selenium',
        'requests',
        'beautifulsoup4',
        'slugify',
    ],  # 의존 패키지 있으면 여기에 추가
    python_requires='>=3.7',
)