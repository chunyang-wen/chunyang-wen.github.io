name: inverse
layout: true
class: center, middle, inverse

---

# Git Tutorial

Wen Chunyang(chunyang.wen@gmail.com)

---

layout: false

## Git status

Any file will be in the following three stages. When we execute command, stages will move forward
or backward.

+ Working directory
    + Tracked files (already been added to git)
    + Untracked files (any new files)
+ Staged
    + Add new files
    + Add changed files
+ Commited
    + Changes has been commited

---

layout: false
## Git basic workflow

The basic workflow of git is:

+ We found some bug or something new, we **checkout** a new branch for it.
+ After finish patching it, we add any new or changed files.
+ Commit changes.
+ Push commits to remote.

---

layout: false
## Detailed commands (CONT.)

* git checkout -b branch-name
    + create a new branch with name **branch-name**
* git add:
    + git add . : add everthing here
    + git add -u . : add everything that is tracked (new files will not be added.)
* git commit -m 'message'
* git push origin branch-name

Then we can create a pull request by comparing **branch-name** with **master** for review.

### Examples

```shell
git checkout -b fix-typos
git add update.md
git commit -m 'ADD: update.md'
git push origin master
```
---

layout: false
## Where I am

### How I can know where I am?

+ git log
+ git status
    + git status -uno: only show tracked files
+ git diff
    + git diff .: show diff for specific folder
    + git diff file-name: show diff for files
    + git diff --cached ./file-name: If we add changed files, show diff between staged and HEAD

---

layout: false

## Git branch and origin management

After bug fixes or new features are merged into master, we can delete local branch and remote
branch.

+ git branch -D branch-name
+ git push origin :branch-name: use **:** to delete it

We can have multiple origins when we develop. For example, we fork some repository, constantly I
want to merge the updates from the repository I fork. A **central**(you name it) origin can be added.

+ git remote add central origin-url
+ Under the master branch of my own repository:
    + git pull central master

---

layout: false

## Git rebase

Git **rebase** is a fantastic feature. If we follow the git workflow, we will checkout a new
branch for my development from current master. After some time, both master and my own branch will
move forward, and they diverge from the time I create the branch.

Before you try to merge, first you should commit the work currently or stash them:

+ git stash

If you are going to work on after rebase, execute **git stash pop**.

The **bad way** is:

+ git checkout master && git pull
+ git checkout my-branch && git merge master

The **correct way** is:

+ git checkout master && git pull
+ git checkout my-branch && git rebase master

Now my work starts from a new master. You can also notice this through the rebase log.

---

layout: false

## Git reset and revert

Well, not all my changes is correct. So I need a way to reset or revert my changes.

+ reset: changes are not pushed to remote.
+ revert: changes have been pushed to remote.

### git reset commit-to-reset-to:

+ This will reset my repository to the specified commit and leave all the changes in the
working directory. If you want to drop changes to specific file after reset,
use `git checkout -- file-name`
    + If you want to clean everything, be carefull with this option:
    + git reset --hard commit-to-reset-to

### git revert commit-to-revert-to:

+ This will add a new commit: revert commit after HEAD.

---

layout: false

## Other useful commands

### Forcely overwrite remotes:(Be carefull)

+ git push -f origin branch-name

### Squash commits (combine commits)

If you have commit three times, and you want to merge them.

+ HEAD(place where you start your work)
+ commit-hash-1
+ commit-hash-2
+ commit-hash-3

Execute:

+ git rebase -i HEAD(or any commit)

Then:, pick(leave commit), squash(drop the commit)

---

template: inverse

## Thanks

