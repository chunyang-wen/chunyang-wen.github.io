---
layout: post
title: Merge tensorflow models
categories: [blog, tensorflow]
tags: [tensorflow]
---

Sometimes you want to transfer certain weights from multiple models into a single model
or just want to merge multiple models. There are at least two ways to do that:

+ `init_from_checkpoint`
+ `gen_io_ops.merge_v2_checkpoints`


+ toc
{:toc}

### init_from_checkpoint

You can refer to [tf.train.init_from_checkpoint](https://www.tensorflow.org/api_docs/python/tf/compat/v1/train/init_from_checkpoint).

```python
tf.train.init_from_checkpoint(init_from_checkpoint(
    ckpt_dir_or_file, assignment_map
)
```

+ `ckpt_dir_or_file`
  + Can be a checkpoint directory or file: /path/to/checkpoint\_dir, /path/to/checkpoint\_dir/model-1234
  + Can be a saved model: /path/to/saved\_model/variables/variables (The second variables is the name prefix of `variables.index`)
+ `assignment_map`
  + key: can be a scope
  + value: can be variable name, variable reference

It is very flexible. Under the hood, `init_from_checkpoint` modifies the `initializer` of a variable. When we run `tf.global_variables_initializer()`, the related restore op will be executed.

```python
variable._initializer_op = init_op
restore_op.set_shape(variable.shape)
variable._initial_value = restore_op
```

If you have user-defined variables such as you create a `AwesomeVariable` which behaves like a tensorflow Variable but with a different back-end storage. You can define a similar function by creating the user-defined `initializer_op`.

```python
# Create your op using
io_ops.restore_v2

# Replace the initializer op
variable._initializer_op = init_op
```

Multiple `init_from_checkpoint` can be called with different `ckpt_dir_or_file`. As a result, a single model's variables can be initialized from different source checkpoints or saved models.

```python
import os
import tensorflow as tf

os.makedirs("./models/a", exist_ok=True)
os.makedirs("./models/b", exist_ok=True)

with tf.Session(graph=tf.Graph()) as session:
    tf.Variable(3, name="a")
    saver = tf.train.Saver()
    session.run(tf.global_variables_initializer())
    saver.save(session, "./models/a/model-a")


with tf.Session(graph=tf.Graph()) as session:
    tf.Variable(4, name="b")
    saver = tf.train.Saver()
    session.run(tf.global_variables_initializer())
    saver.save(session, "./models/b/model-b")


with tf.Session(graph=tf.Graph()) as session:
    a = tf.Variable(1, name="a")
    b = tf.Variable(1, name="b")
    tf.train.init_from_checkpoint("./models/a/model-a", {"a": a})
    tf.train.init_from_checkpoint("./models/b/model-b", {"b": b})
    session.run(tf.global_variables_initializer())
    print(session.run(a))
    print(session.run(b))

```

### gen_io_ops.merge_v2_checkpoints

When tensorflow loads a model, the only requirement is that: all variables in the model must have
a valid value in the checkpoint. So we can first merge checkpoints of different models and then just load once.


 ```python
 import tensorflow as tf
from tensorflow.python.ops import gen_io_ops

src = tf.constant(["./models/a/model-a", "./models/b/model-b"])
target = tf.constant("./models/merged_model")

op = gen_io_ops.merge_v2_checkpoints(src, target, delete_old_dirs=False)

tf.Session().run(op)

with tf.Session(graph=tf.Graph()) as session:

    a = tf.Variable(1, name="a")
    b = tf.Variable(1, name="b")
    saver = tf.train.Saver()
    saver.restore(session, "./models/merged_model")
    print(session.run(a))
    print(session.run(b))

 ```

Be careful that `delete_old_dirs` will delete the `.index` and `.data` file no matter it is set to `True` or `False`.

