---
layout: post
title: Closures in Ruby
categories:
- translating
tags:
- Ruby
- closure
---

##Closures in Ruby
@(Technology)[Ruby|Closure]

这篇文章是翻译自：[Paul Cantrell](http://innig.net/software/ruby/closures-in-ruby)。

我推荐先运行这个文件，然后一边读，一边观察其后的结果。当然你也可也先删除所有的注释，猜测所有程序的结果，以此来测试你自己Ruby能力。

一个闭包是满足如下三个准则：

+ 可以当做一个变量（value）来传递
+ 任何人只要具有那个变量的引用，在任何时候都可以执行
+ 它可以保存它创建时的上下文中的变量（它对于其封存的变量的访问是禁止的，这是其closure给人的感觉）。

closure这个名词的含义各家各持己见，一些人认为准则中不应该包括一，但是我认为应该是。

闭包是函数式编程中的主要概念，但是在其它语言中也支持（如Java的匿名内部类）。有了闭包，你可以做一些很炫的事：他们允许延迟调用（deferred execution）以及一些非常优雅的技巧。

Ruby是基于“最小惊异原则”而设计的，但是在学习时，我却有一些不愉快的惊异。当我明白想"each"这种方式的原理时，我想，“啊哈，Ruby有闭包”。但是我却发现函数不能同时接受多个块（block）---这违反了闭包可以像变量一样自由传递的原则。

这篇文档详细记录我在搞清楚Ruby中闭包到底是如何工作时的所学到的知识。


```ruby
def example(num)
    puts
    puts "-------- Example #{num}---------"
end
```

###第一部分：块

1. 块就像闭包一样，因为他们可以引用他们定义处的变量。

{% highlight ruby linenos %}
# example 1
def thrice
    yield
    yield
    yield
end
x = 5
puts "value of x before: #{x}"
thrice{x += 1}
puts "value of x after: #{x}"
{% endhighlight %}

2. 一个块可以引用它定义处的变量，而不是其调用处的变量

```ruby
# example 2
def thrice_with_local_x
    x = 100
    yield
    yield
    yield
    puts "value of x at the end of thrice_with_local: #{x}"
end

x = 5
thrice_with_local_x {x += 1}
puts "value of outer x after: #{x}"
```

3. 一个块只能引用在创建上下文中已经存在的变量，如果他们不存在，块不会创建他们(译者注：即这个变量不会再块创建的上下文中存在)

```ruby
# example 3
thrice do
    y = 10
    puts "Is y defined inside the block where it is first set?"
    puts "Yes." if defined? y
end
puts "Is y defined in the outer context after being set in the block?"
puts "NO!" unless defined? y
```

4. 目前为止，块似乎和闭包一样：他们对所创建处的变量访问是封闭的，而与他们调用处的上下文无关。但是就目前我们的使用方法来看，他们不是不全是闭包，因为我们无法传递他们。**yield**只能指代传递入相应方法的block。但是我们可以使用&符号，来继续传递块。

```ruby
# example 4
def six_times(&block)
    thrice(&block)
    thrice(&block)
end

x = 4
six_times { x += 10}
puts "value of x after: #{x}"
```

5. 现在我们具有闭包了吗？不完全是！我们不能保存一个&block，然后延迟到任何一个时间来调用它。如下代码不能编译：

```ruby
def save_block_for_later(&block)
    save = &block
end
```

但是我们可以把&符号丢掉，这样就可以传递了。

```ruby
# example 5
def save_block_for_later(&block)
    @save = block
end
save_for_later{puts "Hello"}
puts "Deferred execution of a block:"
@saved.call
@saved.call
```

但是，等等！我们不能给一个函数同时传递多个块。结果是，一个函数至多有一个块，而且&block必须是最后一个参数。

```ruby
# def f(&block1, &block2)
# def f(&block1, arg_after_block)
# f {puts "block1"} {puts "block2}
```

到底是怎么回事？我觉得这种单个块的限制违反了最小惊异原则，原因是C实现的难易程度，而不是语法问题。所以：现在我们用闭包任何健壮以及有兴趣的事的想法被毁了吗？

###Ruby中类似闭包的构建

1. 事实上想法还在。当我们利用&block传递块时，他们指向那个没有&的参数，他们是Proc.new(&param)的简写

```ruby
# example 6
def save_for_later(&b)
    @saved = Proc.new(&b)
end

save_for_later{puts "Hello again!"}
puts "Deferred execution of a Proc works just the same with Proc.new"
@saved.call
```

利用Proc，我们随时定义块，不用&参数。

```ruby
# example 7
@saved_proc_new = Proc.new {puts "I'm declared on the spot with Proc.new"
puts "Deferred execution of a Proc works just the same with ad-hoc Proc.new"
@saved_pro_new.call
```

hold住。纯闭包。但是等一等，还有更多的。Ruby一堆类似闭包的东西，可以.call的方式来调用。

```ruby
@saved_proc_new = Proc.new {puts "I am declared with Proc.new"}
@saved_prc = proc {puts "I am delcared with proc"
@saved_lambda = lambda {puts "I am declared with lambda"}
def some_method
    puts "I am declared as a method"
end
@method_as_closure = method(:some_method)
puts "Here are four superficially identical forms of deferred execution:"
@saved_proc_new.call
@saved_proc.call
@saved_lambda.call
@method_as_closure.call
```

其实事实上，至少有7中方法
+ block(implicitly passed, called with yield)
+ block(&b, f(&b) yield)
+ block(&b, b.call)
+ Proc.new
+ proc
+ lambda
+ method

尽管他们长相各异，但是其中一些事等价的。其中1和2不是真正的闭包，实际上他们是同样的东西。3-7看起来是一样的。但是他们只是语法不同还是语义上完全一样呢？

###第三部分：闭包和控制流

他们不一样，其中一个很明显的不同是他们对return语句的处理。在如下没有return语句的不同像闭包一样的东西中，他们表现方式完全一样。

```ruby
# example 9
def f(closure)
    puts
    puts "about to call closure"
    result = closure.call
    puts "closure returned: #{result}"
    "value from f"
end

puts "f returned: " + f.(Proc.new {"value from Proc.new})
puts "f returned: " + f.(proc {"value from proc})
puts "f returned: " + f.(lambda {"value from lambda})
def another_method
    "value from another_method"
end
puts "f returned: " + f.(method(:another_method))
```

但是一旦有return，好像一切都被打松散了。

```ruby
# example 10
begin
    f(Proc.new {return "value from Proc.new"))
rescue Exception => e
    puts "Failed with #{e.class}: #{e}"
end
```

上述调用会失败，因为return语句必须在一个函数里面调用，但是Proc不是实际上全功能的函数。

```ruby
# example 11
def g
    result = f(Proc.new {return "Value from Proc.new"})
    puts "f returned: " + result # never executed
    "value from g"               # never executed
end
puts "g returned: #{g}"
```

注意Proc.new中的return不仅仅从Proc中返回，直接从g中返回，不仅跳过g后续的语句，而且f后续语句也被跳过，像异常一样。这意味着当创建的上下文不存在时，调用一个带return的Proc是不可能的。

```ruby
# example 12
def make_proc_new
    begin
        Proc.new { return "Value from Proc.new"}
    ensure
        puts "make_proc_new exited"
    end
end

begin
    puts make_proc_new.call
rescue Exception => e
    puts "Failed with #{e.class}: #{e}
end
```

上述方法使得在多个线程间传递Procs不安全。一个Proc.new不是真正封闭：它取决于创建上下文是否是存在。因为return和那个上下文是绑定的。目前lambda不是这么表现的。

```ruby
# example 13
def g
    result = f(lambda {return "Value from lambda"})
    puts "f returned: " + result
    "Value from g"
end
puts "g returned: #{g}"
```

你可以调用一个lambda，尽管创建的上下文已经不存在。

```ruby
# example 14
def make_lambda
    begin
        lambda { return "value from lambda"}
    ensure
        puts "make_lambda exited"
    end
end

puts make_lambda.call
```

lambda中的return语句只是从lambda块中返回，流控制正常进行。所以lambda就像一个函数一样，Proc与其调用者的控制流程是独立的。lambda是Ruby中的真正的闭包。proc是Proc.new的简写。

```ruby
def g
    result = f(proc {return "value from proc"})
    puts "f returned: " + result
    "Value from g"
end
puts "g returned: #{g}"
```

在Ruby1.8中，它是lambda的简写，在Ruby1.9中它是lambda的简写。

"return"，从调用者返回：

+ block(called with yield)
+ block(&b => f(&b) => yield)
+ block(&b => b.call)
+ Proc.new
+ proc in 1.9

"return"，仅仅从闭包中返回

+ pric in 1.8
+ lambda
+ mthod

### 第四部分：闭包与参数个数

不同Ruby闭包中的另外一个不同点是他们如何处理不匹配的参数-参数个数不匹配。闭包除了call方法，还有一个arity方法，返回其想要的参数个数

```ruby
# example 16
puts "One-arg lambda: "
puts (lambda{|x|}.arity)
puts "Three-arg lambda: "
puts (lambda{|x,y,z|}.arity)

puts "No-args lambda: "
puts (lambda{}.arity) # about to change
puts "Varargs lambda: "
puts (lambda{|*args|}.arity)
```

```ruby
# example 17
def call_with_too_many_args(closure)
    begin
        puts "closure arity: #{closure.arity}"
        closure.call(1,2,3,3,4,6)
        puts "too many args worked"
    rescue Exception => e
        puts "too many args threw exception #{e.class}"
    end
end

def two_arg_method(x,y)
end

puts; puts "Proc.new:"; call_with_too_many_args(Proc.new {|x,y|})
puts; puts "proc:"    ; call_with_too_many_args(proc {|x,y|})
puts; puts "lambda:"  ; call_with_too_many_args(lambda {|x,y|})
puts; puts "Method:"  ; call_with_too_many_args(method(:two_arg_method))

def call_with_too_few_args(closure)
 begin
    puts "closure arity: #{closure.arity}"
    closure.call()
    puts "Too few args worked"
 rescue Exception => e
    puts "Too few args threw exception #{e.class}: #{e}"
 end
end

puts; puts "Proc.new:"; call_with_too_few_args(Proc.new {|x,y|})
puts; puts "proc:"    ; call_with_too_few_args(proc {|x,y|})
puts; puts "lambda:"  ; call_with_too_few_args(lambda {|x,y|})
puts; puts "Method:"  ; call_with_too_few_args(method(:two_arg_method))

# Yet oddly, the behavior for one-argument closures is different....

# example 18

def one_arg_method(x)
end

puts; puts "Proc.new:"; call_with_too_many_args(Proc.new {|x|})
puts; puts "proc:"    ; call_with_too_many_args(proc {|x|})
puts; puts "lambda:"  ; call_with_too_many_args(lambda {|x|})
puts; puts "Method:"  ; call_with_too_many_args(method(:one_arg_method))
puts; puts "Proc.new:"; call_with_too_few_args(Proc.new {|x|})
puts; puts "proc:"    ; call_with_too_few_args(proc {|x|})
puts; puts "lambda:"  ; call_with_too_few_args(lambda {|x|})
puts; puts "Method:"  ; call_with_too_few_args(method(:one_arg_method))
 
# Yet when there are no args...

#example 19

def no_arg_method
end

puts; puts "Proc.new:"; call_with_too_many_args(Proc.new {||})
puts; puts "proc:"    ; call_with_too_many_args(proc {||})
puts; puts "lambda:"  ; call_with_too_many_args(lambda {||})
puts; puts "Method:"  ; call_with_too_many_args(method(:no_arg_method))
    
```

Ruby中Proc.new, proc, lambda将一个参数作为一个特殊情况，表现不一致，但是method是一致的。（译者注：在Ruby2.0中行为一致，即Proc.new/proc全适应，lambda/method，全不适应，抛出异常）

###第五部分：责骂

这是一个比较令人眩晕的语法选项，具有一些不是十分清楚的细微语法区别，而且在特殊情况下表现不同。程序员希望语言能工作，就像一个捉大熊的陷阱。

为甚事情会这样？因为Ruby：

+ 由实现设计，并且
+ 受实现约束。

语言一直在发展，因为Ruby小组一直有好玩的想法，但是没有除了CRuby没有维护一个实际的说明书。一个将语言的逻辑结构表述清楚，进而帮助支出我们刚才所见的不一致性。相反，这种不一致性已经渗入语言，把像我这样想学这种语言的人搞得晕头转向，然后以为是bug就提交上去了。向上帝发誓，类似proc这种基本语义的东西不应该是一团糟，以至于不得不在版本之间回溯。是的，我知道，设计语言很难，但是像proc/lambda对arity这种问题第一次时容易解决。抱怨，抱怨。

###第六部分：总结

到现在为止，对于创建闭包的7种方法，我们发现了什么东西：


name  | True closure | Return  | Arith check
----- | ------------ |---------| -----------
block (called with yield)| N|declaring|N
block (&b => f(&b) => yield)|N|declaring|N
block (&b => b.call)| Y except return|declaring|N
Proc.new | Y except return|declaring |N
proc | alias for lambda in 1.8 / Proc.new in 1.9|
lambda | Y | closure | yes, except 1
method | Y | closure | y

下面每组在语义上相同，只是在语法上有区别：

+ block (called with yield)
+ block (&b => f(&b) => yield)

---

+ block (&b => b.call)
+ Proc.new
+ proc in 1.9

---

+ proc in 1.8
+ lambda

---

+ method

或者至少是我基于实验给出的观点。除了测试CRuby的实现，没有其他权威的回答。因为根本没有说明书，所以可能还有其他我没有发现的区别。到此为止，“Ruby makes Paul carzy”告一段落。从这里开始，将是一个特别棒的部分。

###第七部分：用闭包做一些非常炫的事

让我们一起写一个包含所有Fibonacci数的数据结构。是的，我说的是全部。这个可能吗？我们将使用闭包来实现懒惰评估，所以电脑只计算我们要它做的。

为了完成这个工作，我们将使用想Lisp一样的链表：一个递归式的数据结构，包括两个部分：car，链表下一个元素；cdr，链表其余部分。

例如，前三个数的链表是[1,[2,[3]]]。为什么呢？因为

+ [1,[2,[3] <--- car = 1, cdr = [2,[3]]
+    [2,[3] <--- car = 2, cdr = [3]
+       [3] <--- car = 3, cdr = nil

下面是遍历这种链表的类。

```ruby
# example 20
class LispyEnumerable
  include Enumerable
 
  def initialize(tree)
    @tree = tree
  end
 
  def each
    while @tree
      car,cdr = @tree
      yield car
      @tree = cdr
    end
  end
end
 
list = [1,[2,[3]]]
LispyEnumerable.new(list).each do |x|
  puts x
end
```

现在我们如何制造无穷长度链表？为了取代构建一个完整的数据结构的中的每一个节点，我们使用闭包。直到我们需要值的时候，我们才会去调用闭包。这种调用是递归的：树的顶端是个闭包，它的cdr也是闭包，cdr的cdr也是闭包。

```ruby
# example 21
class LazyLispyEnumerable
  include Enumerable
 
  def initialize(tree)
      @tree = tree
  end
 
  def each
      while @tree
          car,cdr = @tree.call # <--- @tree is a closure
          yield car
          @tree = cdr
      end
  end
end
 
list = lambda{[1, lambda {[2, lambda {[3]}]}]} # same as above, except we wrap each level in a lambda
LazyLispyEnumerable.new(list).each do |x|
  puts x
end
 
# example 22
 
# Let's see when each of those blocks gets called:
list = lambda do
  puts "first lambda called"
  [1, lambda do
    puts "second lambda called"
    [2, lambda do
      puts "third lambda called"
      [3]
    end]
  end]
end
 
puts "List created; about to iterate:"
LazyLispyEnumerable.new(list).each do |x|
  puts x
end
```

由于lambda函数可以延迟调用，所以我们得到一个无穷链表。

\<本文完\>
