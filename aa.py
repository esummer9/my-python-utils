import os

PACKAGE_NAME = "myutils"

# 디렉토리 구조 생성
os.makedirs(f"{PACKAGE_NAME}/{PACKAGE_NAME}", exist_ok=True)

# __init__.py
with open(f"{PACKAGE_NAME}/{PACKAGE_NAME}/__init__.py", "w") as f:
    f.write("from .utils import my_function\n")

# utils.py
with open(f"{PACKAGE_NAME}/{PACKAGE_NAME}/utils.py", "w") as f:
    f.write('''def my_function():
    print("이것은 나만의 유틸 함수입니다.")\n''')

# setup.py
with open(f"{PACKAGE_NAME}/setup.py", "w") as f:
    f.write(f'''from setuptools import setup, find_packages

setup(
    name="{PACKAGE_NAME}",
    version="0.1.0",
    description="나만의 유틸리티 모음",
    author="이여름",
    author_email="your@email.com",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.7",
)
''')

# pyproject.toml
with open(f"{PACKAGE_NAME}/pyproject.toml", "w") as f:
    f.write('''[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
''')

# README.md (선택)
with open(f"{PACKAGE_NAME}/README.md", "w") as f:
    f.write("# myutils\n\n나만의 유틸 함수 모음입니다.\n")

print(f"✅ '{PACKAGE_NAME}' 패키지 구조가 생성되었습니다.")

