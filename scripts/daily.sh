#!/bin/sh

FILE=$1
DATE=`date +"%Y-%m-%d"`
FILENAME=${DATE}-${FILE}

echo "Generating file: ${FILENAME}"

cat > ${FILENAME} << EOF
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
