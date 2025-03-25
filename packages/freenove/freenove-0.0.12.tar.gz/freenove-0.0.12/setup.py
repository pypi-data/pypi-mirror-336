from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# with open('requirements.txt', "r", encoding="utf-8") as f:
#     required = f.read().splitlines()

setup(
    name="freenove",                               # 包名
    version="0.0.12",                                 # 版本号
    author="syc",                                     # 作者
    author_email="1318270340@qq.com",                        # 邮箱
    description="freenove_config",                      # 简短描述
    long_description=long_description,               # 详细说明
    long_description_content_type="text/markdown",   # 详细说明使用标记类型
    python_requires=">=3.6",                         # 项目支持的Python版本
    # install_requires=required,                     # 项目必须的依赖
    include_package_data=False                       # 是否包含非Python文件（如资源文件）
)
