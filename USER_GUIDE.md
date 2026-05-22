# 🚀 Neura 顶级多节点指挥部：Windows 实战指南

您提出的 **多节点 + 独立代理** 方案是 Web3 大户（Whale）的标准配置。这种架构实现了物理级别的隔离，确保账号 A 的任何波动都不会影响账号 B。

---

## 1. 准备工作 (Windows PowerShell)

在启动 Docker 之前，我们需要在 D 盘创建好对应的数据文件夹。请以管理员身份打开 **PowerShell**，运行以下命令：

```powershell
# 一键创建所有节点目录
New-Item -ItemType Directory -Force -Path "D:\neura_evm_nodes\node_1"
New-Item -ItemType Directory -Force -Path "D:\neura_evm_nodes\node_2"
New-Item -ItemType Directory -Force -Path "D:\neura_evm_nodes\node_3"
New-Item -ItemType Directory -Force -Path "D:\neura_evm_nodes\docker"
```

---

## 2. 核心架构：1 对 1 绑定模式

在我的重构下，系统现在支持 **“1 个钱包 -> 1 个独立节点 -> 1 个独立代理 IP”** 的完美闭环。

### 配置步骤：
1.  **编辑 `.env`**：设置基础环境。
2.  **编辑 `configs/wallets.json`**：为每个号分配节点地址。
    *   账号 1 连本地节点 1：`"rpc_url": "http://localhost:50002"`
    *   账号 2 连本地节点 2：`"rpc_url": "http://localhost:40002"`
    *   账号 3 连本地节点 3：`"rpc_url": "http://localhost:30002"`
3.  **编辑 `docker-compose.yaml`**：
    *   我已经为您写好了模板。请在 `neura-node-2` 和 `neura-node-3` 的 `environment` 部分，填入您购买的静态 IP 代理信息。

---

## 3. 一键启动全家桶

在项目根目录下运行：
```bash
make docker/up
```

### 运行后您的电脑将呈现以下状态：
*   **Docker 内部**：3 个 Neura 节点同时同步，其中 2 个通过代理 IP 出口。
*   **Python 机器人**：1 个机器人同时开启 3 个线程，分别对应 3 个节点进行监控。
*   **日志展示**：
    ```text
    [账号1] 0x123... | Block: 9441724 | Balance: 10.5 | Node: 50002 (直连)
    [账号2] 0x456... | Block: 9441724 | Balance: 88.2 | Node: 40002 (代理A)
    [账号3] 0x789... | Block: 9441724 | Balance: 5.1  | Node: 30002 (代理B)
    ```

---

## 🛡️ 首席架构师的深度建议

1.  **磁盘空间**：由于跑了 3 个节点，请确保 D 盘有足够的空间（建议 500GB 以上 SSD）。
2.  **内存占用**：3 个节点约占用 6-8GB 内存。如果电脑配置不够，可以先注释掉 `node-3`。
3.  **代理稳定性**：静态 IP 代理如果断开，对应的节点会停止同步。机器人的 **指数退避重试** 机制会不断尝试重连，直到代理恢复。

**这套方案让您的操作完全不可被项目方关联。现在，请执行 PowerShell 命令创建文件夹并开启您的多节点帝国吧！**
