# encoding: utf-8

from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd, env, hosts, execute, roles
from fabric.contrib.console import confirm
#from fabric.contrib import django
#django.settings_module('material_web.settings')
#from  material.models import Material



# 定义主机 Hosts
'''
指定主机的格式字符串为: username@hostname:port

构造主机列表的方式:

    1. 全局指定主机列表的方式

        - 通过 env.host
            env.host=[host_string1, host_string2]

        - 通过 env.roles
            env.roledefs = {
               'role_name1': [host_string1, host_string2],
               'role_name2': [host_string1, host_string2],
               ...
            }

            env.roles = ['role_name1', 'role_name2']

        - 关于主机列表的设置可以在一个任务中进行设置， 然后在运行时将该任务放置在任何其他任务之前

        - 通过 命令行选项来指定 fabfile 文件所在的主机字符串
            fab -H host_string1, host_string2 task_name_list ...
            = 等价于 env.host=[host_string1, host_string2]

            该命令会在加载 fabfile 之前进行解释，因此 fabfile 文件中的任何相关配置
            都会重载命令行选项指定值。



    2. 按每个任务进行指定

        - 通过命令行为每个任务指定主机， 其方式如下(该方式会重载任何其他的主机列表以确保任务在特定的主机上运行)

            fab task_name:hosts="host_string1;host_string2,..."

        - 通过 装饰器(Decorator) 来为每个任务指定运行的主机

    主机列表指定的优先级顺序:
        1. 通过命令行选项为每个任务指定的主机列表
        2. 通过装饰器 hosts()为每个任务指定的主机列表
        3. 通过全局环境变量 env.host 指定的主机列表
        4. 通过命令行的全局主机列表选项 -H/--hosts 初始化的 env 变量


    不同主机列表指定方式的结合:
        1. 如果一个任务同时在 env.hosts 以及 hosts() 装饰器指定的主机列表结合时，通过 hosts()
        装饰器指定的主机列表会覆盖 env.hosts 设置，这是由它们的优先级确定的

        2. 对于每个任务，如果同时指定了 roles 和 hosts, 那么由二者指定的主机列表会被合并起来形成
        一个新的主机列表集合。

    主机列表去重:
        Fabric 为了支持 主机列表结合，默认情况下，Fabric 会对最终的主机列表进行去重这样就使得
        任何的主机字符串只会在主机列表中出现一次。 但是这阻止了故意在相同的主机上运行多次的行为，
        而这有时是非常有用的。

        为了关闭去重处理， 将 env.dedupe_hosts 设置为 False

    排除特定的主机列表:
        有时候，排除特定的一个或多个主机是非常有用的， 如重载几个差的或不想要的主机。
        在 1.4 中，可能会想要使用 skip_bad_hosts 选项替代。

        $> fab -R role_name -x/--exclude_hosts exclude_host_list
        $> fab taskname:roles=role_name,exclude_hosts="host1,host2,..."

    结合排除的主机列表:
        排除的主机列表不会将不同层级的主机列表合并起来。 如全局的 -x 选项不会影响一个由装饰器或关键字参数设置的
        任务特定的主机列表, 同时 单任务的 exclude_hosts 关键字参数也不会影响由全局 -H 指定的主机参数。

        但是有一个特例，命令行关键字参数(task_name:exclude_hosts=x,y)会考虑通过 @hosts/@roles 设置的主机列表。
        会考虑两者之间的差集

'''
MOTO_HOST = 'admin@192.168.0.11:50490'
THEO_HOST = 'theo@192.168.0.190:22'
DEV_HOST = 'liang@192.168.0.186:22'

# 避免重载在之前加载的关于主机的设置选项
env.hosts.extend([
    #     MOTO_HOST,
    THEO_HOST,
    DEV_HOST
])
# 定义角色 Roles
'''
1. 通过 env.roledefs 来定义相关的主机角色
2. 然后通过 env.roles 来指定在配置文件中所需要使用的角色

Roles 与 Host 具有可替代作用
'''

env.roledefs = {
    'dev': {
        'hosts': [DEV_HOST]
    },
    'product': {
        'hosts': [THEO_HOST]
    }
}

# 避免重载在之前加载的关于Roles的设置选项
env.roles.extend(['dev', 'product'])


# 通过装饰器来确保任务只在开发主机上 运行
@hosts(DEV_HOST)
def test_env_obj():
    #     with settings(host_string="liang@dev"):
    for (index, (key, value)) in enumerate(sorted(env.items())):
        print("{}: {} = {}".format(index, key, value))


@hosts(THEO_HOST)
def test_multi_host_taskA():
    run('ls')


@hosts(DEV_HOST)
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


@roles
def migrate():
    print("migrate database on db hosts")


#@hosts(DEV_HOST )
#def print_instance():
#    for instance in Material.objects.all():
#        print(instance)



if __name__ == '__main__':
    test_env_obj()
