
NFS是基于[UDP](https://baike.baidu.com/item/UDP/571511)/IP协议的应用，其实现主要是采用[远程过程调用](https://baike.baidu.com/item/远程过程调用)[RPC](https://baike.baidu.com/item/RPC/609861)机制，RPC提供了一组与机器、操作系统以及低层传送协议无关的存取远程文件的操作。[RPC](https://baike.baidu.com/item/RPC)采用了[XDR](https://baike.baidu.com/item/XDR)的支持。[XDR](https://baike.baidu.com/item/XDR/8796904)是一种与机器无关的数据描述编码的协议，他以独立与任意机器体系结构的格式对网上传送的数据进行编码和解码，支持在异构系统之间数据的传送。

NFS是Network File System的缩写，即网络文件系统。一种使用于分散式文件协定，功能是通过网络让不同的机器、不同的操作系统能够分享个人数据，让应用程序通过网络可以访问位于服务器磁盘中的数据。
NFS在文件传送或信息传送的过过程中，依赖于RPC协议。RPC，远程过程调用（Remote Procedure Call）,是使客户端能够执行其他系统中程序的一种机制。NFS本身是没有提供信息传输的协议和功能的，但NFS却能让我们通过网络进行资料的分享，就是因为NFS使用了RPC提供的传输协议，可以说NFS就是使用PRC的一个程序。

![img](asset/fa6903dc54c511ebba0cb05cdaef25a2)

# 简介

## NFS挂载原理

![在这里插入图片描述](asset/fcab4f3654c511eb8163b05cdaef25a2)

如上图示：

当我们在NFS服务器设置好一个共享目录/home/public后，其他的有权访问NFS服务器的NFS客户端就可以将这个目录挂载到自己文件系统的某个挂载点，这个挂载点可以自己定义，如上图客户端A与客户端B挂载的目录就不相同。并且挂载好后我们在本地能够看到服务端/home/public的所有数据。如果服务器端配置的客户端只读，那么客户端就只能够只读。如果配置读写，客户端就能够进行读写。挂载后，NFS客户端查看磁盘信息命令：

> df –h。

既然NFS是通过网络来进行服务器端和客户端之间的数据传输，那么两者之间要传输数据就要有想对应的网络端口，NFS服务器到底使用哪个端口来进行数据传输呢？基本上NFS这个服务器的端口开在2049,但由于文件系统非常复杂。因此NFS还有其他的程序去启动额外的端口，这些额外的用来传输数据的端口是随机选择的，是小于1024的端口；既然是随机的那么客户端又是如何知道NFS服务器端到底使用的是哪个端口呢？这时就需要通过远程过程调用（Remote Procedure Call,RPC）协议来实现了！

## RPC与NFS通讯原理

因为NFS支持的功能相当多，而不同的功能都会使用不同的程序来启动，每启动一个功能就会启用一些端口来传输数据，因此NFS的功能对应的端口并不固定，客户端要知道NFS服务器端的相关端口才能建立连接进行数据传输，而RPC就是用来统一管理NFS端口的服务，并且统一对外的端口是111，RPC会记录NFS端口的信息，如此我们就能够通过RPC实现服务端和客户端沟通端口信息。PRC最主要的功能就是指定每个NFS功能所对应的port number,并且通知客户端，记客户端可以连接到正常端口上去。

那么RPC又是如何知道每个NFS功能的端口呢？

首先当NFS启动后，就会随机的使用一些端口，然后NFS就会向RPC去注册这些端口，RPC就会记录下这些端口，并且RPC会开启111端口，等待客户端RPC的请求，如果客户端有请求，那么服务器端的RPC就会将之前记录的NFS端口信息告知客户端。如此客户端就会获取NFS服务器端的端口信息，就会以实际端口进行数据的传输了。

> 注意：在启动NFS SERVER之前，首先要启动RPC服务（即portmap服务，下同）否则NFS SERVER就无法向RPC服务区注册，另外，如果RPC服务重新启动，原来已经注册好的NFS端口数据就会全部丢失。因此此时RPC服务管理的NFS程序也要重新启动以重新向RPC注册。特别注意：一般修改NFS配置文档后，是不需要重启NFS的，直接在命令执行systemctl reload nfs或exportfs –rv即可使修改的/etc/exports生效

## NFS服务端

![img](asset/fec5cff854c511eba16bb05cdaef25a2)

## NFS客户端

![img](asset/004c29f654c611eb83a0b05cdaef25a2)

## NFS客户端和NFS服务器通讯过程

![在这里插入图片描述](asset/01d95b6254c611eb88dfb05cdaef25a2)

1. 首先服务器端启动RPC服务，并开启111端口

2. 服务器端启动NFS服务，并向RPC注册端口信息

3. 客户端启动RPC（portmap服务），向服务端的RPC(portmap)服务请求服务端的NFS端口

4. 服务端的RPC(portmap)服务反馈NFS端口信息给客户端。

5. 客户端通过获取的NFS端口来建立和服务端的NFS连接并进行数据的传输。

# 部署

## 服务端安装NFS服务步骤

**首先， 检查系统中是否安装 NFS 和 RPC ，并进行安装NFS 和RPC**

> [root@NFS ~]# rpm -qa nfs-utils rpcbind
>
> rpcbind-0.2.0-13.el6.x86_64
>
> nfs-utils-1.2.3-75.el6.x86_64

**第一步：安装NFS和rpc。**

> [root@localhost ~]# yum install -y  nfs-utils   
>
> #安装nfs服务
>
> [root@localhost ~]# yum install -y rpcbind
>
> #安装rpc服务

**第二步：启动服务和设置开启启动：**

注意：先启动rpc服务，再启动nfs服务。

> [root@localhost ~]# systemctl start rpcbind    #先启动rpc服务
>
> [root@localhost ~]# systemctl enable rpcbind   #设置开机启动
>
> [root@localhost ~]# systemctl start nfs-server nfs-secure-server    
>
> #启动nfs服务和nfs安全传输服务
>
> [root@localhost ~]# systemctl enable nfs-server nfs-secure-server
>
> [root@localhost /]# firewall-cmd --permanent --add-service=nfs
>
> success   #配置防火墙放行nfs服务
>
> [root@localhost /]# firewall-cmd  --reload 
>
> success

**第三步：配置共享文件目录，编辑配置文件：**

首先创建共享目录，然后在/etc/exports配置文件中编辑配置即可。

> [root@localhost /]# mkdir /public
>
> #创建public共享目录
>
> [root@localhost /]# vi /etc/exports
>
> ​	/public 192.168.245.0/24(ro)
>
> ​	/protected 192.168.245.0/24（rw）
>
> [root@localhost /]# systemctl reload nfs 
>
> #重新加载NFS服务，使配置文件生效

配置文件说明：

> 格式： `共享目录的路径 允许访问的NFS客户端（共享权限参数）`
>
> 如上，共享目录为/public , 允许访问的客户端为192.168.245.0/24网络用户，权限为只读。
>
> **请注意，NFS客户端地址与权限之间没有空格。**
>
> NFS输出保护需要用到kerberos加密（none，sys，krb5，krb5i，krb5p），格式sec=XXX
>
> none：以匿名身份访问，如果要允许写操作，要映射到nfsnobody用户，同时布尔值开关要打开，setsebool nfsd_anon_write 1
>
> sys：文件的访问是基于标准的文件访问，如果没有指定，默认就是sys， 信任任何发送过来用户名
>
> krb5：客户端必须提供标识，客户端的表示也必须是krb5，基于域环境的认证
>
> krb5i：在krb5的基础上做了加密的操作，对用户的密码做了加密，但是传输的数据没有加密
>
> krb5p：所有的数据都加密

用于配置NFS服务程序配置文件的参数：

| 参数           | 作用                                                         |
| -------------- | ------------------------------------------------------------ |
| ro             | 只读                                                         |
| rw             | 读写                                                         |
| root_squash    | 当NFS客户端以root管理员访问时，映射为NFS服务器的匿名用户     |
| no_root_squash | 当NFS客户端以root管理员访问时，映射为NFS服务器的root管理员   |
| all_squash     | 无论NFS客户端使用什么账户访问，均映射为NFS服务器的匿名用户   |
| sync           | 同时将数据写入到内存与硬盘中，保证不丢失数据                 |
| async          | 优先将数据保存到内存，然后再写入硬盘；这样效率更高，但可能会丢失数据 |

## NFS客户端挂载配置

**第一步：使用showmount命令查看nfs服务器共享信息。输出格式为“共享的目录名称 允许使用客户端地址”。**

> [root@localhost ~]# showmount -e 192.168.245.128    
>
> Export list for 192.168.245.128:
>
> /protected 192.168.245.0/24
>
> /public    192.168.245.0/24

showmount命令的用法；

| 参数 | 作用                                      |
| ---- | ----------------------------------------- |
| -e   | 显示NFS服务器的共享列表                   |
| -a   | 显示本机挂载的文件资源的情况NFS资源的情况 |
| -v   | 显示版本号                                |

**第二步，在客户端创建目录，并挂载共享目录。**

> [root@localhost ~]# mkdir /mnt/public
>
> [root@localhost ~]# mkdir /mnt/data
>
> [root@localhost ~]# vim /etc/fstab 
>
> #在该文件中挂载，使系统每次启动时都能自动挂载
>
> ​	192.168.245.128:/public  /mnt/public       nfs    defaults 0 0
>
> ​	192.168.245.128:/protected /mnt/data     nfs    defaults  0 1
>
> [root@localhost ~]# mount -a   #是文件/etc/fstab生效

**第三步：检查**

> [root@mail ~]# df -Th
>
> Filesystem                 Type      Size  Used Avail Use% Mounted on
>
> ...
>
> 192.168.245.128:/public    nfs4       17G  3.7G   14G  22% /mnt/public
>
> 192.168.245.128:/protected nfs4       17G  3.7G   14G  22% /mnt/data

## 在Window上挂载NFS

第一步：在控制面板–>添加程序和功能–>添加NFS组件。
![在这里插入图片描述](asset/05415b0a54c611eb969fb05cdaef25a2)

第二步：在此电脑，映射驱动器中添加nfs地址，和要共享的文件夹。

![在这里插入图片描述](asset/06f9187854c611ebbbcfb05cdaef25a2)

第三步：如果权限有问题，打开注册表：regedit, 在

> HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\ClientForNFS\CurrentVersion\Default 

下新建两个OWORD（64）位值，添加值AnonymousGid，值默认为0，AnonymousUid，值默认为0。



# 排错

## nfs server

1、检查是否安装

> [root@host ~]# rpm -qa |grep nfs     //查看是否安装了nfs
>
> nfs-utils-lib-1.0.8-7.6.el5
>
> nfs-utils-1.0.9-42.el5              //nfs主程序，已安装

2、NFS配置文件设置

若要共享目录或文件，需要在共享清单中指明该文件/etc/exports  (语法参照 man  exports)

> #vim   /etc/exports
>
> /home/nfs 192.168.2.0/24(rw,sync)    (192.168.2.0网段的用户对/home/nfs NFS卷具有读写)
>
> /media/cdrom 192.168.2.*(ro)        (192.168.2.0网段的用户对/media/cdromNFS卷具有读)

注：/etc/exports，配置文件有三部分： 输出目录，客户端，参数选项

- 输出目录是指NFS系统中需要共享给客户机使用的目录；


    客户端是指网络中可以访问这个NFS输出目录的计算机

- 客户端常用的指定方式


    指定ip地址的主机 192.168.0.200
    
    指定子网中的所有主机 192.168.0.0/24
    
    指定域名的主机 a.liusuping.com
    
    指定域中的所有主机 *.liusuping.com
    
    所有主机 *

- 选项：


    选项用来设置输出目录的访问权限、用户映射等。NFS主要有3类选项：
    
    访问权限选项
    
    设置输出目录只读 ro
    
    设置输出目录读写 rw

- 用户映射选项

  all_squash 将远程访问的所有普通用户及所属组都映射为匿名用户或用户组（nfsnobody）；

  no_all_squash 与all_squash取反（默认设置）；

  root_squash 将root用户及所属组都映射为匿名用户或用户组（默认设置）;

  no_root_squash 与rootsquash取反；

  anonuid=xxx 将远程访问的所有用户都映射为匿名用户，并指定该用户为本地用户（UID=xxx）；

  anongid=xxx 将远程访问的所有用户组都映射为匿名用 户组账户，并指定该匿名用户组账户为本地用户组账户（GID=xxx）；

- 其它选项


    secure 限制客户端只能从小于1024的tcp/ip端口连接nfs服务器（默认设置）；
    
    insecure 允许客户端从大于1024的tcp/ip端口连接服务器；
    
    sync 将数据同步写入内存缓冲区与磁盘中，效率低，但可以保证数据的一致性；
    
    async 将数据先保存在内存缓冲区中，必要时才写入磁盘；
    
    wdelay 检查是否有相关的写操作，如果有则将这些写操作 一起执行，这样可以提高效率（默认设置）；
    
    no_wdelay 若有写操作则立即执行，应与sync配合使用；
    
    subtree 若输出目录是一个子目录，则nfs服务器将检查其父目录的权限(默认设置)；
    
    no_subtree 即使输出目录是一个子目录,nfs服务器也不检查其父目录的权限,这样可以提高效率

3、启动nfs服务

> service nfs start
> 启动 NFS 服务：                                            [确定]
>
> 关掉 NFS 配额：                                            [确定]
>
> 启动 NFS 守护进程：                                        [确定]
>
> 启动 NFS mountd：                                          [确定]

4、查看自己的rpc进程，与NFS相关的是否正常开启，如下表明已经正常开启：
> #rpcinfo -p  192.168.2.1 (本机ip,)
>
> 100011    1   udp    821  rquotad 
>
> 100003    2   udp   2049  nfs
>
> 100021    1   tcp  34647  nlockmgr
>
> 100005    1   udp    852  mountd

5、导出共享清单

> [root@host ~]# exportfs -rv
>
> exporting 192.168.2.0/24:/home/nfs
>
> exporting 192.168.2.*:/media/cdrom

## nfs client

1、查看自己的rpc进程是否开启

> [root@client ~]# rpcinfo -p
>
> 程序 版本 协议   端口
>
> 100000    2   tcp    111  portmapper
>
> 100024    1   udp    794  status 
>
> 100021    1   udp  58859  nlockmgr


2、查看nsf-server的exports文件是否可以访问：

> [root@client ~]# showmount -e 192.168.2.1
>
> Export list for 192.168.2.1:
>
> /media/cdrom 192.168.2.*
>
> /home/nfs    192.168.2.0/24

3、创建挂载点，手动挂载

> #mkdir  /tmp/abc
>
> #mkdir  /tmp/cdrom
>
> mount 192.168.2.1:/home/nfs  /tmp/abc
>
> mount 192.168.2.1:/media/cdrom  /tmp/cdrom

4、设置开机自动挂载

> #vim /etc/fstab
>
> 192.168.2.1:/home/nfs   /tmp/abc                nfs     defaults,soft,intr      0 0
>
> 192.168.2.1:/media/cdrom   /tmp/cdrom           nfs     defaults,soft,intr      0 0

 注：（soft、intr等参数可查看man nfs）

 -ro,soft,intr:  -ro:挂载时的权限，soft:如果有I/O错误时，会告知系统，中继挂载；intr:挂载时有大量超时时，中继挂载，并告知系统。

> #umount /tmp/cdrom    /tmp/abc
>
> #mount -a

5、这种方式的挂载需要消耗大量的资源来维持连接，可以使用自动挂载当切换到该目录时进行挂载，退出时，取消挂载

a、安装autofs软件包

> [root@client tmp]# rpm -qa|grep autofs
>
> autofs-5.0.1-0.rc2.131.el5

b、编辑autofs的配置文件/etc/auto.master

> #vim /etc/auto.master
>
> /tmp /etc/nfs.misc   --timeout=08
>
> /tmp /etc/nfs.misc   --timeout=08

c、编辑要求的产生/etc/nfs.misc

> #vim /etc/nfs.misc
>
> abc     -fstype=nfs   192.168.2.1:/home/nfs
>
> cdrom   -fstype=nfs   192.168.2.1:/media/cdrom

d、启动autofs服务

> #service autofs  start
>
> #rm -rf /tmp/abc
>
> #rm -rf /tmp/cdrom

e、测试

注：abc、cdrom : 本地目录，我们不需要创建它，用于挂载远程共享文件192.168.2.1:/home/nfs，在我们想要使用远程共享文件/home/nfs时，只要在本地目录/tmp下键入cd abc 系统就会自动挂载到远程共享目录:192.168.2.10:/home/nfs,我们就可以正常使用里面的共享文件了 ，在到达超时时间时就会自动卸载。

f、以rw自动挂载/home/nfs/ NFS卷到/tmp/abc目录下，却发现无法创建目录，因为nfs-server的本地目录还没有写权限，

> [root@client abc]# touch nfs.txt
>
> touch: 无法触碰 “nfs.txt”: 权限不够

g、nfs-server服务端修改/home/nfs的本地权限

> [root@host home]# chmod o+wt nfs/

就可以正常创建了，

> [root@client abc]# touch nfs.txt
>
> [root@client abc]# dir
>
> hello-word.txt nfs.txt  nft-test

注：NFS客户端与NFS服务器在连接上之后，为了保证其正常的连接，NFS客户端与NFS服务器之间要不断的发送数据包，来宣告自己还在与NFS服务器进行着连接，但是，如果一个NFS服务器上有许多的客户端一直连接的话，NFS服务器会承受很大的带宽压力，这对NFS服务器的正常使用会造成很大的影响，因此，为了避免这种情况的发生，人们就想到了一种方法，让NFS客户端在获取数据时与NFS服务器进行连接，而在没有获取数据的时间内，自动的断开与NFS服务器之间的连接，但只要客户端发送获取数据的请求进，客户端就与服务器自动连接上，自动挂载的方法对客户端主机与服务器主机都有很大的好处。配置方法是在NFS客户端方面进行配置的



### umount nfs文件系统

> root@ubuntu:/# umount /app/nfs/
>
> umount.nfs: /app/nfs: device is busy
>
> umount.nfs: /app/nfs: device is busy

提示文件系统设置busy

> root@ubuntu:/# fuser -km /app/nfs/   先使用这条命令
> /data/nfs/:                     8119c
> root@ubuntu:/# umount /app/nfs/      在umount 就可以了
> root@ubuntu:/#

也可使用

> umount -f /app/nfs



## NFS常见故障解决方法

NFS服务出现了故障，主要从以下几个方面检查原因：

（1）检查NFS客户机和服务器的负荷是否太高，Server和Client之间的网络是否正常；

（2）检查/etc/exports文件的正确性；

（3）必要时重启NFS和portmap服务；

（4）运行下列命令重新启动portmap和NFS:

> /etc/init.d/portmap restart
>
> /etc/init.d/nfs restart
>
> /etc/init.d/rpcbind restart （在RHEL/CentOS 6.x里面）
>
> chkconfig portmap on
>
> chkconfig nfs on
>
> chkconfig rpcbind on （在RHEL/CentOS 6.x里面）

注意：在RHEL/CentOS 6.x里面，portmap服务改名为rpcbind服务了；顺便说一下，rpcbind服务也是图形界面的关键基础服务，不启动此服务，不能启动图形桌面。

（5） 检查Client上的mount命令或/etc/fstab的语法是否正确;

（6） 查看内核是否支持NFS和RPC服务。一般正常安装的Linux系统都会默认支持NFS和RPC服务，除非你自己重新编译的内核，而且没选择nfs支持选项编译。



1、The rpcbind failure error
故障现象：

> nfs mount: server1:: RPC: Rpcbind failure
> RPC: Timed Out
> nfs mount: retrying: /mntpoint

原因：
第一，可能因为客户机的hosts文件中存在错误的ip地址、主机名或节点名组合；
第二，服务器因为过载而暂时停止服务。

2、The server not responding error
现象：

> NFS server server2 not responding, still trying

原因：
第一，网络不通，用ping命令检测一下。
第二，服务器关机。

3、The NFS client fails a reboot error
现象：

> 启动客户机后停住了，不断显示如下提示信息：
> Setting default interface for multicast: add net 224.0.0.0: gateway:
> client_node_name.

原因：
在etc/vfstab的mount选项中使用了fg而又无法成功mount服务器上的资源，改成bg或将该行注释掉，直到服务器可用为止。

4、The service not responding error
现象：

> nfs mount: dbserver: NFS: Service not responding
> nfs mount: retrying: /mntpoint

原因：
第一，当前级别不是级别3，用who -r查看，用init 3切换。
第二，NFS Server守护进程不存在，用ps -ef | grep nfs检查，用/etc/init.d/nfs start启动。

5、The program not registered error
现象：

> nfs mount: dbserver: RPC: Program not registered
> nfs mount: retrying: /mntpoint

原因：
第一，当前级别不是级别3。
第二，mountd守护进程没有启动，用/etc/init.d/nfs脚本启动NFS守护进程。
第三，看/etc/dfs/dfstab中的条目是否正常。

6、The stale file handle error
现象：

> stale NFS file handle

原因：
服务器上的共享资源移动位置了，在客户端使用umount和mount重新挂接就可以了。

7、The unknown host error
现象：

> nfs mount: sserver1:: RPC: Unknown host 

原因：
hosts文件中的内容不正确。

8、The mount point error
现象：

> mount: mount-point /DS9 does not exist.

原因：
该挂接点在客户机上不存在，注意检查命令行或/etc/vfstab文件中相关条目的拼写。

9、The no such file error
现象：

> No such file or directory.

原因：
该挂接点在服务器上不存在，注意检查命令行或/etc/vfstab文件中相关条目的拼写。

10、No route to host
错误现象：

> mount 10.10.11.211:/opt/data/xmldb /c2c-web1/data/xmldb -t nfs -o rw
>
> mount: mount to NFS server ’10.10.11.211′ failed: System Error: No route to host.

原因：
防火墙被打开，关闭防火墙。
这个原因很多人都忽视了，如果开启了防火墙（包括iptables和硬件防火墙），NFS默认使用111端口，我们先要检测是否打开了这个端口，还要检查TCP_Wrappers的设定。

11、Not owner
现象：
> mount -t nfs -o rw 10.10.2.3:/mnt/c2c/data/resinfo2 /data/data/resinfo2
>
> nfs mount: mount: /data/data/resinfo2: Not owner

原因：
这是Solaris 10版本挂载较低版本nfs时报的错误。

解决：
需要用-o vers=3参数

示例：
> mount -F nfs -o vers=3 10.10.2.3:/mnt/c2c/data/resinfo2 /data/data/resinfo2

12、RPC: Program not registered & retrying
现象：

> nfs mount: 10.10.2.3: : RPC: Program not registered
> nfs mount: retrying: /data/data/resinfo2

原因：
没有启动NFS共享端服务。

解决：需要重新启动share端的NFS服务，

> Linux:
> mount: RPC: Program not registered
>
> /etc/init.d/nfs restart
>
> Solaris:
> mount: RPC: Program not registered
>
> /etc/rc.d/init.d/nfs restart



13、can’t contact portmapper: RPC: Remote system error – Connection refused
现象：
> exportfs -a
>
> can’t contact portmapper: RPC: Remote system error – Connection refused

原因：
出现这个错误信息是由于server端的portmap没有启动。

解决：

> /etc/init.d/portmap start

14、Cannot register service: RPC

> [root@IT_Only 20180815_std]# showmount -e nas09
> mount clntudp_create: RPC: Port mapper failure - RPC: Unable to receive

发现无法找到共享，决定在nas存储上重启nfs服务，报错如下

> Starting NFS quotas: Cannot register service: RPC: Unable to receive; errno = Connection refused rpc.rquotad: unable to register (RQUOTAPROG, RQUOTAVERS, udp).
>
> [service](https://www.centos.bz/tag/service/) nfs restart
>
> Shutting down NFS mountd: [ OK ]
>
> Shutting down NFS daemon: [ OK ]
>
> Shutting down NFS quotas: [ OK ]
>
> Shutting down NFS services: [ OK ]
>
> Starting NFS services: [ OK ]
>
> Starting NFS quotas: Cannot [register](https://www.centos.bz/tag/register/) service: RPC: Unable to receive; errno = Connection refused
>
> rpc.rquotad: unable to register (RQUOTAPROG, RQUOTAVERS, udp).
>
> [FAILED]

解决方法：

> service portmap start
>
> 先启动portmap才行
>

15、Address already in use

> tail -f /var/log/message
>
> Apr :: bogon nfsd[]: nfssvc: Setting version failed: errno (Device or resource busy)
>
> Apr :: bogon nfsd[]: nfssvc: unable to bind UPD [socket](https://www.centos.bz/tag/socket/): errno (Address already in use)
>
> Apr :: bogon nfsd[]: nfssvc: Setting version failed: errno (Device or resource busy)
>
> Apr :: bogon nfsd[]: nfssvc: unable to bind UPD socket: errno (Address already in use)
>
> Apr :: bogon nfsd[]: nfssvc: Setting version failed: errno (Device or resource busy)

解决方法：

> ps aux | grep nfs
>

然后用kill干掉这些进程

16、reason given by server: Permission denied

> mount: …:/nfsdata failed, reason given by server: Permission denied

解决方法：

> a.把该客户端的ip加入服务端的/etc/exports
>
> b.服务端的和客户端规则要统一，要么都使用主机名（注意每台机器的hosts文件），要么都使用IP
>

17、客户端挂载超时

> tail -f /var/log/message
>
> Apr :: localhost kernel: portmap: [server](https://www.centos.bz/tag/server/) localhost not responding, timed out
>
> Apr :: localhost kernel: RPC: failed to contact portmap (errno -).
>
> Apr :: localhost kernel: RPC: failed to contact portmap (errno -).
>
> Apr :: localhost kernel: lockd_up: makesock failed, [error](https://www.centos.bz/tag/error/)=-
>
> Apr :: localhost kernel: RPC: failed to contact portmap (errno -).

解决方法：

> service portmap restart
>
> service nfs restart
>

18、Error: RPC MTAB does not exist.

> service nfs start
>
> Starting NFS services: [ OK ]
>
> Starting NFS quotas: [ OK ]
>
> Starting NFS daemon: [ OK ]
>
> Starting NFS mountd: [ OK ]
>
> Starting RPC idmapd: Error: RPC MTAB does not exist.

解决方法：

手动执行

> mount -t rpc_pipefs sunrpc /var/lib/nfs/rpc_pipefs/

需要时加入开机启动时，加入下面两行到/etc/fstab

> rpc_pipefs /var/lib/nfs/rpc_pipefs rpc_pipefs defaults
>
> nfsd /proc/fs/nfsd nfsd defaults
>



# exportfs

exportfs主要用于管理当前NFS服务器的文件系统。

此命令的适用范围：RedHat、RHEL、Ubuntu、CentOS、Fedora。

## 参数列表

| 选项   | 说明                                                         |
| ------ | ------------------------------------------------------------ |
| **-a** | 共享nfs配置文件中所有的共享目录                              |
| **-i** | 忽略/etc/exports配置文件，只使用exportfs指令的默认值和命令行指定的参数 |
| **-r** | 重新共享所有的nfs文件系统                                    |
| **-u** | 取消一个或者多个NFS共享文件系统的共享                        |
| **-v** | 显示详细执行信息                                             |

> [root@localhost ~]# exportfs -u 192.168.1.7:/media/test

## 补充说明

- exportfs命令和nfs-utils这个包一起安装的
- 例子：
  - 假设在第一次配置nfs的共享目录，之后需要新增、更改某些机器或共享的目录；
  - 首先需要更改配置文件，然后重启NFS服务，但如果远程客户端正在使用NFS服务，正在挂载着，如果你需要先停止nfs服务，那远程的客户端就会挂起，就会很大的影响，造成服务异常，进程异常，有很大可能导致系统坏掉
- nfs服务不能随便重启，要重启，就需要先去服务器上，把挂载的目录卸载下来
  - 在卸载目录的时候，若是在当前目录下去卸载会提示umount.nfs4: /mnt: device is busy
    - 方法一：退出该目录后，再去卸载
    - 方法二：在目录下卸载的时候，加 -l 选项，表示 lazy 懒惰的意思
  - 在卸载目录后，在重启nfs服务
- 若是挂载了很多台机器，那么每台机器都需要去卸载，就会很麻烦，降低了工作效率
  - 方法：使用exportfs命令，重新加载下
- exportfs命令
  - -a 全部挂载或者全部卸载
  - -r 重新挂载
  - -u 卸载某一个目录
  - -v 显示共享目录

## 使用样例

- 在B机器客户端，卸载目录

> [root@test ~]# umount /mnt/

- 然后在A机器服务端，使用exportfs -arv命令，重新使配置文件生效

> [root@test~]# exportfs -arv
>
> exporting 192.168.202.0/24:/home/nfstestdir
>
> [root@test~]# 

- 在A机器上的/etc/exports配置文件中，在增加一行，把 /tmp 目录单独共享给192.168.202.131 这个IP

> [root@test~]# vim /etc/exports
>
> 在配置文件中加入
>
> /tmp 192.168.202.131(rw,sync,no_root_squash)
>
> 结果如下
>
> /home/nfstestdir  192.168.202.0/24(rw,sync,all_squash,anonuid=1000,anongid=1000)
>
> /tmp 192.168.202.131(rw,sync,no_root_squash)
>
> 保存退出

- 然后在A机器服务端执行exportfs -arv命令

> [root@test~]# exportfs -arv
>
> exporting 192.168.202.131:/tmp
>
> exporting 192.168.202.0/24:/home/nfstestdir

- 在B机器客户端showmount -e看是否生效——>并没有重启nfs服务，就已经生效

> [root@test ~]# showmount -e 192.168.202.130
>
> Export list for 192.168.202.130:
>
> /home/nfstestdir 192.168.202.0/24
>
> /tmp             192.168.202.131

- 在B机器客户端挂载，将 tmp目录 挂载到 mnt 目录下

> [root@test ~]# mount -t nfs 192.168.202.130:/tmp/ /mnt/
>
> [root@test ~]# df -h
>
> 文件系统              容量  已用  可用 已用% 挂载点
>
> 192.168.202.130:/tmp   18G  3.2G   15G   18% /mnt

这就是因为在A机器服务端的配置文件中，使用了no_root_squash ，所以root用户不受约束，在B机器上到挂载点下，到共享目录下，就可以像在本地磁盘使用root用户一样，是不受限制的（通常情况下，不限制root用户的比较多）