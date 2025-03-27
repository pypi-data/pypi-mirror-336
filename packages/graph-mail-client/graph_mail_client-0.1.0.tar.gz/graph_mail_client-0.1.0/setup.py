"""
安装脚本
"""

from setuptools import setup, find_packages

setup(
    name="graph-mail-client",
    version="0.1.0",
    description="Microsoft Graph API 邮件客户端",
    author="Huaguang",
    author_email="2475096613@qq.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.25.0",
        "pyyaml>=5.4.0",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
