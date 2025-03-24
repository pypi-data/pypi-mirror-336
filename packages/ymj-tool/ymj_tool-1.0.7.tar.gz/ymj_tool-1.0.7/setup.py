from setuptools import setup, find_packages

setup(
    name="ymj_tool",
    version="1.0.7",
    description="A useful tool for ...",  # 修改为你的描述
    author="ssseVennn",
    author_email="739369987@qq.com",
    packages=find_packages(),
    package_data={
        # 指定需要包含的运行时文件（根据实际情况调整）
        'pyarmor_runtime_000000': ['*.py', '*.pyd'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
