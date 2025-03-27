from setuptools import setup, find_packages

setup(
    name="hush-p2p",
    version="2.0.5",
    author="MinakiLabs",
    author_email="support@minakilabs.com",
    description="🔐 Hush-P2P is a secure, encrypted peer-to-peer messaging system.",
    long_description="Secure, LAN and internet-capable peer-to-peer messaging and file transfer with automatic key exchange, UDP/TCP support, and no servers required.",
    long_description_content_type="text/markdown",
    url="https://github.com/MinakiLabs-Official/hush-p2p",
    project_urls={
        "Source": "https://github.com/MinakiLabs-Official/hush-p2p",
        "Bug Tracker": "https://github.com/MinakiLabs-Official/hush-p2p/issues",
    },
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "cryptography",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "hush=hush.cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Communications :: Chat",
        "Topic :: Security :: Cryptography",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: Other/Proprietary License",
    ],
    python_requires=">=3.7",
    license="Proprietary - Not Open Source",
)
