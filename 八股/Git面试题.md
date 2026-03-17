---
title: "Git面试题"
source: "https://xiaolincoding.com/interview/git.html#git-%E4%BD%BF%E7%94%A8%E7%86%9F%E7%BB%83%E5%90%97"
author:
  - "[[小林coding]]"
published: undefined
created: 2025-09-18
description: "全面的Git版本控制面试题汇总，涵盖Git核心概念、常用命令、分支管理策略、合并冲突解决、Git工作流程(GitFlow/GitLab Flow)、Git底层原理、远程仓库操作、标签管理、代码托管平台(GitHub/GitLab)、团队协作开发、版本回退、暂存区管理等核心知识点。深入解析Git工作机制，适合开发者面试准备和团队协作学习。"
tags:
  - "clippings"
---
## Git 面试题

[![](https://cdn.xiaolincoding.com/mianshiya.png)](https://mianshiya.com/?shareCode=xeu1wi)

## Git 使用熟练吗？

熟悉，项目的代码是用 git 工具来管理的/

git 的工作原理如下图：

![image-20250320161914470](https://cdn.xiaolincoding.com//picgo/image-20250320161914470.png)

几个专用名词的译名如下：

- Workspace：工作区
- Index / Stage：暂存区
- Repository：仓库区（或本地仓库）
- Remote：远程仓库

> 工作流程

最基础的工作流程，首先执行 `git pull` 获取远程仓库的最新代码，进行代码的编写。

完成相应功能的开发后执行 `git add .` 将工作区代码的修改添加到暂存区，再执行 `git commit -m 完成xx功能` 将暂存区代码提交到本地仓库并添加相应的注释，最后执行 `git push` 命令推送到远程仓库。

> 撤回 git commit 操作

当执行了 `git commit -m 注释内容` 命令想要撤回，可以使用 `git reset --soft HEAD^` 把本地仓库回退到当前版本的上一个版本，也就是刚刚还没提交的时候，代码的改动会保留在暂存区和工作区。

也可以使用 `git reset --mixed HEAD^` ，这样不止回退了刚刚的 `git commit` 操作，还回退了 `git add` 操作，代码的改动只会保留在工作区。因为 `--mixed` 参数是 `git reset` 命令的默认选项，也就是可以写为 `git reset HEAD^` 。

> 撤回 git push 操作

当执行了 `git push` 命令想要撤回，可以使用 `git reset HEAD^` 将本地仓库回退到当前版本的上一个版本，代码的修改会保留在工作区，然后使用 `git push origin xxx --force` 将本地仓库当前版本的代码强制推送到远程仓库。

## git rebase和merge的区别

- **Rebase** （变基）是将一个分支上的提交逐个地应用到另一个分支上，使得提交历史变得更加线性。当执行rebase时，Git会将目标分支与源分支的共同祖先以来的所有提交挪到目标分支的最新位置。这个过程可以看作是将源分支上的每个提交复制到目标分支上。简而言之，rebase可以将提交按照时间顺序线性排列。
- **Merge** （合并）是将两个分支上的代码提交历史合并为一个新的提交。在执行merge时，Git会创建一个新的合并提交，将两个分支的提交历史连接在一起。这样，两个分支的修改都会包含在一个合并提交中。合并后的历史会保留每个分支的提交记录。

## 如何使用 git 命令合并两个分支，发生冲突如何解决

1. **查看冲突** ：当发生冲突时，Git 会提示您文件中的冲突部分。您可以使用以下命令查看所有冲突文件的状态。
```bash
git status
```
1. **解决冲突** ：打开包含冲突的文件，您会看到类似以下的标记：
```
<<<<<<< HEAD
// 代码来自目标分支
=======
// 代码来自要合并的分支
>>>>>>> branchName
```

您需要手动编辑这些文件，决定保留哪些变更或者如何整合这些变更。

1. **标记为已解决** ：完成冲突解决后，对已解决的文件使用以下命令标记为已解决。
```bash
git add <已解决文件>
```
1. **完成合并** ：继续提交这些已解决的冲突文件。
```bash
git commit -m "解决合并冲突"
```

## 推荐学习

- [摸清 Git 的门路，就靠这 22 张图 (opens new window)](https://mp.weixin.qq.com/s/ONRUG0_pb_ULdtItS_tfSA)

---

[![](https://cdn.xiaolincoding.com/mianshiya.png)](https://mianshiya.com/?shareCode=xeu1wi)

最新的图解文章都在公众号首发，别忘记关注哦！！如果你想加入百人技术交流群，扫码下方二维码回复「加群」。

![img](https://cdn.xiaolincoding.com/gh/xiaolincoder/ImageHost3@main/%E5%85%B6%E4%BB%96/%E5%85%AC%E4%BC%97%E5%8F%B7%E4%BB%8B%E7%BB%8D.png)

阅读全文

登录后查看评论