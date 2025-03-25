from setuptools import setup, Extension, find_packages

dummy_extension = Extension("ymj_tool._dummy", ["ymj_tool/dummy.c"])

setup(
    name="ymj_tool",
    version="1.0.11",
    description="A useful tool for ...",  # 修改为你的描述
    author="ssseVennn",
    author_email="739369987@qq.com",
    packages=find_packages(),
    ext_modules=[dummy_extension],
    package_data={
        'ymj_tool': ['pyarmor_runtime_000000/*']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
