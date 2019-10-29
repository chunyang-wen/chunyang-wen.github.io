---
layout: post
title: 去除下载文档中的水印
categories: [blog, tools]
tags: [tools]
redirect_from:
 - /tools/remove-watermarks
---


在这个开放的世界，有许多知识共享出来才会有更大的价值。与此同时也要尊重原作者的权利，毕竟任何一个文档或者书籍
的诞生都是凝结着许多作者许多心血。但是对于共享出来的文档，很多时候会被加上让人反感的水印。本文就带大家一起尝试
攻克这些难题。

+ [allitebooks](http://www.allitebooks.com)
+ [it-ebooks.info](http://www.it-ebook.info)

上述两个网站上可以下载到很多高清的 PDF（现在第二个网站已经无法正常下载了）。但是这两个网站有个共同的特点：**水印**等。
之前简单研究过怎么去除 it-ebook.info 的水印，但是多次尝试都失败了，屡战屡败。

> 一件事情没有成功有时候是因为你没有足够得渴望。

上述话不知道从哪里引用的，但是有时候想想还是挺有道理的。最近分析了 allitebooks 网站的页面内容，开发了一个简单的爬虫
来从这个网站上下载免费的电子书（这部分内容会单独写一篇总结，感觉过程还是挺好玩的，
[toy-spiders](https://github.com/chunyang-wen/toy-spiders/)）。但是如上述所言，存在水印，
对于经常看到 PDF 底端的水印表示不满。此外有时候需要去打印 PDF，去除水印也会让打印结果更美观。

### vim 查看和 sed 删除

下载完PDF后，我用 vim 直接打开，然后搜索水印对应的点击串，发现：每个点击串都出现在单独的行。于是觉得是不是把点击串所
在的行直接删除就可以把水印去除。

```shell
# sed命令原地修改
sed -i '/click_url/d' document
```

上述命令 -i 表示直接将修改应用到源文件（实际上 sed 会创建备份文件，然后再 mv 回去）。click\_url部分表示点击串的
模式。 d 命令表示直接删除匹配的行。

Bingo！水印都去除了。这是一次意外的收获。下面会讲解如何去除 it-ebooks 的水印，这个就相对难了。

### vim 查看和 awk 去水印

有了之前在 allitebooks 的经验，决定在 it-ebooks 网站的电子书上同样进行类似的 sed 命令，替换 click\_url部分。

Bingo！ 发现水印也没了。如果事情都是这么一帆风顺，那就没什么意思了。

将鼠标移动至原来水印的位置，发现鼠标会变成可点击状态，然后点击下去后，由于没有点击串，它提示打开一个本地链接。
显然 sed 命令的去除水印功能并没有十分彻底，但是如果你不是一个强迫症患者，那么可以在这里结束去水印之旅。

同样用 vim 打开，然后搜索点击串。在阅读了点击串附近的内容后发现是在*创建可以点击的块*以及*相关的对象*，而且重复度很高。
于是乎去 google 了 PDF 点击串的标准。发现描述的内容和在 vim 中看到的一致。
[PDF标准](https://www.w3.org/TR/WCAG20-TECHS/PDF11.html)，在靠下面的 Resources部分附近。

总结下看到的规律：

+ 定位点击串所在的行（/URI xx)
+ 前面32行，后面3行是一个完整的点击水印区域

如果定位至点击串所在的行，然后往前删32行，删除当前行，再往后删除3行，那么水印即可消除。sed 可以很方便得通过模式
匹配找到所在的行，但是对于 sed 来说，一旦跳过的行你不去处理，那么就没法回头。虽然可以通过一些 
[Hack](http://www.coolshell.cn/articles/9104.html): pattern space, hold space。但是感觉 sed 不适合这种需要
回溯的场景。

sed 的兄弟 awk 通过脚本控制三个块 BEGIN{}, END{}, {}能实现非常复杂的功能。

本例的目的是找到匹配行，然后删除前32行和后3行，以及当前行。可以通过构建一个窗口大小=32的滑动窗口。在第33行到来时，
如果不匹配模式，那么输出第一行；如果匹配则清空窗口，并且跳过后面3行。在结束时，把窗口中剩余的内容输出。

```shell
#!/bin/env awk
# Usage
# This file is used to delete lines before and after a matched pattern.
# It is a pity that sed only support delete lines after a match.
#  sed '/pattern/, +2d' # will delete matched line and followed two lines.
# awk's way is to maintain a window of size w. If target line is:
#   1. matched, delete the entire window
#   2. not matched, delete the head of the window.

# awk -vw=36 -vlb=num1 -vla=num2 -vp="your-pattern" -f pattern-delete.awk source > target
# w: window size
# lb: delete lines before pattern
# lb: delete lines after pattern
# p : pattern

# for example, delete watermarks from it-ebooks.info
# awk -vw=36 -vlb=32 -vla=3 -vp="\/URI (http:\/\/www.it-ebooks.info\/)" -f pattern-delete.awk  source > target

BEGIN{
	FS = "\n";
	OFS = "\t";
	window = w; #36;
	line_before = lb; #32;
	line_after = la;  #3;
	target_line = line_before;
	shift_index = 0; # when remove ++shift_index
	current_index = 0;
	pattern = p; # get from input
	skip_index = 0;
	BINMODE = 3;
}
{
	if (skip_index > 0) {
		--skip_index;
		next;
	}
	#print "Index", current_index, shift_index, target_line
	if (current_index - shift_index < target_line) {
		a[current_index] = $0;
		++current_index;
		next;
	}
	#print "Cur: ", $0, pattern, match($0, pattern)
	if (match($0, pattern) != 0) {
		# found a match
		shift_index += window;
		current_index = shift_index;
		skip_index = line_after;
		delete a;
	} else {
		print a[shift_index];
		delete a[shift_index];
		a[current_index] = $0;
		++shift_index;
		++current_index;
	}
}
END {
	# print shift_index to current_index
	while (shift_index < current_index) {
		print a[shift_index];
		++shift_index;
	}
}
```

具体可以去[Github: pattern delete](https://github.com/chunyang-wen/code-practice/blob/master/Shell/pattern-delete.awk)

Bingo！终于去除了水印，妈妈再也不用担心我的学习了。

本文完
