# coding: utf-8

from fabkit import *  # noqa
from fablib.base import SimpleBase


class Etcd(SimpleBase):
    def __init__(self):
        self.data_key = 'etcd'
        self.data = {
            'etcd_cluster_nodes': [],
        }

        self.packages = {
            'CentOS .*': [
                'wget',
                'etcd',
            ]
        }

        self.services = {
            'CentOS .*': [
                'etcd',
            ]
        }

    def init_after(self):
        etcd_initial_cluster = []
        etcd_name = 'default'
        for i, node in enumerate(self.data['cluster_nodes']):
            if node == env.host:
                etcd_name = 'node{0}'.format(i)
            etcd_initial_cluster.append('node{0}=http://{1}:2380'.format(i, node))

        self.data.update({
            'etcd_name': etcd_name,
            'my_ip': env.node['ip']['default_dev']['ip'],
            'etcd_initial_cluster': ','.join(etcd_initial_cluster),
        })

    def setup(self):
        data = self.init()
        self.install_packages()

        sudo('setenforce 0')
        filer.Editor('/etc/selinux/config').s('SELINUX=enforcing', 'SELINUX=disable')

        Service('firewalld').stop().disable()

        if filer.template('/etc/etcd/etcd.conf', data=data):
            self.handlers['restart_etcd'] = True

        self.start_services().enable_services()
        self.exec_handlers()
