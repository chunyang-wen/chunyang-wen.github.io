#!/bin/sh

FILE=$1

echo "Generating file: ${FILE}"

cat > ${FILE} << EOF
---
layout: post
title:
categories: [blog, algorithm]
tags: [dailycodingproblem]
---

+ toc
{:toc}

### Problem

### Solution


EOF
