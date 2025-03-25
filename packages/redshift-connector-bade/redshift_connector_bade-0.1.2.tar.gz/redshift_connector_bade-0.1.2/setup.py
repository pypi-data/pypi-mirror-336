from setuptools import setup, find_packages

setup(
    name="redshift-connector-bade",           # 🔥 PyPI上的名字，建議用 - 符號
    version="0.1.2",                         # 🔥 升版本！不然PyPI不讓你上傳
    author="Hans, Roy",
    author_email="royhsu1012@hmail.com",
    description="A simple connector for Amazon Redshift using JDBC",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/royhsu1012/redshift_connector",
    packages=find_packages(),               # ✅ 抓 redshift_connector_bade 資料夾
    include_package_data=True,              # ✅ 如果你有 data / json 可用這個
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "jpype1",
        "jaydebeapi",
        "pandas",
        "requests",
    ],
    python_requires=">=3.6",
)
