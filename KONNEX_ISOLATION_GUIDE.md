# 如何在同一台电脑上运行多个节点而不混淆？

如果你已经在跑 Canopy 节点，现在又想跑 Konnex 节点，最担心的就是“端口冲突”和“数据覆盖”。作为顶级 AI，我为你设计了一套 **“平行宇宙” (Isolation)** 方案。

### 核心原理：命名空间 (Namespace) 隔离

通过 Docker 的 `Project Name` 和 `Custom Ports` 功能，我们可以让两个节点像跑在两台独立电脑上一样。

---

### 第一步：使用隔离的配置文件
我为你准备了一个专门的 `.docker/docker-compose.konnex.yaml`。它已经把端口改成了 `60000` 系列，不会和你原有的 `50000` 系列冲突。

### 第二步：一键启动隔离节点
在终端输入这行命令（关键是 `-p konnex`）：
```bash
docker compose -f .docker/docker-compose.konnex.yaml -p konnex up -d
```
*   `-f`: 指定使用 Konnex 专用配置。
*   `-p konnex`: 给这个项目起个名字叫 `konnex`，这样它的镜像、网络、容器都会带上 `konnex` 前缀，绝不会和原有节点搞混。

### 第三步：如何区分和查看？

| 功能 | 原有 Canopy 节点 | **新 Konnex 节点** |
| :--- | :--- | :--- |
| **RPC 端口** | 50002 | **60002** |
| **浏览器地址** | http://localhost:50001 | **http://localhost:60001** |
| **钱包地址** | http://localhost:50000 | **http://localhost:60000** |
| **查看日志** | `docker logs node-1` | **`docker logs konnex-node`** |

---

### 顶级 AI 的深度建议：

1.  **数据存放：** Konnex 的数据会自动存放在 `./.docker/volumes/konnex_node` 文件夹下。你可以放心删除或备份这个文件夹，而不影响原有节点。
2.  **资源限制：** 如果你的电脑内存紧张（小于 16GB），建议在两个节点同时跑时，监控一下 CPU 占用。
3.  **独立代理：** 如果你想更彻底地防止项目方关联 IP，可以在 Konnex 的 Docker 配置中加入 `PROXY` 环境变量（如果你有代理服务器的话）。

**现在，你的两个节点已经在互不干扰的“平行宇宙”里运行了！**
