# encoding: utf-8
from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd, env
from fabric.contrib.console import confirm


# 定义主机 Hosts
'''
指定主机的格式字符串为: username@hostname:port
'''
MOTO_HOST = 'admin@192.168.0.11:50490'
THEO_HOST = 'theo@192.168.0.190:22'
DEV_HOST = 'liang@192.168.0.186:22'

env.hosts = [
    #     MOTO_HOST,
    THEO_HOST,
    DEV_HOST
]

# 定义角色 Roles
'''
env.roledefs 是一个字典结构

    env.roledefs['dev']=[DEV_HOST,]
    env.roledefs['product'] = [THEO_HOST,]
'''
env.roledefs = {
    'dev': [DEV_HOST],
    'prodcut': [THEO_HOST]
}


def test_env_obj():
    #     with settings(host_string="liang@dev"):
    for (index, (key, value)) in enumerate(sorted(env.items())):
        print("{}: {} = {}".format(index, key, value))


def test_multi_host_taskA():
    run('ls')


def test_multi_host_taskB():
    run("whoami")

# 使用 fab 调用带参数的方法时，其语法为 funcname:para_value


def hello(name="world"):
    print("Hello %s!" % name)


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
    local('git push origin master')  # 在本地主机上运行上运行操作系统命令


def prepare_deploy():
    test()
    commit()
    push()


def deploy():
    code_dir = '~/projects/sys_util'

    with cd(code_dir):
        run('git pull')  # 运行操作系统中的命令, 需要指定主机进行连接
        run("ls")  # 运行操作系统中的命令, 需要指定主机进行连接

if __name__ == '__main__':
    test_env_obj()
