---
layout: post
title: SuperTAB and YouCompleteMe compatibility
categories: [blog, tools]
tags: [tools]
---

* TOC
{:toc}

### SuperTAB

<a href="https://github.com/ervandew/supertab" target="_blank">SuperTAB Github</a>

### YouCompleteMe

<a href="https://github.com/ycm-core/YouCompleteMe" target="_blank">YouCompleteMe Github</a>

### Problems

+ <a href="https://vi.stackexchange.com/questions/10490/bypassing-tab-auto-complete" target="_blank">StackExchange</a>

`SuperTAB` and `YouCompleteMe` are both awesome plugins for Vim.

+ `SuperTAB` completes using current context.
+ `YouCompleteMe` completes in a more complex way.

They both use the key `TAB`. `SuperTAB` uses `TAB` key to trigger completion, `YouCompleteMe` uses
`TAB` to select the first item in the suggestion list.

By adding the following into your `.vimrc`

```vim
" auto close the completion window
let g:ycm_autoclose_preview_window_after_completion = 1
" only use the `Down` key to select the first item
let g:ycm_key_list_select_completion = ['<Down>']
```

Bingo! You can enjoy both.
