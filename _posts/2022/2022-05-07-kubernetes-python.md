---
layout: post
title: Kubernetes python package
categories: [blog, python]
tags: [blog, python]
---

在项目中使用比较多的 [kubernetes](http://kubernetes.io)。主要使用相应的 python
[kubernetes](https://github.com/kubernetes-client/python) 库包来进行各种部署的管理。
国内很多讲解 kubernetes 原理，但是对于这个库各种使用看起来比较少。

+ toc
{:toc}

## Initialization

网上搜索得到比较多的是使用默认的 kubeconfig 来初始化。

```python
import os
from kubernetes import client, config

config.load_kube_config(os.path.expanduser("~/.kube/config"))

core_v1_api = client.CoreV1Api()
apps_v1 = client.AppsV1Api()
batch_v1_api = client.BatchV1Api()
networking_v1_api = client.NetworkingV1Api()
```

如果我们要管理多个集群，这种方式就不行。因为是使用了默认的 `api_client`。如何按需创建需要的
`api_client` 呢？


```python
import os
from kubernetes import client, config
from kubernetes.client import ApiClient, Configuration

config_file = os.path.expanduser("~/.kube/config")

client_configuration = Configuration()
config.load_kube_config(
    config_file=config_file,
    client_configuration=client_configuration,
)
api_client = ApiClient(configuration=client_configuration)
core_v1_api = client.CoreV1Api(api_client)
```

我们就可以用这段代码去初始化不同的 `api_client`，然后用 `client` 来获取对应的 `API` 操作对象。

## Deployments

**为了简化代码，后续所有的示例都采用默认的配置，而不是单独创建 `api_client` 的形式。**

创建一个 deployment，使用的是 `AppsV1Api.create_namespaced_deployment`

```python
apps_v1_api = client.AppsV1Api()
namespace = "test"
response = apps_v1_api.create_namespaced_deployment(body=yaml_content, namespace=namespace)
```

这里的`yaml_content` 是创建具体的 deployment 的内容。

> $$image$$ 请替换成真实的镜像名字

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    deployment.kubernetes.io/revision: '1'
  labels:
    app: my-awesome-deployment
spec:
  progressDeadlineSeconds: 600
  backoffLimit: 5
  replicas: 1
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app: my-awesome-deployment
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
    type: RollingUpdate
  template:
    metadata:
      labels:
        app: my-awesome-deployment
    spec:
      containers:
        - image: $$image$$
          imagePullPolicy: Always
          name: my-awesome-deployment
          ports:
            - containerPort: 8080
              protocol: TCP
          resources:
            requests:
              cpu: 1
              memory: 1Gi
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
```

Deployment 的其它接口

```python
# 不需要修改 replica
apps_v1_api.patch_namespaced_deployment(
     name, body=body, namespace=namespace
)

# 需要修改 replica
apps_v1_api.patch_namespaced_deployment_scale(
    name, body=body, namespace=namespace
)

apps_v1_api.read_namespaced_deployment(name, namespace=namespace)


apps_v1_api.delete_namespaced_deployment(name, namespace)
```

### 重启 deployment (patch_xxx)

重启实际上是需要增加一个新的 annotations

```python
import datetime
import pytz

# deployment 就是加载进来的 yaml_content

deployment["spec"]["template"]["metadata"]["annotations"] = {
    "kubectl.kubernetes.io/restartedAt": datetime.datetime.utcnow()
    .replace(tzinfo=pytz.UTC)
    .isoformat()
}
```

## Service and ingress

### Service

Service 使用的是 `CoreV1Api`

```python
core_v1_api = client.CoreV1Api()
core_v1_api.create_namespaced_service(body=yaml_content, namespace=namespace)
core_v1_api.delete_namespaced_service(name, namespace)
```

`yaml_content` 内容如下：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: $$service_name$$
spec:
  ports:
    - port: $$service_port$$
      targetPort: $$target_port$$
      protocol: TCP
  selector:
    app: $$target_name$$
  sessionAffinity: None
  type: $$service_type$$
```

注意填充上上述对应 `$$$$` 中的内容。其中要注意的是 `selector` 是和
deployment 中对应配置是对上的。`spec.template.metadata` 中的 `labels`。

### Ingress

Ingress 使用的 `NetworkingV1Api`

```python
networking_v1_api = client.NetworkingV1Api()
core_v1_api.create_namespaced_ingress(body=yaml_content, namespace=namespace)
networking_v1_api.delete_namespaced_ingress(name, namespace)
```

`yaml_content` 如下：

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress-name
spec:
  rules:
  - host: my-host
    http:
      paths:
      - backend:
          service:
            name: my-service-name
            port:
              number: my-service-port
        path: my-path
        pathType: Prefix  # Exact
```

上述所有 `my-` 开头都希望用户自己填充实际的。其中 `my-service-name` 和创建的 `service` 名称对应上。

## Job

Job 使用的是 `BatchV1Api`

```python
batch_v1_api = client.BatchV1Api()
batch_v1_api.create_namespaced_job(body=yaml_content, namespace=namespace)
batch_v1_api.read_namespaced_job(name, namespace)
batch_v1_api.delete_namespaced_job(name, namespace)
```

`yaml_content` 内容如下：

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  labels:
    app: $$ name $$
  name: $$ name $$
spec:
  ttlSecondsAfterFinished: 3600
  template:
    metadata:
      labels:
        app: $$ name $$
    spec:
      containers:
      - name: $$ name $$
        image: $$ image $$
        resources:
          requests:
            cpu: 1
            memory: 2Gi
        command: $$ command|safe $$
      restartPolicy: Never
  backoffLimit: 0
```

请自行填充 `$$ $$` 中的内容。

## Logs and Events

查看 POD 的日志和事件时，一般需要先知道有哪些 POD，然后遍历这些 POD 来获取对应的内容。

```python
core_v1_api = client.CoreV1Api()
# 使用具体的 label_selector 来选择相应的 POD
all_pods = core_v1_api.list_namespaced_pod(namespace=namespace, label_selector="app=my-awesome-deployment")

# all_pods 有个接口 `to_dict()`，可以把它打印出来，然后看怎么找到 POD name
dict_response = all_pods.to_dict()
pod_names = [item["metadata"]["name"] for item in dict_response["items"]]
```

### Log

```python
core_v1_api = client.CoreV1Api()
namespace = "test"
response = core_v1_api.read_namespaced_pod_log(
    name=name, namespace=namespace, tail_lines=100
)
```

### event

```python
core_v1_api = client.CoreV1Api()
namespace = "test"
pod_name = "zhangsan"
core_v1_api.list_namespaced_event(
    namespace=namespace,
    pretty=True,
    field_selector=f"involvedObject.name={pod_name}"
)
```

## 其它

+ Api 对应的函数有个 `async_req=True` 入参，可以发起异步调用，`response.get()` 拿到结果
+ 结果一般会有一个 `to_dict` 函数，可以通过打印这个结果来判断怎么去提取对应的信息
+ 建议 **yaml** + **jinja2** 来进行模板配置和模板的渲染，这样可以方便生成想要的 `yaml_content`

## Reference

+ [Kubernetes](http://kubernetes.io)
