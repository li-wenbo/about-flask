## ansible overview

![ansible](https://liwb-csdn.oss-cn-hangzhou.aliyuncs.com/ansible.png)

## use case

* 使用ansible playbook 安装mysql
* 任务拆分 
    * 下载mysql 二进制包
    * 在目标机器解压包，安装db software
    * 初始化db
    * 启动db Server
    * 修改root密码
    * see my [git repo](https://github.com/li-wenbo/ansible-role-mysql-startup.git)
    * ![role-overview](https://liwb-csdn.oss-cn-hangzhou.aliyuncs.com/ansible-usecase.png)

## vars in playbook

* `vars` 指令
* `vars_files` 指令
* 内置变量
    * hostvars
    * inventory_name
    * group_names
    * groups
    * play_hosts
    
## vars in files

* group vars/host vars in inventory file or in group_vars/host_vars dir
* defaults/ dir  should be override
* vars/ dir      should not override


