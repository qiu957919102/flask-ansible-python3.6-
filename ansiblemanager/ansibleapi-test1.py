#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 17:15
# @Author  : LiYuan_Zhang
# @Site    : 
# @File    : 
# @Software: PyCharm
import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase


class ResultCallback(CallbackBase):
    def __init__(self):
        self.x = dict()
        self.y = dict()
        self.z = dict()

    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        # 执行成功后的结果放到x字典中
        self.x[host.name] = result._result['stdout']

    def v2_runner_on_failed(self, result, ignore_errors=True):
        host = result._host
        # 执行后的结果放到x失y字典中
        self.y[host.name] = result._result['stderr_lines']

    def v2_runner_on_unreachable(self, result):
        host = result._host
        # 后的网络不结果放到x通z字典中
        self.z[host.name] = result._result['msg']


class AnsibleRunner:
    def __init__(self, remote_user='root', conn_pass='1234567 ', group='test01', module_name='shell', module_args='hostname'):
        # 在remote服务器上执行命令的用户
        self.remote_user = remote_user
        # 执行命令用户的密码
        self.conn_pass = conn_pass
        # 执行命令的主机，可以使group例如test01，也可以使列表例如['192.168.1.30']
        self.group = group
        # 执行的模块，例如shell,command,ping
        self.module_name = module_name
        # 命令，例如hostname,whoami
        self.module_args = module_args

    def order_run(self):
        Options = namedtuple('Options',['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user','remote_user', 'check', 'diff'])
        # initialize needed objects
        loader = DataLoader()
        options = Options(connection='smart', module_path=None, forks=100, become=None, become_method=None,become_user=None, remote_user=self.remote_user, check=False, diff=False)
        passwords = dict(vault_pass='secret', conn_pass=self.conn_pass)
        # Instantiate our ResultCallback for handling results as they come in
        results_callback = ResultCallback()

        # create inventory and pass to var manager
        inventory = InventoryManager(loader=loader, sources=['./hosts'])
        variable_manager = VariableManager(loader=loader, inventory=inventory)

        # create play with tasks
        play_source = dict(
            name="Ansible Play",
            hosts=self.group,
            gather_facts='no',
            tasks=[
                dict(action=dict(module=self.module_name, args=self.module_args), register='shell_out'),
                # dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
            ]
        )
        play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

        # actually run it
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                options=options,
                passwords=passwords,
                stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin
            )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
            # 这里可以再进一步改进的，实现实时的现实执行结果
            return [results_callback.x, results_callback.y, results_callback.z]
# a = AnsibleRunner(remote_user='liuxin', conn_pass='1234567', group='test01', module_name='shell', module_args='whoami')
# print(a.order_run())
