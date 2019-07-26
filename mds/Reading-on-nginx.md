## How Nginx Works
* When master_process is on
    * ngx call *ngx_master_process_cycle* to loop
    * call ngx_start_worker_processes and ngx_spawn_process to span the worker processes
    * call ngx_worker_process_cycle in sub process
    * actually workers loop in **ngx_process_events_and_timers** called by ngx_worker_process_cycle
* When master_process is off
    * ngx call *ngx_single_process_cycle* to loop
    * directly call **ngx_process_events_and_timers**


![nginx-main-flow](https://liwb-csdn.oss-cn-hangzhou.aliyuncs.com/ngx-main-flow.jpg)

---
## How Nginx Manager the Processes
* ngx_pass_open_channel maintain the process
* ngx_processes stores the workers' infomation

---
## Everything in nginx is A module
* configure to make module list: ngx_modules.c
* modules is struct ngx_module_t
* modules init in ngx_init_cycle at main
```cmake
ngx_module_t *ngx_modules[] = {
    &ngx_core_module,
    &ngx_errlog_module,
    &ngx_conf_module,
    &ngx_regex_module,
    &ngx_events_module,
    &ngx_event_core_module,
    &ngx_kqueue_module,
    &ngx_http_module,
    &ngx_http_core_module,
    &ngx_http_log_module,
    &ngx_http_upstream_module,
    &ngx_http_static_module,
    &ngx_http_autoindex_module,
    &ngx_http_index_module,
    &ngx_http_mirror_module,
    &ngx_http_try_files_module,
    &ngx_http_auth_basic_module,
    &ngx_http_access_module,
    &ngx_http_limit_conn_module,
    &ngx_http_limit_req_module,
    &ngx_http_geo_module,
    &ngx_http_map_module,
    &ngx_http_split_clients_module,
    &ngx_http_referer_module,
    &ngx_http_rewrite_module,
    &ngx_http_proxy_module,
    &ngx_http_fastcgi_module,
    &ngx_http_uwsgi_module,
    &ngx_http_scgi_module,
    &ngx_http_memcached_module,
    &ngx_http_empty_gif_module,
    &ngx_http_browser_module,
    &ngx_http_upstream_hash_module,
    &ngx_http_upstream_ip_hash_module,
    &ngx_http_upstream_least_conn_module,
    &ngx_http_upstream_random_module,
    &ngx_http_upstream_keepalive_module,
    &ngx_http_upstream_zone_module,
    &ngx_http_write_filter_module,
    &ngx_http_header_filter_module,
    &ngx_http_chunked_filter_module,
    &ngx_http_range_header_filter_module,
    &ngx_http_gzip_filter_module,
    &ngx_http_postpone_filter_module,
    &ngx_http_ssi_filter_module,
    &ngx_http_charset_filter_module,
    &ngx_http_userid_filter_module,
    &ngx_http_headers_filter_module,
    &ngx_http_copy_filter_module,
    &ngx_http_range_body_filter_module,
    &ngx_http_not_modified_filter_module,
    NULL
};
```

---
## main
in main there are: cycle, init_cycle, ngx_cycle. search by: ```\b(init_|ngx_)?cycle\b```
ngx_cycle is global variable in nginx lifetime, using volatile modifier, and ngx_cycle would by modified by other process in nginx.

---
## module
* we can get every module information through the ngx_module_names in the ngx_modules.c, even before the main function. 
* in ngx_init_cycle, we just create_conf and init_conf the core module, by ```cycle->modules[i]->type != NGX_CORE_MODULE```


## module type in nginx
* NGX_CONF_MODULE
* NGX_CORE_MODULE
* NGX_EVENT_MODULE
* NGX_HTTP_MODULE
* NGX_MAIL_MODULE
* NGX_STREAM_MODULE


## how nginx dispatch the relate process when meet the module command

the command define below:

```cmake
struct ngx_command_s {
    ngx_str_t             name;
    ngx_uint_t            type;
    char               *(*set)(ngx_conf_t *cf, ngx_command_t *cmd, void *conf);
    ngx_uint_t            conf;
    ngx_uint_t            offset;
    void                 *post;
};
```


## ngx_core_module_t vs ngx_http_module_t vs ngx_event_s ...
* all modules share ngx_module_t, keeps its private data in the ctx field
* different type module has different type ctx, like ngx_core_module_t, ngx_http_module_t and etc
* cycle->conf_ctx stores all core modules ctx
* generally, create_conf allocate configuration struct memory


## when to call ngx_init_cycle
* in main func

## elts stands for elements        

## why log level is 4
* ngx_log_init in main set ```ngx_log.log_level = NGX_LOG_NOTICE;```
* ngx_log_open_default in ngx_init_cycle set ```log->log_level = NGX_LOG_ERR;```


## memory in nginx
* Allocates a block of memory from a pool. ```void *ngx_pnalloc(ngx_pool_t *pool, size_t size)```
* Similar to ngx_pnalloc() but allocates a block of memory from the pool aligned to NGX_ALIGNMENT. ```void *ngx_palloc(ngx_pool_t *pool, size_t size)```
* A wrapper for ngx_palloc() which also sets every byte of the allocation to 0. ```void *ngx_pcalloc(ngx_pool_t *pool, size_t size)```


## 我在豆瓣上写笔记
https://book.douban.com/people/3488235/annotation/22793675/


## event

when enter in worker process or single process

when conf finish and then init_process

ngx_add_event in ngx_event_process_init

at last ngx_process_events_and_timers


## someting on c

Static defined local variables do not lose their value between function calls. In other words they are global variables, but scoped to the local function they are defined in.
Static global variables are not visible outside of the C file they are defined in.
Static functions are not visible outside of the C file they are defined in.

In the C programming language, 
static is used with global variables and functions to set their scope to the containing file. 

In local variables, static is used to store the variable in **the statically allocated memory** instead of **the automatically allocated memory**. 
While the language does not dictate the implementation of either type of memory, 
statically allocated memory is typically reserved in data segment of the program at compile time, while the automatically allocated memory is normally implemented as a transient call stack.



## nginx architecture

![nginx architecture](https://liwb-csdn.oss-cn-hangzhou.aliyuncs.com/ngx-architecture.png)

---
# upstream 
* The ngx_http_upstream_module module is used to define groups of servers that can be referenced by the proxy_pass, fastcgi_pass, uwsgi_pass, scgi_pass, memcached_pass, and grpc_pass directives.
* traffic flow
    * u--> dns--> entry--> load balance--> apps
* apps so called upstream

---
# upstream checkers
* when to check
* what to check
* when a server fail
* when a server comeback


# ngx_http_realip_module
* set_real_ip_from
    - Defines trusted addresses that are known to send correct replacement addresses. 
* real_ip_header
    - Defines the request header field whose value will be used to replace the client address.
* real_ip_recursive
    - If recursive search is disabled, the original client address that matches one of the trusted addresses is replaced by the last address sent in the request header field defined by the real_ip_header directive. 
    - If recursive search is enabled,  the original client address that matches one of the trusted addresses is replaced by the last non-trusted address sent in the request header field.

---
# when ngx_http_realip_module works
```cmake
static ngx_int_t
ngx_http_realip_init(ngx_conf_t *cf)
{
    ...
    h = ngx_array_push(&cmcf->phases[NGX_HTTP_POST_READ_PHASE].handlers);
    if (h == NULL) {
        return NGX_ERROR;
    }

    *h = ngx_http_realip_handler;

    h = ngx_array_push(&cmcf->phases[NGX_HTTP_PREACCESS_PHASE].handlers);
    if (h == NULL) {
        return NGX_ERROR;
    }

    *h = ngx_http_realip_handler;

    ...
}
```

---
# what ngx_http_realip_module will do
```cmake
static ngx_int_t
ngx_http_realip_set_addr(ngx_http_request_t *r, ngx_addr_t *addr)
{
    size_t                  len;
    u_char                 *p;
    u_char                  text[NGX_SOCKADDR_STRLEN];
    ngx_connection_t       *c;
    ngx_pool_cleanup_t     *cln;
    ngx_http_realip_ctx_t  *ctx;

    cln = ngx_pool_cleanup_add(r->pool, sizeof(ngx_http_realip_ctx_t));
    if (cln == NULL) {
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }

    ctx = cln->data;

    c = r->connection;

    len = ngx_sock_ntop(addr->sockaddr, addr->socklen, text,
                        NGX_SOCKADDR_STRLEN, 0);
    if (len == 0) {
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }

    p = ngx_pnalloc(c->pool, len);
    if (p == NULL) {
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }

    ngx_memcpy(p, text, len);

    cln->handler = ngx_http_realip_cleanup;
    ngx_http_set_ctx(r, ctx, ngx_http_realip_module);

    ctx->connection = c;
    ctx->sockaddr = c->sockaddr;
    ctx->socklen = c->socklen;
    ctx->addr_text = c->addr_text;

    c->sockaddr = addr->sockaddr;
    c->socklen = addr->socklen;
    c->addr_text.len = len;
    c->addr_text.data = p;

    return NGX_DECLINED;
}
```


---
# 应用如何从request或者proxy上拿到client address
* 直连应用
    * 可以使用getpeeraddress 类API拿到socket另一端的信息
* 经过代理的应用
    * 代理结构复杂，应用难以获知真实的client，代理也只是能够获取client的大概范围，若存在header 欺骗，真实性更要打折扣
* ngx_http_realip_module 
    * 在 NGX_HTTP_PREACCESS_PHASE 之前修正remote_addr 
* note on client address
    * client address 并不能真正的表明真实的用户，如果作为用户的访问来源是具备一定的意义    
    
