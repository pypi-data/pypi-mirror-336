from setuptools import find_packages, setup

setup(
    name="dm-touka-utils",
    version="0.0.0",
    packages=find_packages(),
    author="Daiki Morita",
    description="自作のユーティリティ関数集",
    url="https://github.com/DaikiMorita/dm_utils",
    install_requires=["pandas", "rich"],
    python_requires=">=3.10",
)
