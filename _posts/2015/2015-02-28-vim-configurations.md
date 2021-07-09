---
layout: post
title: vim configuration
categories: [tools, ]
tags: [vim, ]
---


作为在linux下的程序猿，如果不知道如何使用vim，那其实不算是一个真正的程序猿（前提是不在图形化界面的环境中）。但是vim是那种学习曲线比较陡峭的工具，只有你真正的长时间去化时间学习vim的命令你才可以真正的去了解，让vim称为神的编辑器。

这篇文章主要是想总结一下自己在vim使用过程中的一些基本的方法，一来是作为自己的借鉴；而来是也为让其它需要的人得到帮助。

```vim
" normal configurations
set nu " show line number
set tabstop=4 shifwidth=4
set expandtab
set autoindent
filetype plugin indent on
syntax on
set hlsearch " highlight search
" set backup extension and directory
set backupext=.bak
set backupdir=~/Backup
iabbrev @@ wxxx@xxx.com " quick insert eamil info
```

上面只是做一些基本的设置，接下来介绍几款比较实用的插件，这些插件让vim真正的强大起来。

### supertab

supertab是一款自动补全的vim插件，其实不用这个插件我们通过使用c-n, c-p也可以自动补全，但是这个插件提高了效率。但是该插件有个缺点，即当我们真正需要输入tab时，却不可以，除非我们在前面是空格或者一行其实位置处。这里有一个方法：c-v, tab， c-v告诉vim接下来的输入直接作为输入，不需要做任何解析。

### air-line

这个插件和vim-powerline很相似，但是作者说这个插件是更加轻量级，而且不依赖其它。这个插件的功能是让vim的状态栏的功能更加丰富。它可以显示文件名字，显示函数名字，存在一些警告信息等。具体的内容大家可以在github上找到。

### indent-line

当程序变得庞大起来时，往往对齐成了问题，特别是对于python这种对于对齐要求十分严格的脚本。indent line是让对齐可视化。开发插件的作者利用了vim的新特性（vim7.3版本及以上）。对于平常的一些需求，我们可以通过如下命令来实现：

```vim
set list
```

这样我们tab就会显示成\^I，我们可以通过更加细化的设置，将tab设置成我们想要的符号：

```vim
set listchars=tab:>,trail:-
```

tab会被显示成>-，尾部多余的空白字符会显示成-

### tagbar

tagbar和taglist功能很类似，不过功能更强大。它可以将程序文件中的函数声明、类、宏定义等归纳出来，并且显示成侧边栏。我们可以使用c-w，右，来选择这个窗口，然后快速在函数声明之间切换。这里有一些小的快捷方式：

```vim
nmap <F8> :TagbarToggle<CR>
```

* **gd** 局部查找变量
* **[[** **]]** 在函数定义体之间内移动
* **gf** 在include位置打开对应的文件名字

### ctags

vim的高版本是自带ctags，我们只需要在对应目录下使用如下命令：

```vim
ctags -R ./
```

然后在.vimrc配置文件中使用如下方式：

```vim
set tags=./tags; 
```

注意刚才的分号后面是由空格的，这个是让vim在当前目录中找不到ctags文件时，向上递归查找。

### Nerdtree

方便打开其它目录的文件。

```vim
nmap <F5> :NERDTreeToggle<CR>
let NERDTreeShowHidden=1 " Show hidden file
```

#### 新的切分窗口打开

移动鼠标选中文件，按下 `s` 按键即可

#### 开启拼写检查

```vim
set spell spelllang=en_us
hi clear SpellBad
hi SpellBad cterm=underline
hi clear SpellRare
hi SpellRare cterm=underline
hi clear SpellCap
hi SpellCap cterm=underline
hi clear SpellLocal
hi SpellLocal cterm=underline
```

#### 使用 Plug 来管理

首先要先安装 `vim-plug` 这个插件，然后就可以使用它来安装其它插件

```vim
call plug#begin('~/.vim/plugged')

Plug 'preservim/nerdcommenter'
Plug 'neoclide/coc.nvim', {'branch': 'release'}

call plug#end()
```
执行 `:PlugInstall` 会安装相关的插件


#### Python 语法检测

```vim
Plug 'neoclide/coc.nvim', {'branch': 'release'}
```

`:CocInstall coc-pyright`


本文完
