# 12. 工作区与隔离策略规格

## 1. 目标

不同 agent 不能默认拥有相同的文件系统权限。产品必须允许根据角色与场景控制工作区隔离。

## 2. 隔离模式

Python 版建议至少定义：

### 2.1 shared workspace
主线程默认工作区，共享项目目录。

### 2.2 read-only workspace
用于探索、规划、验证等只读角色。

### 2.3 temp workspace
用于临时脚本、临时测试产物。

### 2.4 worktree workspace
用于隔离修改型子任务，避免污染主分支。

### 2.5 remote workspace
用于远程执行环境（第一版可不做）。

## 3. 为什么隔离必须存在

没有隔离会导致：
- 子任务互相污染
- 验证角色破坏项目
- fork 实验影响主线程
- 风险动作边界模糊

## 4. 角色与隔离建议

- Explore Agent -> read-only
- Plan Agent -> read-only
- Verification Agent -> read-only + temp writable
- General Agent -> shared 或 worktree
- 高风险实现任务 -> worktree

## 5. 路径翻译需求

如果子任务运行在 worktree 中，而继承的上下文引用的是父工作区路径，系统需要能做路径翻译或重新读取。

## 6. 清理需求

隔离工作区结束后必须支持：
- 清理临时文件
- 清理临时目录
- 清理 worktree（如适用）
- 清理孤儿进程

## 7. 验收标准

1. 只读角色不能修改项目文件
2. 验证角色只能在 temp 目录写测试脚本
3. worktree 任务不污染主项目目录
4. 任务结束后能清理隔离资源
