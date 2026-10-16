# M0-1 开发环境搭建记录

## 环境信息

- 系统：Ubuntu 22.04.5 LTS，运行在虚拟机中
- ROS 2：Humble
  - 使用 `source /opt/ros/humble/setup.bash` 加载环境
  - `echo $ROS_DISTRO` 输出 `humble`
  - `ros2 --help` 能显示帮助信息
- Python：3.10.12
- Python 环境工具：uv 0.13.0
  - 在 `~/smartcar-practice` 中创建 `.venv`
  - VS Code 运行脚本时使用 `/home/yan/smartcar-practice/.venv/bin/python`
- C/C++ 工具：gcc/g++ 11.4.0、make 4.3、cmake 3.22.1
- Git：2.34.1，已配置 `user.name` 和 `user.email`
- 编辑器：Visual Studio Code
  - 已安装 Microsoft Python、C/C++、Remote - SSH 扩展
- SSH：已安装并启动 OpenSSH 服务端；通过 `ssh yan@localhost` 成功登录，使用 `scp` 成功传输文件，并完成 SSH 密钥登录练习

## 搭建与检查过程

1. 在 Ubuntu 中安装 uv，并用 `uv venv --python 3.10` 创建 Python 虚拟环境。
2. 在 VS Code 中打开项目文件夹，选择 `.venv` 解释器；运行 `hello.py`，确认解释器路径位于 `.venv/bin/python`。
3. 检查 ROS 2 Humble、gcc、g++、make、cmake 和 Git 是否可用。
4. 安装 VS Code 的 Python、C/C++ 和 Remote - SSH 扩展，并选择 g++ 编译器。
5. 安装并启动 OpenSSH 服务端，练习 SSH 登录、scp 传文件和密钥登录。

## 本机踩坑记录

- Firefox 显示“代理服务器拒绝连接”，但 Ubuntu 终端中 `ping -c 4 1.1.1.1` 和 `ping -c 4 ubuntu.com` 均收到回复。由此确认基础网络和域名解析可用；浏览器的代理设置仍需按实际需要单独配置。(之前已经把代理的端口配置好了，这次不知道为什么不能用，直接关闭代理就能正常上外网。)
- VS Code 集成终端运行 `sudo apt install openssh-server` 时提示 `no new privileges`。改在 Ubuntu 系统终端安装后，SSH 服务状态显示 `active (running)`。
- ROS 环境变量按终端会话加载。在一个终端中执行 `source /opt/ros/humble/setup.bash` 后，`ROS_DISTRO` 显示 `humble`；新终端需要再次加载。
- VS Code 曾多创建一个 `.venv-1`。项目应使用最初由 uv 创建的 `.venv`，Python 文件放在项目目录中，不放进虚拟环境目录。
- 中文输入法：系统右上角显示 `ZH`，设置里的输入源也有“汉语”，但输入拼音仍只显示英文。检查后发现，汉语输入源可能只是键盘布局，不一定包含拼音输入引擎。
- 输入检查脚本发现pip不可用，已严肃安装
- 刚刚因为磁盘空间不足导致无法更改代理http的IP，以及登录后无法生成图形登录界面，经过扩容然后分区解决
