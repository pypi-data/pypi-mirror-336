import setuptools
import re
# import requests
# from bs4 import BeautifulSoup
import os
#package_name = "YJKAPI_TEST"
package_name = "YJKAPI"
 
def curr_version():
    # 方法1：通过文件临时存储版本号
    # with open('VERSION') as f:
    #     version_str = f.read()
    return "0.0.0.dev1"
    return version_str
    # # 方法2：从官网获取版本号
    # url = f"https://pypi.org/project/{package_name}/"
    # response = requests.get(url)
    # soup = BeautifulSoup(response.content, "html.parser")
    # latest_version = soup.select_one(".release__version").text.strip()
    # return str(latest_version)
 
def get_version():
    return "0.0.0.3"
 
# def get_version():
#     # 从版本号字符串中提取三个数字并将它们转换为整数类型
#     match = re.search(r"(\d+)\.(\d+)\.(\d+)", curr_version())
#     major = int(match.group(1))
#     minor = int(match.group(2))
#     patch = int(match.group(3))
 
#     # 对三个数字进行加一操作
#     patch += 1
#     if patch > 9:
#         patch = 0
#         minor += 1
#         if minor > 9:
#             minor = 0
#             major += 1
#     new_version_str = f"{major}.{minor}.{patch}"
#     return new_version_str
 
 
def upload():
    with open("README.md", "r") as fh:
        long_description = fh.read()
    # with open('requirements.txt') as f:
    #     required = f.read().splitlines()
    a=os.path.join('DLLs','**','*.*')
    setuptools.setup(
        name=package_name,
        version=get_version(),
        author="lme",  # 作者名称
        description="YJK_Python_API", # 库描述
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://gitee.com/yjk-opensource/yjkapi_-python/", # 库的官方地址
        packages=setuptools.find_packages(include=['YJKAPI', 'YJKAPI.*']),
        package_data={
            'YJKAPI': [os.path.join('DLLs', '**', '*.*'),'_APIData/__init__.pyi','_DataFuncApplication/__init__.pyi','_CsToYjk/__init__.pyi']
        },
        # data_files=["requirements.txt"], # yourtools库依赖的其他库
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.7',
        install_requires=["pythonnet"]
        #install_requires=["wheel","pyinstaller","python-dotenv","pythonnet==3.0.5"]
    )
 
 
def write_now_version():
    print("Current VERSION:", get_version())
    with open("VERSION", "w") as version_f:
        version_f.write(get_version())
 
 
def main():
    try:
        upload()
        print("Upload success , Current VERSION:", get_version())
    except Exception as e:
        raise Exception("Upload package error", e)
 
 
if __name__ == '__main__':
    main()