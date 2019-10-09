#!/bin/sh

# Generate template for weekly digest

END=`date +"%Y%m%d"`
DIFF=7

if [[ "$OSTYPE" == "darwin"* ]]
then
    START=`date -j -f "%Y%m%d" -v-${DIFF}d ${END} +"%Y%m%d"`
else
    START=`date -d "${START} -${DIFF} days" "+%Y%m%d"`
fi

FILE=`date +"%Y-%m-%d"`"-weekly-digest-${END}".md

cat > ${FILE} << EOF
---
layout: post
title: Leetcode summary of ${START}-${END}
categories: [blog, algorithm]
tags: [leetcode]
---

+ [Summary](#summary)
+ [Highlight](#highlight)
+ [Code Section](#code)

<a id="summary"></a>

### Summary

**Solved problems list**


<a id="highlight"></a>

### Highlight

<a id="code"></a>

### Code Section

The sequence of code is the same with the problem list.

EOF
