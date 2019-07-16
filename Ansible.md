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
    * https://github.com/li-wenbo/ansible-role-mysql-startup.git


    * ![](https://liwb-csdn.oss-cn-hangzhou.aliyuncs.com/ansible-usecase.png)


## ansible vars

* vars dirctory
* defaults dirctory
* group vars
* host vars
* command args



