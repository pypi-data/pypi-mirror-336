import setuptools

with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="wjj", # 模块名称
    version = "0.1.4", # 当前版本
    author="JJWang", # 作者
    author_email="jj.wang2@siat.ac.cn", # 作者邮箱
    description="常用函数集成", # 简短介绍
    long_description=long_description, # 模块详细介绍
    long_description_content_type="text/markdown", # 模块详细介绍格式
    packages=setuptools.find_packages(), # 自动找到项目中导入的模块
    # 模块相关的元数据(更多描述信息)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
)



