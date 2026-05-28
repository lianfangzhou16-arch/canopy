# Konnex Node & Faucet Operations Guide

This guide explains how to run a node for the Konnex Protocol (built on the Canopy Stack) and how to interact with the Faucet to receive test tokens.

## 1. Prerequisites
- **Go**: Version 1.22+ (for building the Canopy node)
- **Python**: Version 3.10+ (for the plugin and SDK)
- **Docker**: Optional, for containerized execution.

## 2. Building the Node
Compile the official implementation of the Canopy Network Protocol:
```bash
make build/canopy-full
```
This installs the `canopy` binary to `~/go/bin/canopy`.

## 3. Initializing the Node
Run the node to generate the default data directory and configuration:
```bash
~/go/bin/canopy start
# Press Ctrl+C once you see "Creating config.json file"
```
The data will be stored in `~/.canopy/`.

## 4. Configuring for Konnex Testnet
Edit `~/.canopy/config.json` to match the Konnex/Neura parameters:
- **Chain ID**: 267 (Neura Testnet)
- **Network ID**: 1
- **Plugin**: "python" (To enable custom transaction types like Faucet)

## 5. Setting up the Python Plugin (Faucet Support)
Konnex utilizes a Python-based FSM extension for its subnets. To enable the Faucet functionality:
```bash
cd plugin/python
make dev
```

## 6. Daily Faucet & Transaction Testing
The Faucet allows you to claim test tokens daily. You can use the provided Python SDK to interact with it.

### Claiming via RPC Test Script
We have verified the faucet flow using the tutorial test suite:
```bash
cd plugin/python/tutorial
pip install -r requirements.txt
python rpc_test.py
```
This script will:
1. Create two temporary accounts.
2. Request tokens from the **Faucet**.
3. Perform a **Send** transaction.
4. Perform a **Reward** transaction (minting).

## 7. Protocol Parameters Summary
- **Official Docs**: [https://docs.konnex.world/](https://docs.konnex.world/)
- **Python SDK Docs**: [https://docs.konnex.world/sdk/python](https://docs.konnex.world/sdk/python)
- **Explorer**: [https://subnets.testnet.konnex.world/explorer](https://subnets.testnet.konnex.world/explorer)
- **Faucet URL**: [https://subnets.testnet.konnex.world/faucet](https://subnets.testnet.konnex.world/faucet)

## 8. Hardware Recommendations
- **CPU**: 4+ Cores
- **RAM**: 8GB+
- **Storage**: 500GB+ SSD (Recommended for full sync)
