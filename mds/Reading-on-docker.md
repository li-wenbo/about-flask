docker 是一种"虚拟化"技术。实际上，它只是融合了cgroup和union file system。


![docker-engine](https://docs.docker.com/engine/images/engine-components-flow.png)
![docker-architecture](https://docs.docker.com/engine/images/architecture.svg)

Container format
* Namespaces
* cgroup
* union file system

Dockerfile

* RUN         run command、commit the result if a write happens
* CMD         the defaults action when container runs as a executor, or supplies the args to ENTRYPOINT
* ENTRYPOINT  run when container runs as a executor