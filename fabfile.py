# encoding: utf-8
from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd
from fabric.contrib.console import confirm

# fabric 可以运行 fabfile.py 中定义的任意函数

# 使用 fab 调用带参数的方法时，其语法为 funcname:para_value
def hello(name="world"):
    print("Hello %s!" %name)

def host_type():
    local('uname')

def test():
    with settings(warn_only=True):
        result = local("./manage.py test", capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Abort at user request.")        

def commit():
    local("git add -A && git commit -m 'fabric commit'")

def push():
    local('git push origin master') # 在本地主机上运行上运行操作系统命令

def prepare_deploy():
    test()
    commit()
    push()

def deploy():
    code_dir = '~/projects/sys_util'

    with cd(code_dir):
        run('git pull') # 运行操作系统中的命令, 需要指定主机进行连接
        run("ls") # 运行操作系统中的命令, 需要指定主机进行连接
