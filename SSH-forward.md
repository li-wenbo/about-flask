# overview

ssh 端口转发可以理解，ssh 作为一种数据通道而存在。所谓的端口转发，就存在一个直接业务。

## local forward 

ssh -L [<localhost>]:<port>:<remote>:<port>  remote host

在ssh 客户端建立port，流量会通过ssh 会话到达ssh server，在ssh server，发起对remote:port 的连接。

## remote forward

ssh -R [<localhost>]:<port>:<remote>:<port>  remote host

在ssh 服务端建立port，流量会通过ssh 会话到达ssh client，在ssh client，发起remote:port的连接。

## how to choose  

如果业务的方向和ssh 会话方向相同，我们建立local forward，反之，建立remote forward。

## use case

* 加密非加密的cs应用流量
* 压缩cs应用流量 -C gzip