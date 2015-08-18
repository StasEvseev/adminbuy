#coding: utf-8

from fabric.api import local, sudo, lcd, put, cd
from fabric.context_managers import settings
from fabric.contrib.files import exists
from fabric.decorators import roles
from fabric.operations import local as lrun, run
from fabric.api import task

from fabric.state import env

import os

env.user = 'vagrant'

proj_dir = '/home/user/www'
root_folder = '/adminbuy'

local_config_dir = proj_dir + root_folder + '/config'
local_config_dir_super = local_config_dir + "/supervisor"

remote_nginx_dir = '/etc/nginx/sites-enabled'
remote_supervisor_dir = '/etc/supervisor/conf.d'

super_flikiss = "flikiss.conf"


remote_wiki_dir = '/home/www/wiki'
wiki_conf_file = '.flikissrc'


@task
def localhost():
    global proj_dir, local_config_dir, local_config_dir_super
    proj_dir = "/home/user/bitbucket"
    local_config_dir = proj_dir + root_folder + '/config'
    local_config_dir_super = local_config_dir + "/supervisor"
    env.run = lrun
    env.hosts = ['localhost']
    env.port = '22'
    env.user = 'user'

@task
def remote():
    env.run = run
    env.hosts = ['127.0.0.1']
    env.port = '2222'


@task
def deploy():
    create_user()
    with settings(user='user'):
        install_env()
        clone_proj()
        install_dependency()
        install_rabbitmq()
        install_redis()
        prepare_db()
        configure_nginx()
        configure_supervisor_proj()
        configure_supervisor_socket()
        configure_supervisor_celery()
        reload_nginx()
        reload_super()
        create_superuser()


@task
def update():
    with cd(proj_dir + root_folder):
        run('git pull origin master')
    migration()
    reload_super()
    reload_nginx()


@task
def migration():
    with cd(proj_dir + root_folder):
        run("python manage.py db upgrade")


@task
def prepare_db():
    with cd(proj_dir + root_folder):
        user = run('python -c "from config import USER; print USER"')
        password = run('python -c "from config import PASSWORD; print PASSWORD"')
        db = run('python -c "from config import DB; print DB"')

    run('sudo -u postgres psql -c "CREATE ROLE {0} WITH PASSWORD \'{1}\' NOSUPERUSER CREATEDB NOCREATEROLE LOGIN;"'.format(user, password))
    run('sudo -u postgres psql -c "CREATE DATABASE {0} WITH OWNER={1} TEMPLATE=template0 ENCODING=\'utf-8\';"'.format(db, user))

    migration()


@task
def clone_proj():
    run('mkdir ' + proj_dir + ' -p')
    with cd(proj_dir):
        run('git clone https://github.com/StasEvseev/adminbuy.git')

@task
def create_user():
    sudo('adduser user')
    sudo('gpasswd -a user sudo')

@task
def install_env():
    sudo('apt-get update')
    sudo('apt-get install -y python')
    sudo('apt-get install python-setuptools')
    sudo('easy_install pip')
    sudo('apt-get install -y python-virtualenv')
    sudo('apt-get install -y nginx')
    sudo('apt-get install -y gunicorn')
    sudo('apt-get install -y supervisor')
    sudo('apt-get install -y git')
    sudo('apt-get install libpq-dev python-dev -y')
    sudo('apt-get install postgresql-9.1 -y')


@task
def install_dependency():
    with cd(proj_dir + root_folder):
        sudo('pip install -r REQUIREMENTS')


@task
def create_superuser():
    with cd(proj_dir + root_folder):
        run('python manage.py create_superuser')

@task
def install_rabbitmq():
    try:
        sudo("dpkg -l | grep rabbitmq-server")
    except:
        sudo("echo 'deb http://www.rabbitmq.com/debian/ testing main' | tee -a /etc/apt/sources.list")
        sudo("wget https://www.rabbitmq.com/rabbitmq-signing-key-public.asc")
        sudo("apt-key add rabbitmq-signing-key-public.asc")
        sudo("apt-get update")
        sudo("apt-get install rabbitmq-server -y")
        sudo("rabbitmqctl add_user myuser mypassword")
        sudo("rabbitmqctl add_vhost myvhost")
        sudo("rabbitmqctl set_permissions -p myvhost myuser \".*\" \".*\" \".*\"")


@task
def install_redis():
    sudo("apt-get install redis-server -y")


@task
def configure_wiki():
    local("pip install flikiss")
    if os.path.exists(remote_wiki_dir + "/" + wiki_conf_file) is False:
        local("sudo mkdir %s -p" % remote_wiki_dir)
        local("sudo cp %s/%s %s/%s " % (
            local_config_dir, wiki_conf_file,
            remote_wiki_dir, wiki_conf_file))

    if os.path.exists(remote_supervisor_dir + "/" + super_flikiss) is False:
        local("sudo cp %s/%s %s/%s" % (
            local_config_dir_super, super_flikiss,
            remote_supervisor_dir, super_flikiss))


@task
def reload_nginx():
    sudo('/etc/init.d/nginx restart')


@task
def reload_super():
    try:
        sudo('service supervisor start')
    except:
        pass
    sudo('supervisorctl reread')
    sudo('supervisorctl reload')

@task
def configure_nginx():
    """
    """
    sudo('/etc/init.d/nginx start')
    if exists('/etc/nginx/sites-enabled/default'):
        sudo('rm /etc/nginx/sites-enabled/default')
    sudo('cp ' + local_config_dir + "/buyapi " + remote_nginx_dir + "/buyapi")

    if exists("/etc/nginx/sites-enabled/buyapi") is False:
        sudo('ln -s /etc/nginx/sites-available/buyapi' +
             ' /etc/nginx/sites-enabled/buyapi')


@task
def configure_supervisor_proj():
    """
    """
    if exists(remote_supervisor_dir + '/buyapi.conf') is False:
        sudo('cp ' + local_config_dir_super + '/buyapi.conf ' + remote_supervisor_dir + '/buyapi.conf')


@task
def configure_supervisor_socket():
    """
    """
    if exists(remote_supervisor_dir + '/socket.conf') is False:
        sudo('cp ' + local_config_dir_super + '/socket.conf ' + remote_supervisor_dir + '/socket.conf')


@task
def configure_supervisor_celery():
    if exists(remote_supervisor_dir + "/celery.conf") is False:
        sudo('cp ' + local_config_dir_super + '/celery.conf ' + remote_supervisor_dir + '/celery.conf')
        sudo('mkdir /var/log/celery')
    if exists(remote_supervisor_dir + "/celerybeats.conf") is False:
        sudo('cp ' + local_config_dir_super + '/celerybeats.conf ' + remote_supervisor_dir + '/celerybeats.conf')
        sudo('mkdir /var/log/celerybeats')