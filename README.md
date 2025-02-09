# CBJQAutoBot
 - 尘白懒人脚本
 - 目前仅支持增益试炼全自动挂机
 - 无分辨率要求,窗口模式即可
 - **需要管理员权限运行(用于控制鼠标键盘)**
 - 欢迎大佬PR
## 前置条件
 - 拥有角色: 晨星-琼弦
 - 拥有增益: 护盾·夺取
## 运行环境要求
 - 英伟达显卡
 - [CUDA Toolkit 12.3](https://developer.nvidia.com/cuda-12-3-0-download-archive)
## 源码运行
 - 安装python3
 - [安装GPU版飞桨](https://www.paddlepaddle.org.cn/install/quick?docurl=/documentation/docs/zh/develop/install/pip/windows-pip.html): pip install paddlepaddle-gpu==3.0.0rc1 -i https://www.paddlepaddle.org.cn/packages/stable/cu123/
 - 安装其他依赖: pip install pywin32 PyAutoGUI pillow paddleocr numpy
## 增益选择逻辑
 - 首选非单体未获得增益
 - 次选非单体已获得增益
 - 全是单体增益选一个丢弃
## 大招释放逻辑
 - 释放技能约8次后放大招
