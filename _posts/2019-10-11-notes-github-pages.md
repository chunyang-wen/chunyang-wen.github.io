---
layout: post
title: Notes about making Github pages beautiful
categories: [blog, tools]
tags: [tools]
---

* TOC
{:toc}

### Introduction
More and more people are using Github pages as their personal website. Github pages use
Jekyll to render the site. This blog will introduce ways to make your blog more attractive.

+ Set markdown engine to `kramdown` in the `_config.yml`
+ Use Github style of input

```conf
markdown: kramdown
kramdown:
    input: GFM
```

It is better you can test your pages locally. Please refer to following article.

<a href="https://help.github.com/en/articles/testing-your-github-pages-site-locally-with-jekyll" target="_blank">
Testing your GitHub Pages site locally with Jekyll
</a>

### Auto TOC

Set `auto_ids` to `true` for `kramdown` options.

```conf
kramdown:
    auto_ids: true
```

Then in your blog, you can use following code to generate the toc.

```conf
* TOC
{:toc}
```

\* TOC is required. We can also use `1 TOC` (ordered list) instead.

### Highlight

+ Set the `highlighter` to `rouge`

```conf
highlighter: rouge
```

If you install `rougify` locally, you can generate the css file yourself. Then include the
file in your html file.

```bash
rougify style github > style.css
```

### Anchor

Please visit the blog for more details. By default `.add()` will add `h1~5`.

```js
<!-- anchor-js, Doc:http://bryanbraun.github.io/anchorjs/ -->
async("https://cdn.bootcss.com/anchor-js/1.1.1/anchor.min.js",function(){
    anchors.options = {
      visible: 'always',
      placement: 'right',
      /*icon: '¶'*/
    };
    anchors.add().remove('.intro-header h1').remove('.subheading');
})
```
