# 🚀 Neura 指挥中心：首席架构师级运行指南

您指出的非常对！在顶级工程实践中，**Environment Isolation (环境隔离)** 是铁律。我们不应该仅仅依赖于文件的存在，而是应该通过环境变量来“指挥”系统。

## 1. 核心运行逻辑 (大白话)

整个系统的运作是由 **`.env`** 文件驱动的。它就像是飞机的仪表盘，告诉机器人去哪里读密钥、用哪个 IP。

### 第一步：创建你的“仪表盘” (.env)
1.  找到 `.env.example`，复制一份并改名为 **`.env`**。
2.  打开 `.env` 文件，你会看到两个选项：

#### 选项 A：只跑一个号 (快速测试)
在 `PRIVATE_KEY=` 后面填入你的私钥。

#### 选项 B：跑多个号 + IP 代理 (专业量化)
1.  确保 `WALLETS_JSON_PATH=configs/wallets.json` 这行没改。
2.  去 `configs/` 文件夹，把 `wallets.json.example` 改名为 `wallets.json`。
3.  在 `wallets.json` 里填入所有的私钥和对应的代理。

---

## 2. 详细操作流程

### 1. 准备环境
```bash
pip install -r requirements.txt
```

### 2. 余额预检 (强制性流程)
在正式运行前，必须通过环境变量驱动的脚本检查所有钱包：
```bash
python tools/wallet_check.py
```
*   **逻辑**：系统会先看 `.env` 里的 `WALLETS_JSON_PATH` 指向的文件；如果文件不存在，才会去读 `PRIVATE_KEY`。

### 3. 启动实盘
```bash
python main.py --mode production
```

---

## 3. 关于“IP 代理”怎么创建？

如果你在 `wallets.json` 里填了代理：
*   **格式**：`"proxy": "http://用户名:密码@IP:端口"`
*   **如果不填**：系统会自动使用 `.env` 里的 `GLOBAL_PROXY`（如果有的话），或者直接用你本机的网络。

---

## 🛡️ Web3 铁律：为什么这么麻烦？

1.  **环境隔离**：所有的配置都应该通过 `os.getenv` 读取。这样当你把代码部署到不同的服务器（比如阿里云、AWS）时，只需要改 `.env`，而不需要改代码。
2.  **安全性**：`.gitignore` 已经帮你把 `.env` 和 `wallets.json` 排除在外了。只要你遵守这个规范，你的私钥就永远不会意外上传到网上。
3.  **确定性**：程序在启动时会打印 `[✅] Connected to RPC: ...`。如果没有这个反馈，说明环境变量没配对。

**首席工程师提示**：您现在的操作是正确的，先配 `.env` 仪表盘，再通过它去索引具体的钱包清单。祝实盘大赚！
