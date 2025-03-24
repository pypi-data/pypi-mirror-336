from setuptools import setup, find_packages

setup(
    name="ymj_tool",
    version="1.0.9",
    description="A useful tool for ...",  # 修改为你的描述
    author="ssseVennn",
    author_email="739369987@qq.com",
    packages=find_packages(),
    package_data={
        'ymj_tool': ['pyarmor_runtime_000000/*']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
