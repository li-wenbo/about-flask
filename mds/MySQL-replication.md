# Binary Log File Position Based Replication

Based on the master server keeping track of all changes to its databases (updates, deletes, and so on) in its binary log. 

## replication type

* asynchronous
  * semisynchronous
  * delayed replication
* GTI 

## replication format

* Statement-based replication
  * Replication of the master to the slave works by executing the SQL statements on the slave. 
* Row-based replication
  * Replication of the master to the slave works by copying the events representing the changes to the table rows to the slave. 
* Mixed-based replication

## how to works

* Each slave receives a copy of the entire contents of the binary log. 
* Binlog Dump thread on master for each replica, sending updates in <I>binary log</I>
* on slave
  * slave io thread connect and recevice updates, write the <I>relay log</I>
  * slave sql thread read relay log and execute sql on slave

## consensus protocol

set value -> uncommit -> commit -> consensus

* 2-pc
* paxos
* raft