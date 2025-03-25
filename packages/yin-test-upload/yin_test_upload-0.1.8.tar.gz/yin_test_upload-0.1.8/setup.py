from setuptools import setup, find_packages


setup(
    name='yin_test_upload',  # 你的包名
    version='0.1.8',  # 版本号
    description='脚本打包',  # 包的简要描述
    # long_description=long_description,  # 包的详细描述
    long_description_content_type='text/markdown',  # 描述文件的类型
    include_package_data=True,  # 包含包数据
    package_data={'yin_test_upload': ['*.py']},  # 指定数据文件
    author='yin',  # 作者姓名
    author_email='2018209921@qq.com',  # 作者邮箱
    packages=find_packages(),  # 自动查找包目录
    python_requires='>3.9',  # python版本要求
    install_requires=['setuptools', 'test'],  # 依赖库列表 (除开python自带的包外的其他依赖库(代码中如果缺少了对应的库会导致无法运行的包))
)
