from setuptools import setup, find_packages

setup(
    name='jackchendongtest',  # 写包的名字
    version='1.1.0',  # Start with a small number and increase it with every change you make
    license='MIT',  # 选择一个开源许可对应你刚才那个from here: https://help.github.com/articles/licensing-a-repository
    description='observa API',  # Give a short description about your library
    author='chendong',  # 填写作者名称
    author_email='chendong@qq.com',  # 填写email
    url='https://github.com',  # Provide either the link to your github or to your website
    packages=find_packages(),
    keywords=['API', 'AI', 'Python'],  # Keywords that define your package best
    install_requires=[  # 包的依赖
        'requests~=2.31.0',  # 可以加上版本号，如validators=1.5.1
        'langchain~=0.3.20',
        'langchain-core~=0.3.45',
    ],
    python_requires='>=3.9',
)
