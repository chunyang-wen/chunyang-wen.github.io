---
layout: post
title: Feature column a tutorial
categories: [blog, tensorflow]
tags: [tensorflow]
---

+ toc
{:toc}

**本篇文章翻译自：Demonstration of TensorFlow Feature Columns (tf.feature_column)，标题改了下。**

![image.png](/images/tensorflow/feature-column/1599731488110-7ce09327-0bf2-4c61-99fb-444e16b8cc18.png)

在这篇帮助文档中你将学习到：

- 什么是 Tensorflow 中的 feature column
- 数值的 feature column
- 分桶 feature column
- 分类 feature column
- 指示 feature column
- 向量化 feature column
- 哈希的 feature column
- 交叉的 feature column
- 在 tf.keras.models 中如何使用
- 在 estimator 中如何使用（线性和基于树的模型）


### 特征列 feature column

这篇文章详细介绍特征列。设想特征列就是原始数据和 estimator 之间的中间桥接。特征列十分丰富，你可以从很多种原始数据转化得到 Estimator 数据可以使用的方式，便于试验。

> 简而言之，特征列是原始数据和 Estimator 以及模型之间的桥梁。

![image.png](/images/tensorflow/feature-column/1599731856151-6b19c869-9449-42a9-a5ff-471a36e42de5.png)


### 深度神经网络输入

一个深度神经网络可以操作什么类型的数据？答案当然是数值，例如 (tf.float32)。毕竟，神经网络中的每一个神经元都会对权重或者数据数据上进行乘或者加的操作。然而现实中的输入数据，经常包含非数值（分类的 categorical）数据。例如，考虑一个产品类型的特征，它可能包含一些三个非数值的值：

- kitchenware
- electronics
- sports

机器学习（Machine Learning, ML) 模型通常使用简单的向量来表示分类的值，1 表示该值出现，0 表示该值缺失。例如，当产品类型设置为 sports 时，一个机器学习模型通常会使用 [0, 0, 1] 来表示，它的含义是：

- 0: kitchenware 不存在
- 0: electronics 不存在
- 1: sports 存在

所以，尽管原始数据可以是数值或者分类的，机器学习模型会将所有特征表示为数值。


### Feature columns

如下图所示，你可以利用 Estimator （Iris 的 DNNClassifier） 的 feature column 参数指定模型的输入。特征列搭建输入数据（input_fn 的返回值）和模型之间的桥梁。

![image.png](/images/tensorflow/feature-column/1599732216276-55b4d479-5aa4-415e-a392-7d1a9cd673c5.png)

调用 `tf.feature_column` 包中的函数来创建特征列。这篇文章介绍该模块中的 9 个函数。如下图所示，所有的 9 个函数要么返回 `CategoricalColumn` 或者一个 `Dense-Column` 。 `bucketized_column` 例外，它集成自二者。

![image.png](/images/tensorflow/feature-column/1599732435827-a27f92b3-329a-4955-84ae-e1334e4ce257.png)

让我们来详细研究这些函数。

### 引入 Tensorflow 和其它库

```python
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import feature_column
from tensorflow.keras import layers
```

### 构造示例数据

```python
data = {'marks': [55,21,63,88,74,54,95,41,84,52],
        'grade': ['average','poor','average','good','good',
                  'average','good','average','good','average'
        ],
        'point': ['c','f','c+','b+','b','c','a','d+','b+','c']}
```

### 示例数据

```python
df = pd.DataFrame(data)
df
```

![image.png](/images/tensorflow/feature-column/1599732542434-c2a3078f-0bcc-4ed0-affb-315debcfa73b.png)

### 演示几种不同类型的特征列

```python
# A utility method to show transromation from feature column
def demo(feature_column):
  feature_layer = layers.DenseFeatures(feature_column)
  print(feature_layer(data).numpy())
```

### 数值列 (Numeric columns)

特征列输出变成模型的输入（使用上述 `demo` 函数，我们可以清晰看到来自 dataframe 的数据怎么转换的）。数值列是最简单的列类型。可以用它来表示实值的特征。当使用这个特征列时，你的模型会接收到来自 dataframe 一样的数据。

```python
marks = feature_column.numeric_column("marks")
demo(marks)
>> [[55.]
   [21.]
   [63.]
   [88.]
   [74.]
   [54.]
   [95.]
   [41.]
   [84.]
   [52.]]
```

### 分桶列 (Bucketized columns)

通常你不想将一个数值直接喂给模型，取而代之的是根据数值的范围将值切换为多个不同的类。考虑原始数据表示一个人的年龄。我们利用分桶列将年龄切分为多个不同的桶，而不是直接将年龄表示为一个数值列。注意下述的 one-hot 值表示每一行年龄段匹配的范围。桶包括左边界，不包括右边界。例如，假设原始数据表示房子的建造年代。我们会将年代切分为 4 个桶，不用标量数值列来表示年代。

![image.png](/images/tensorflow/feature-column/1599736424381-47a5130b-ef61-42b6-97a9-f53c6286ae5f.png)

模型将上述桶表示为：

![image.png](/images/tensorflow/feature-column/1599736448994-8f827adc-4a90-42b3-a177-2dc50ee6762b.png)

为什么我们会想切分一个对模型完全合法的数值为多个类别值？恩，单一的输入数切分为一个 4 个元素的向量。因为，模型可以学习得到 4个不同的权重，而不是 1 个；4 个权重比 1 个权重产出更丰富的模型。更重要的是，分桶可以让模型显示的区分不同的年代范围，因为只有一个元素被设置为 1，其它位置都被清 0。例如，当我们只是使用一个单一数值（年）作为输入，线性模型只能学到线性的关系。所以，分桶给模型提供额外的灵活度来学习。


下面代码展示怎么来使用分桶的特征：

```python
marks_buckets = feature_column.bucketized_column(
    marks, boundaries=[30,40,50,60,70,80,90]
)
demo(marks_buckets)
>> [[0. 0. 0. 1. 0. 0. 0. 0.]
   [1. 0. 0. 0. 0. 0. 0. 0.]
   [0. 0. 0. 0. 1. 0. 0. 0.]
   [0. 0. 0. 0. 0. 0. 1. 0.]
   [0. 0. 0. 0. 0. 1. 0. 0.]
   [0. 0. 0. 1. 0. 0. 0. 0.]
   [0. 0. 0. 0. 0. 0. 0. 1.]
   [0. 0. 1. 0. 0. 0. 0. 0.]
   [0. 0. 0. 0. 0. 0. 1. 0.]
   [0. 0. 0. 1. 0. 0. 0. 0.]]
```

### 分类特征 (Categorical columns)

#### 指示和向量列（Indicator and embedding columns)

指示列和向量列不是直接作用于特征，它们以分类特征列为输入。

#### 指示列 (Indicator columns)

在数据集中，质量以字符串的形式表示 (例如 `poor` , `average` ，或者 `good` )。我们不能直接给模型提供字符串输入。取而代之，我们必须将它们映射为数值。分类词汇列（Categorical vocabulary column) 提供一种将字符串表示为 one-hot 向量的方式（很像之前看到的年龄分桶）。词汇表可以传递给 `categorical_column_with_vocabulary` ，或者利用 `categorical_column_with_vocabulary_file`来加载。

我们不能给模型直接传递字符串，我们必须将字符串转化为数值或者分类的值。分类词表列提供了将字符串表示为 one-hot 向量的很好方法。例如：

![image.png](/images/tensorflow/feature-column/1599788407886-980afcae-92f2-4467-b398-b17c3e13e7dc.png)

```python
grade = feature_column.categorical_column_with_vocabulary_list(
      'grade', ['poor', 'average', 'good'])
grade_one_hot = feature_column.indicator_column(grade)
demo(grade_one_hot)
>> [[0. 1. 0.]
   [1. 0. 0.]
   [0. 1. 0.]
   [0. 0. 1.]
   [0. 0. 1.]
   [0. 1. 0.]
   [0. 0. 1.]
   [0. 1. 0.]
   [0. 0. 1.]
   [0. 1. 0.]]
```

#### 向量列 (Embedding columns)

假设我们不是有几个可能的字符串，而是每类有成千甚至更多的字符串。由于多种原因，当种类数据变大时，使用 one-hot 编码来训练神经网络变得不现实。我们可以使用向量列来克服这个限制。向量列将数据表示为低维稠密的向量，每一个位置表示任意数，不仅是 0 和 1，不像 one-hot 表示为多维的向量。向量的长度 （下图示例是 8）是可以必须要好调整的参数。

关键点：最佳使用向量列的时机是分类具有好多可能的值。这里我们用 1 只是示意，这样你以后为不同的数据集修改时有一个完整的样例做为参考。

#### Point 列编码为指示列（Point column as indicator_column)

```python
point = feature_column.categorical_column_with_vocabulary_list(
 ‘point’, df[‘point’].unique())
point_one_hot = feature_column.indicator_column(point)
demo(point_one_hot)
>> [[1. 0. 0. 0. 0. 0. 0.]
   [0. 1. 0. 0. 0. 0. 0.]
   [0. 0. 1. 0. 0. 0. 0.]
   [0. 0. 0. 1. 0. 0. 0.]
   [0. 0. 0. 0. 1. 0. 0.]
   [1. 0. 0. 0. 0. 0. 0.]
   [0. 0. 0. 0. 0. 1. 0.]
   [0. 0. 0. 0. 0. 0. 1.]
   [0. 0. 0. 1. 0. 0. 0.]
   [1. 0. 0. 0. 0. 0. 0.]]
```

#### Point 列编码为向量列 （Point column as embedding_column)

```python
# Notice the input to the embedding column is the categorical column
# we previously created
point_embedding = feature_column.embedding_column(point, dimension=4)
demo(point_embedding)
>>[[ 0.6905385  -0.08270663  0.15046535 -0.3439266 ]
   [ 0.56737125  0.06695139 -0.58371276  0.49233127]
   [ 0.4538004  -0.03839593 -0.4058998  -0.1113084 ]
   [-0.50984156 -0.11315092  0.39700866  0.09811988]
   [ 0.35654882  0.41658938 -0.67096025 -0.2758388 ]
   [ 0.6905385  -0.08270663  0.15046535 -0.3439266 ]
   [ 0.58311635  0.6259656  -0.27828178  0.14894487]
   [-0.721768   -0.0898371   0.5906883  -0.4207294 ]
   [-0.50984156 -0.11315092  0.39700866  0.09811988]
   [ 0.6905385  -0.08270663  0.15046535 -0.3439266 ]]
```

当我们使用指示列时，我们告诉 Tensorflow 完成我们 `product_class` 作为分类列一样的事情。也就是指示列将每一个类型表示为 one-hot 向量中的一个元素，匹配位置具有 1 值，其它位置是 0。

![image.png](/images/tensorflow/feature-column/1599789026024-9253b7ed-2579-4150-b537-4aa75e42c6e8.png)

现在，假设我们不仅仅有 3 个值，而是有 100 万个值。又或者是 10 亿。由于多种原因，类别数目边的很大时，不太可能直接使用指示列来训练神经网络。

我们可以使用向量列来克服这个限制。向量列将数据表示为低维普通的向量，每一个位置可以使用不仅仅是 0 或者 1 的任意数值。不像特征列是一个高维的 one-hot 向量。向量列在每个位置允许使用更多的数值，它相对于指示列具有更小的长度。

让我们来看一个指示列和向量列对比的例子。假设我们的输入样本来自一个有限的只有 81 个字符的集合。进一步假设数据集提供如下 4 个不同的样本：

- dog
- spoon
- scissors
- guitar


这个例子中，下图表示如何处理成指示列和向量列的过程：

![image.png](/images/tensorflow/feature-column/1599789408646-d2f37e5e-49c9-47a1-ac7a-057f1b612dd1.png)

当处理样本时， `categorical_column_with..` 其中一个函数将样本的字符串映射为数值的分类值。例如一个函数将 `spoon` 映射为 [32]。（32 是假想的，实际值依赖于映射函数）。然后你可以将数值的分类值表示为如下两种方式之一：

- 指示列。函数将每一个数值分类值转化为一个 81 维的向量，分类值位置设置为 1，其它位置为 0.
- 向量列。函数将数值的分类值（0,32,79,80) 设置为一个查找表的索引。每一个查找的位置包含长度为 3 的向量

向量中的值是如何像变魔术一样赋值的？实际上，赋值发生在训练过程中。也就是说模型通过学习得到从数值分类值到向量类的最佳映射，从而解决你的问题。向量列增加模型的能力，因为向量是模型从训练数据中学到的和分类之间的新关系。

### 哈希特征列 (Hashed feature column)

另外一个表示大量分类特征的方式是使用 `categorical_column_with_hash_bucket` 。这个特征列计算输入的哈希值，然后选择 `hash_bucket_size` 中的一个桶来编码字符串。当使用这个列时，你不用提供词汇表，你可以选择相对于实际分类数较小的哈希桶数，以此来节约空间。

关键点：这个技术的重要缺点是不同的字符串可能被映射到同一个桶，从而发生冲突。然而实际中这个方法在一些数据集中工作得很好。

```python
point_hashed = feature_column.categorical_column_with_hash_bucket(
      'point', hash_bucket_size=4
)
demo(feature_column.indicator_column(point_hashed))
>> 
[[1. 0. 0. 0.]
 [1. 0. 0. 0.]
 [0. 1. 0. 0.]
 [0. 0. 0. 1.]
 [0. 0. 1. 0.]
 [1. 0. 0. 0.]
 [0. 0. 0. 1.]
 [1. 0. 0. 0.]
 [0. 0. 0. 1.]
 [1. 0. 0. 0.]]
```

目前为止，你可能会想：这太疯狂了。毕竟我们将不同的输入值强制映射到更小的分类集合。这意味着两个不相关的输入可能被映射为同一类，这也对导致在神经网络看来是同样的事情。下面显示这种困境，显示 `kitchenware` 和 `sports` 被映射的 12 这个相同的桶。

![image.png](/images/tensorflow/feature-column/1599790266053-d96fa125-2d52-4af3-ad5d-4af29522d479.png)

想很多机器学习中反常识的现象一样，哈希在实际中工作的非常好。因为哈希分类给模型提供了一些隔离。模型可以进一步利用其它特征来进一步区别 `kitchenware` 和 `sports` 。

### 交叉列 (Crossed feature columns)

组合多个特征为一个单一的特征，称之为特征交叉。模型可以为每一个组合的特征学得不同的权重。这里，我们将创造一个新的特征，它是 `marks` 和 `age` 的交叉。注意到 `cross_column` 不是基于所有可能组合构建一个完整的表（表可能很大）。它是基于 `hashed_column` ，所以你可以控制表的大小。

更具体的，假设我们的模型可以计算亚特兰大周房地产的价格。房地产的价格随着位置在整个城市中变化很大。单独使用经纬度来表示位置不是很有用。但是我们可以将经纬度交叉成一个特征。假设我们将亚特兰大表示成一个 100 * 100 的矩形块，表示经过经纬度交叉得到的 10000 个区域。这种特征交叉使得模型可以根据每一个区域来训练价格，这相对于单独的将维度的关系更加强。

下图展示我们的计划，在角落位置利用红色字体标出了经纬度：

![image.png](/images/tensorflow/feature-column/1599791117628-09e9538b-0b18-4575-8193-e354a7eacad7.png)

```python
crossed_feature = feature_column.crossed_column(
    [marks_buckets, grade], hash_bucket_size=10
)
demo(feature_column.indicator_column(crossed_feature))
>>
[[0. 0. 0. 0. 0. 0. 0. 0. 1. 0.]
 [0. 0. 0. 0. 1. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 1. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 1. 0. 0. 0. 0. 0.]
 [1. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 1. 0.]
 [0. 0. 0. 0. 0. 1. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 1. 0. 0. 0.]
 [0. 0. 0. 0. 1. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 1. 0.]]
```

你可以如下任意方式进行特征交叉：

- 特征名字： `input_fn` 返回的字典的键名字
- 任意一个分类类，除了 `categorical_colun_with_hash_bucket` （因为交叉列会将输入哈希，译注：重复哈希可能会有问题）


但是完整的格子只针对有限的词汇表才可行。为了不构造这个潜在的很大的输入表， `cross_column` 只会构造 `hash_bucket_size` 大小的列。特征列针对输入的组合执行一个哈希函数，针对 `hash_bucket_size` 取余，然后给每一个样本一个索引。

如之前讨论，计算哈希和取余会限制分类的数，可能会导致分类冲突。也就是多个 （经度，维度）特征交叉会进入同一个桶。虽然实际中进行特征交叉仍然可以显著增加模型的能力。

有点反常识的是，当做特征交叉时，通常你需要将原始特征也作为模型的输入。独立的经度和维度提升模型在交叉特征中发生哈希冲突时区分能力。

### 参考

- Stackoverflow：[https://stackoverflow.com/questions/54375298/how-to-use-tensorflow-feature-columns-as-input-to-a-keras-model](https://stackoverflow.com/questions/54375298/how-to-use-tensorflow-feature-columns-as-input-to-a-keras-model)
- Dense features: [https://www.tensorflow.org/api_docs/python/tf/keras/layers/DenseFeatures](https://www.tensorflow.org/api_docs/python/tf/keras/layers/DenseFeatures)
- Feature column: [https://www.tensorflow.org/api_docs/python/tf/feature_column](https://www.tensorflow.org/api_docs/python/tf/feature_column)
- [原文] Demonstration of TensorFlow Feature Columns (tf.feature_column):[https://medium.com/ml-book/demonstration-of-tensorflow-feature-columns-tf-feature-column-3bfcca4ca5c4](https://medium.com/ml-book/demonstration-of-tensorflow-feature-columns-tf-feature-column-3bfcca4ca5c4)

### 其它

#### 非 eager 代码

原文中使用的是 eager 模式。对于非 eager 模式，修改后的代码如下：

- 当使用哈希相关的功能时，会需要初始化表

```python
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import feature_column
from tensorflow.keras import layers

data = {'marks': [55,21,63,88,74,54,95,41,84,52],
        'grade': [
            'average','poor','average','good','good','average',
            'good','average','good','average'
        ],
        'point': ['c','f','c+','b+','b','c','a','d+','b+','c']}

df = pd.DataFrame(data)

sess = tf.Session()


# A utility method to show transformation from feature column
def demo(feature_column):
    feature_layer = layers.DenseFeatures(feature_column)
    tensor = feature_layer(data)
    sess.run(tf.global_variables_initializer())
    sess.run(tf.tables_initializer())
    print(sess.run(tensor))


marks = feature_column.numeric_column("marks")
demo(marks)

marks_buckets = feature_column.bucketized_column(
    marks, boundaries=[30,40,50,60,70,80,90]
)
demo(marks_buckets)

grade = feature_column.categorical_column_with_vocabulary_list(
      'grade', ['poor', 'average', 'good'])
grade_one_hot = feature_column.indicator_column(grade)
demo(grade_one_hot)

point = feature_column.categorical_column_with_vocabulary_list(
 'point', df['point'].unique())
point_one_hot = feature_column.indicator_column(point)
demo(point_one_hot)

point_embedding = feature_column.embedding_column(point, dimension=4)
demo(point_embedding)

point_hashed = feature_column.categorical_column_with_hash_bucket(
      'point', hash_bucket_size=4)
demo(feature_column.indicator_column(point_hashed))


crossed_feature = feature_column.crossed_column(
    [marks_buckets, grade],
    hash_bucket_size=10
)
demo(feature_column.indicator_column(crossed_feature))
```

#### 分类特征补充

目前文中示意的代码基本都是需要知道分类的数，实际中可能我们并不知道分类的个数。这时需要使用：<br />`categorical_column_with_identity` 。这个是假设原始的特征就已经是数值化。后面可以继续使用这个值来进行编码为 `indicator_column` 或者 `embedding_column` 。
