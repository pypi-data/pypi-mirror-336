import setuptools
import re
# import requests
# from bs4 import BeautifulSoup
import os
#package_name = "YJKAPI_TEST"
package_name = "YJKAPI"
 
def get_version():
    # with open('VERSION') as f:
    #     version_str = f.read()
    # return version_str
    return "0.0.0.9"

def update_version():
    with open('VERSION') as f:
        version_str = f.read()
        paras=version_str.split(".")
        paras[-1]=str(int(paras[-1])+1)
    new_version = ".".join(paras)
    with open('VERSION','w') as f :
        f.write(new_version+'\n')
 
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
            'YJKAPI': [os.path.join('DLLs', '**', '*.*'),'_APIData/__init__.pyi','_DataFuncApplication/__init__.pyi','_CsToYjk/__init__.pyi','_MiddleTrans/__init__.pyi','_Base/__init__.pyi','_YJKIPC/__init__.pyi']
        },
        #data_files=["VERSION"], #把同级目录下的VERSION文件上传
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.7',
        install_requires=["pythonnet"]
        #install_requires=["wheel","pyinstaller","python-dotenv","pythonnet==3.0.5"]
    )
 
def main():
    try:
        #update_version()
        upload()
        print("Upload success , Current VERSION:", get_version())

    except Exception as e:
        raise Exception("Upload package error", e)
 
 
if __name__ == '__main__':
    main()