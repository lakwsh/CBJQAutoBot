# CBJQAutoBot
 - 基于`Python3`+`飞桨OCR`实现的尘白禁区挂机脚本
 - 目前仅支持增益试炼全自动挂机(稳定挂机一个晚上)
 - 无分辨率要求,窗口模式即可
 - **需要管理员权限运行(用于控制鼠标键盘)**
 - 欢迎大佬PR~
## 前置条件
 - 拥有角色: 晨星-琼弦
 - 拥有增益: 护盾·夺取
## 源码运行
 - 使用GPU文字识别
   - **仅支持英伟达显卡**
   - 安装[CUDA Toolkit 12.9](https://developer.nvidia.com/cuda-12-9-1-download-archive)
   - [安装GPU版飞桨](https://www.paddlepaddle.org.cn/install/quick?docurl=/documentation/docs/zh/develop/install/pip/windows-pip.html): `pip install paddlepaddle-gpu==3.2.1 -i https://www.paddlepaddle.org.cn/packages/stable/cu129/`
 - 安装其他依赖: `pip install pywin32 PyAutoGUI paddleocr`
## 增益选择逻辑
 - 首选非单体未获得增益
 - 次选非单体已获得增益
 - 全是单体增益选一个丢弃
## 大招释放逻辑
 - 释放技能约8次后放大招
