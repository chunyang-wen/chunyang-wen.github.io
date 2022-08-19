---
layout: post
title: Arrays and dict in bash
categories: [blog, shell]
tags: [shell]
---

Most languages will have builtin data structures such as array(list) or
dict(hashtable). Is it interesting that whether `bash` has similar choices?

+ toc
{:toc}


## Dict/Hashtable

### Create and access

bash version > 4.0

```bash
declare -A dict
dict["A"]="B"
dict["C"]="D"

size=${#dict[@]}

key="A"
echo ${dict[${key}]}

declare -A hash
hash=([one]=1 [two]=2 [three]=3)
echo ${hash[one]}
```

### Iterate a dict

Other interesting implementations:

```bash
declare -A dict
dict["A"]="B"
dict["C"]="D"

for i in "${!dict[@]}"
do
  echo "key  : $i"
  echo "value: ${dict[$i]}"
done
```

+ `${!dict[@]}` keys
+ `${dict[@]}` values

### Other implementation

```bash
for i in a,b c_s,d ; do
  KEY=${i%,*};
  VAL=${i#*,};
  echo $KEY" XX "$VAL;
done
```

## Array

By separating strings:

```bash
for i in a b c
do
    echo $i
done
```

By definition

```bash
a=(a b c)
for i in ${a[@]}
do
    echo $i
done

size=${#a[@]}
size=$((size-1))

for i in `seq 0 ${size}`
do
    echo ${a[$i]}
done

echo ${a[0]}

echo ${a[4]} # Out of range, get empty value
```

## Reference

+ [Is there a way to create key-value pairs in Bash script?](https://stackoverflow.com/questions/14370133/is-there-a-way-to-create-key-value-pairs-in-bash-script)
+ [How to find the length of an array in shell?](https://stackoverflow.com/questions/1886374/how-to-find-the-length-of-an-array-in-shell)
+ [3.5.3 Shell Parameter Expansion](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html)
+ [How to iterate over associative arrays in Bash](https://stackoverflow.com/questions/3112687/how-to-iterate-over-associative-arrays-in-bash)
+ [What is the difference between [@] and [\*] when referencing bash array values?](https://unix.stackexchange.com/questions/135010/what-is-the-difference-between-and-when-referencing-bash-array-values)
