---
layout: post
title: Tensorflow save and restore A tutorial
categories: [blog, tensorflow]
tags: [tensorflow]
---

+ toc
{:toc}

### Introduction

一个正常的 Tensorflow 的 Pipeline 大概如下:

![image.png](/images/tensorflow/save-and-restore/1597653804065-3b86deae-b3bd-411a-8c5a-0bff185abf8b.png)

Save 和 Restore 可以在多个阶段同时或者单独发生。

- Training 阶段：模型可以基于某个基线进行恢复继续训练
- Training 阶段：为了保证出错时可以继续训练，在训练同时会有一些间隔来保存 checkpoint
- Evaluating：
   - 如果直接将训练停止，Evaluating 可以直接在内存中直接做 evaluate，而不用去 restore 模型
   - estimator 单独的 evaluator，需要 restore 模型
   - 导出时：可以导出成 checkpoint 格式或者 saved model 格式

现在主要有两种格式：Checkpoint 格式和 SavedModel 格式

### Show me the code

#### Checkpoint 格式

```python
import tensorflow as tf

## Save

var = tf.Variable(3)
sess = tf.Session()

sess.run(tf.global_variables_initializer())

saver = tf.train.Saver()
saver.save(sess, "./checkpoint/my-ckpt")

## Restore

with tf.Session(graph=tf.Graph()) as sess:
    var = tf.Variable(-1)
    sess.run(tf.global_variables_initializer())

    saver = tf.train.Saver()
    saver.restore(sess, "./checkpoint/my-ckpt")
    print(sess.run(var))


```

保存出：ckpt.py

![image.png](/images/tensorflow/save-and-restore/1597656096995-ae2e40fe-379a-4e65-8f17-26726181713a.png)

具体文件内容暂时忽略。

#### SavedModel

**注意每次导出时需要确保导出路径是空的，否则会报错。**

```python
import subprocess

import tensorflow as tf
from tensorflow.python.saved_model.builder import SavedModelBuilder
from tensorflow.python.saved_model import tag_constants

var = tf.Variable(3, name="he")
sess = tf.Session()

sess.run(tf.global_variables_initializer())
path = "./saved_model"
subprocess.check_call("command rm -rf {}".format(path), shell=True)

builder = SavedModelBuilder(path)
builder.add_meta_graph_and_variables(sess, tags=[tag_constants.SERVING])
# builder.add_meta_graph() 可以增加其它 tag 对应的 graph
builder.save()

with tf.Session(graph=tf.Graph()) as sess:
    tf.saved_model.loader.load(sess, [tag_constants.SERVING], path)
    graph = tf.get_default_graph()
    print(sess.run(graph.get_tensor_by_name("he:0")))
```

![image.png](/images/tensorflow/save-and-restore/1597656981066-5ef12719-359f-40bf-bb75-666b923de8a2.png)

使用 SavedModel 保存时实际上我们需要填充一个 signature，这样我们通过 signature 获取到输入和输出的所有信息，就可以使用 sess 来直接执行。这里我是直接利用 tensorflow 的命名规则来获取相关的信息。

```python
import subprocess

import tensorflow as tf
from tensorflow.python.saved_model.builder import SavedModelBuilder
from tensorflow.python.saved_model import tag_constants

var = tf.Variable(3, name="he")
sess = tf.Session()

sess.run(tf.global_variables_initializer())
path = "./saved_model"
subprocess.check_call("command rm -rf {}".format(path), shell=True)

# Build signature
tensor_info_var = tf.saved_model.utils.build_tensor_info(var)
signature_key = tf.saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY
prediction_signature = (
    tf.saved_model.signature_def_utils.build_signature_def(
        inputs={},
        outputs={"var": tensor_info_var},
        method_name=tf.saved_model.signature_constants.PREDICT_METHOD_NAME
    )
)

builder = SavedModelBuilder(path)
builder.add_meta_graph_and_variables(
    sess,
    tags=[tag_constants.SERVING],
    signature_def_map={
        signature_key: prediction_signature
    },
)
builder.save()

with tf.Session(graph=tf.Graph()) as sess:
    meta_graph_def = tf.saved_model.loader.load(sess, [tag_constants.SERVING], path)
    signature_def = meta_graph_def.signature_def
    print(sess.run(signature_def[signature_key].outputs["var"].name))

```

### Directory structure

其实不管是 checkpoint 还是 saved model。其实关于数据部分是类似的：{name}.index, {name}.data-{shardindex}-of-{shardnum}。如下代码也是可以正常 restore 的：

```python
import tensorflow as tf

with tf.Session(graph=tf.Graph()) as sess:
    var = tf.Variable(-1, name="he")
    sess.run(tf.global_variables_initializer())

    saver = tf.train.Saver()
    # saver.restore(sess, "./checkpoint/my-ckpt")
    saver.restore(sess, "./saved_model/variables/variables")
    print(sess.run(var))
```
可以从 saved model 对应的数据部分恢复。其它 checkpoint 相对于 saved model：<br />

- checkpoint 文件：这个文件是记录一些 checkpoint 的信息，例如当前最新的，以及最近的几个版本
   - 这些信息可以便于 checkpoint 的管理，例如清理过期的 checkpoint
- checkpoint.meta 和 saved_model.pb
   - 二者在内容是类似的，都是通过 tf.tran.export_meta_graph 生成

上述在恢复路径中我们增加到了 **variables/variables** ，这是因为 Restore 相关 Op 会优先探测版本 2 格式的记录，而这个格式会探测 {path}.index 文件的存在即 my-ckpt.index 或者 variables.index。所以路径要比 checkpoint 多一点。

### Cpp
前面都是 Python 前端怎么去使用，tensorflow 背后是怎么实现这些功能的呢？大概的文件结构如下：

![image.png](/images/tensorflow/save-and-restore/1597671410637-ebd6654a-2c62-44fb-b1e8-957baf713a54.png)

```python
from tensorflow.python import pywrap_tensorflow
path = "checkpoint/my-ckpt"  # saved_model/variables/variables
reader = pywrap_tensorflow.NewCheckpointReader(path)
print(reader.get_variable_to_shape_map())
```

#### CheckpointReader implementation

![image.png](/images/tensorflow/save-and-restore/1597671638822-a94408a6-2ab2-4efc-adf2-96e9afdee969.png)

##### tensor_bundle.proto

![image.png](/images/tensorflow/save-and-restore/1597671969002-56160c1b-4ac0-4671-87e7-bd842b39539b.png)

对于每一个 tensor 都会记录相应的信息。在读取时，根据协议进行反解就行。


### saver.py

saver.py 基本是上是 Tensorflow 保存模型的默认入口，例如 MonitoredTrainingSession，CheckpointSaverHook 等。<br />包括主要类：

- BaseSaverBuilder
- BulkSaverBuilder
- Saver

#### BaseSaverBuilder && BulkSaverBuilder

主要的接口如下：

![image.png](/images/tensorflow/save-and-restore/1597721722447-e1517763-f0be-4cc0-bc83-a73f4f79b310.png)

Save 和 Restore 都要依赖一个 SaveableObject (tensorflow/python/training/saving/)对象，这个对象会依赖：

- Op： 产出需要保存 tensor 的 op
- specs：SaveSpec
   - SaveSpec(tensor, slice_spec, name, dtype=None)

现在默认的版本都是 V2。V2 的保存都会先保存成一个临时文件，然后再 Rename 成最终的文件。

#### Saver

![image.png](/images/tensorflow/save-and-restore/1597723296753-041977ca-026c-49ef-9883-370f61330864.png)

- 构造 saver_def

默认使用：BulkSaverBuilder.build 来生成 saver_def

- save:

```python
sess.run(
    self.saver_def.save_tensor_name,
    {self.saver_def.filename_tensor_name: checkpoint_file},
)
```

- restore:

```python
sess.run(
    self.saver_def.restore_op_name,
    {self.saver_def.filename_tensor_name: save_path},
)
```
### Reference

- [SavedModel Doc](https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/saved_model/README.md)
- [SavedModel API](https://www.tensorflow.org/versions/r1.15/api_docs/python/tf/saved_model)
