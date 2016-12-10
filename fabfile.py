# encoding: utf-8

from fabric.api import local

def host_type():
    local('uname')


def prepare_deploy():
    local("./manage.py test ")
    local("git add -p && git commit")
    local("git push")
