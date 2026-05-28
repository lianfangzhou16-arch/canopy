# Running a Neura Protocol Node (Canopy Implementation)

Neura is a sovereign Layer-1 blockchain built on the **Canopy Stack**. This guide explains how to run a Neura node using the official implementation in this repository.

## 🚀 Quick Start (Docker)

The fastest way to get a Neura-compatible node running is via Docker:

```bash
# Build the Canopy images
make docker/build

# Start the node (Testnet configuration)
make docker/up

# View live logs
make docker/logs
```

## 🛠️ Native Build (Linux/macOS)

For production environments or local development:

```bash
# 1. Build the full suite (canopy, wallet, explorer)
make build/canopy-full

# 2. Initialize the data directory
# This will create config.json and genesis.json
canopy start --data-dir ./data/neura_node
```

## ⚙️ Configuration for Neura Testnet

Ensure your `config.json` in the data directory matches the Neura Testnet parameters:

- **Chain ID**: 267
- **Network ID**: 1
- **RPC URL**: `https://testnet.rpc.neuraprotocol.io/`

## 📊 Monitoring

Use the provided **Web3 Quant Command Center** to monitor your node and wallet:

```bash
# 1. Align dependencies
pip install -r requirements.txt

# 2. Set up environment
cp .env.example .env
# Edit .env with your Private Key and RPC URL

# 3. Check Wallet Balance (Pre-flight logic)
python tools/wallet_check.py

# 4. Start Command Center
python main.py --mode production
```

## 🛡️ Web3 Iron Laws (Node Operator)

- **Isolation**: Always use `.env` for keys. Never commit your data directory.
- **Robustness**: The Command Center automatically handles RPC timeouts and node restarts.
- **Balance**: Ensure your validator has sufficient **ANKR** (Testnet gas token) for signing proposals.
