---
layout: post
title: Diagram in UML
category: [blog, tools]
tags: [tools]
---

UML (Unified Modeling Language) 是一个通用的建模工具，其很多图形的绘制对程序员来说是比较重要地
理清思路的工具。本文简单介绍下其类图中常用的设置，工具名称：Visual Paradigm。它有社区版本，可以
体验一般的功能。

## 新建一个类

新建一个类很简单，直接在 UML 工具中拖出一个框就行。

![New Class](/images/tools/uml/new-class.png)

新建一个类图有好几种类型，比较常见的：

+ 普通的类
  + 类可以是抽象类，或者接口类
+ 枚举类
  + 枚举类在 C++11，Java，Python 中都有相关的专门解决方法

![Demo new class](/images/tools/uml/demo-new-class.png)

## 类的属性设置

类的属性：

+ 类本身是抽象的
+ 类的接口是抽象

在 UML 图中会将类或者操作的名字设置为斜体表示其实抽象的

![Abstract class and operation](/images/tools/uml/abstract-class-operation.png)

## 类之间的关系

常用类之间的关系：

+ 接口实现和接口之间的关系（Realization)
+ 类之间的派生关系（Generalization）
+ 类之间的组合关系
  + Composition: 整体与部分的关系，部分离开整理没有意义 (人：四肢，头部)
  + Aggregation: 整体与部分的关系，类可以独立 （计算机：主机，显示器）
  + Association：类之间的关系（一个人可以有多个手机）
  + Dependency: 之间存在调用的依赖关系

![Class relationship](/images/tools/uml/class-relationship.png)

需要注意各种关系的顺序：

+ 派生和实现都是指向基类或者接口
+ 依赖关系：指向依赖的对象
+ 组合、聚合：指向整体
+ 关联关系：指向关联的物体，人指向手机

本文完


