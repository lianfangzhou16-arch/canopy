# 小白也要跑节点：Konnex 节点极简上手指南 🚀

如果你只有一台电脑，完全不懂编程，跟着下面这几步走，就能把节点跑起来。

### 第一步：准备工具（像装游戏一样简单）
你需要安装两个“基础软件”，如果还没装，去官网下载安装就行：
1. **Docker Desktop** (必备)：它是运行节点的“集装箱”。[官网下载](https://www.docker.com/products/docker-desktop/)
2. **Python**: 领测试币用的工具。[官网下载](https://www.python.org/downloads/)

---

### 第二步：把代码搬回家
1. 打开你电脑上的 **终端**（Windows 叫 PowerShell 或 CMD，Mac 叫 Terminal）。
2. 输入下面这行命令（把代码下载下来）：
   ```bash
   git clone https://github.com/canopy-network/canopy.git
   cd canopy
   ```

---

### 第三步：一键启动节点 (最省事的方法)
我们使用 Docker 来运行，这样你不需要自己配置复杂的运行环境。
1. 在终端里输入（这会自动下载并启动一切）：
   ```bash
   make docker/plugin PLUGIN=python
   make docker/run-python
   ```
2. **怎么看成功了没？**
   如果你看到屏幕上开始滚动一些蓝绿色的字，或者出现 `Committed block...`，恭喜你，你的节点已经开始工作了！

---

### 第四步：领取每日测试币 (领水)
官方提供了两种领水方式：
1. **手动领（最快）：**
   访问 [Konnex 领水官网](https://subnets.testnet.konnex.world/faucet)，填入你的地址点领取。
2. **用咱们的工具领：**
   在终端运行：
   ```bash
   cd plugin/python/tutorial
   pip install -r requirements.txt
   python rpc_test.py
   ```
   这个脚本会自动帮你创建账号、领测试币、然后测试能不能转账。

---

### 常见问题 (FAQ)
*   **节点要一直开着吗？** 是的，如果你想赚取积分或参与测试，建议保持电脑联网并开启 Docker。
*   **我怎么看我的余额？**
    你可以访问 [Konnex 浏览器](https://subnets.testnet.konnex.world/explorer)，输入你的地址查询。
*   **报错了怎么办？**
    确保你的 Docker 已经打开，且网络通畅。

---

### 🌟 进阶：如果你已经在跑其他节点 (多节点共存)
如果你电脑里已经有一个 Canopy 节点在跑，为了不搞混，请使用我为你专门设计的“隔离模式”启动：
```bash
docker compose -f .docker/docker-compose.konnex.yaml -p konnex up -d
```
这样，你的 Konnex 节点会跑在 **60002** 端口，而原有节点继续在 **50002** 端口，互不干扰，完美共存！具体原理请看 `KONNEX_ISOLATION_GUIDE.md`。

**大功告成！你现在已经是 Konnex 网络的一员了。**
