import setuptools,os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

template_dir = os.path.join('nonebot_plugin_animepush', 'templates')
if not os.path.exists(template_dir):
    raise FileNotFoundError(f"模板目录不存在: {template_dir}")

setuptools.setup(
    name="nonebot-plugin-animepush",
    version="0.0.3",
    author="huanxin996",
    author_email="mc.xiaolang@foxmail.com",
    description="将每日更新番剧渲染为图片",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/huanxin996/nonebot-plugin-animepush",
    packages=setuptools.find_packages(),
    package_data={
        'nonebot_plugin_animepush': ['templates/*.html'],
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=['nonebot-plugin-apscheduler<=0.5.0','nonebot_plugin_tortoise_orm<=0.1.4','nonebot_plugin_htmlrender<=0.6.2','nonebot_plugin_localstore<=0.7.3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)