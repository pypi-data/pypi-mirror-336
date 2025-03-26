"""
使用Cython生成so文件,加快执行速度
1、安装python-dev和gcc
apt install python-dev gcc
2、安装Cython
pip install Cython
3、编辑dir_paths
4、执行python build_setup.py build_ext --inplace
5、在第四步成功的情况下执行
python build_setup.py
"""
import sys
import os
import shutil
from distutils.core import setup
from Cython.Build import cythonize
# 需要编译的目录
# anchor.py  edge.py  graph_base.py  graph.py  __init__.py  modcls  module.py  modules  node.py  pipegraph.py
dir_paths = [
    'PipeGraphPy/core',
    'PipeGraphPy/core/modcls',
    'PipeGraphPy/db/models.py',
]
files = []
for d in dir_paths:
    if str(d).endswith(".py"):
        files.append(d)
    else:
        for f in os.listdir(d):
            if not str(f).endswith("__init__.py") and str(f).endswith(".py"):
                files.append(d+"/"+f)

def del_file(py_file):
    # 判断so文件是否存在
    so_file = str(py_file)[:-3] + '.cpython-39-aarch64-linux-gnu.so'
    if not os.path.isfile(so_file):
        raise Exception(f"{so_file}不存在")

    # 删除c文件
    c_file = str(py_file)[:-3] + '.c'
    if not os.path.isfile(c_file):
        raise Exception(f"{c_file}不存在")
    else:
        os.remove(c_file)

    # 删除py文件
    if not os.path.isfile(py_file):
        raise Exception(f"{py_file}不存在")
    else:
        os.remove(py_file)

    # 删除pyc文件
    pyc_file = str(py_file)[:-3] + '.pyc'
    if os.path.isfile(pyc_file):
        os.remove(pyc_file)

    # 删除__pycache__
    py_file_split = str(py_file).split("/")
    if len(py_file_split) == 1:
        pycache = "__pycache__"
    else:
        pycache = "/".join(py_file_split[:-1] + ["__pycache__"])
    if os.path.isdir(pycache):
        shutil.rmtree(pycache)

# 参数包含build_ext 说明是编译
if  'build_ext' in sys.argv:
    # 编译生成so文件
    setup(ext_modules = cythonize(
        files,
        exclude=['__init__.py'],
        compiler_directives={'language_level': '3'})
    )
else:
    home_path = os.path.dirname(os.path.abspath(__file__))
    # 删除py和.c 文件
    for d in dir_paths:
        abs_path = os.path.join(home_path, d)
        if str(abs_path).endswith(".py") and not str(abs_path).endswith("__init__.py"):
            del_file(abs_path)
        else:
            for f in os.listdir(abs_path):
                if not str(f).endswith("__init__.py") and str(f).endswith(".py"):
                    del_file(os.path.join(abs_path, f))

