from setuptools import setup, find_packages

setup(
    name='ymj_tool',
    version='1.0.3',  # 再次改为新版本号，必须！
    description='ymj tool common utilities',
    author='ssseVennn',
    author_email='739369987@qq.com',
    packages=find_packages() + ['pyarmor_runtime_000000'],  # <-- 关键在这里，强制添加此包
    package_data={
        'pyarmor_runtime_000000': ['*.py', '*pyd'],  # 确保包含运行时.py文件
    },
    include_package_data=True,
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
