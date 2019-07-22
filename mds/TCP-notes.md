## TCP State transform flow

![tcp-state](https://liwb-csdn.oss-cn-hangzhou.aliyuncs.com/tcp-state-flow.png)

在这个迁跃图里，需要注意的其中一点是，这里并没有具体客户端和服务端之分。客户端上也可能存在大量的close_wait，服务端也可能存在大量的time_wait，取决于，主动关闭链接的是谁。


## tcp socket programming

![tcp-socket](https://liwb-csdn.oss-cn-hangzhou.aliyuncs.com/tcp-socket-api.png)


## tcp connection queue

![tcp-queue](https://liwb-csdn.oss-cn-hangzhou.aliyuncs.com/tcp-queue.png)


在linux内核里，对tcp，维护了两个队列：

* incomplete connection
  * min(net.core.somaxconn, backlog)

* complete connection
  * max(64, net.ipv4.tcp_max_syn_backlog) when syncookies is disabled

