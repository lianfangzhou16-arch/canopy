import os
import json
import asyncio
import signal
import logging
import argparse
from typing import List, Dict
from dotenv import load_dotenv
from colorama import init, Fore, Style
from web3 import AsyncWeb3
from web3.providers import AsyncHTTPProvider
from eth_account import Account

init(autoreset=True)

class Web3Formatter(logging.Formatter):
    def format(self, record):
        if record.levelno >= logging.ERROR:
            prefix = f"{Fore.RED}[🔥] {Style.BRIGHT}"
        elif record.levelno >= logging.WARNING:
            prefix = f"{Fore.YELLOW}[⚠️] {Style.NORMAL}"
        else:
            prefix = f"{Fore.GREEN}[✅] {Style.NORMAL}"
        return f"{prefix}{record.getMessage()}{Style.RESET_ALL}"

logger = logging.getLogger("CommandCenter")
logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
sh.setFormatter(Web3Formatter())
logger.addHandler(sh)

class CommandCenter:
    def __init__(self, mode: str):
        load_dotenv()
        self.mode = mode
        self.is_running = True
        self.rpc_url = os.getenv("RPC_URL", "https://testnet.rpc.neuraprotocol.io/")
        self.semaphore = asyncio.Semaphore(int(os.getenv("MAX_CONCURRENT_REQUESTS", 5)))
        self.wallets = self._load_wallets()

    def _load_wallets(self) -> List[Dict]:
        """
        Iron Law: Environment Isolation
        Configuration must be driven by os.getenv()
        """
        wallet_path = os.getenv("WALLETS_JSON_PATH")
        if wallet_path and os.path.exists(wallet_path):
            with open(wallet_path, 'r') as f:
                return json.load(f)

        pk = os.getenv("PRIVATE_KEY")
        if pk and pk != "your_private_key_here":
            return [{"private_key": pk, "proxy": os.getenv("GLOBAL_PROXY"), "note": "Default"}]

        return []

    async def monitor_wallet(self, wallet_info: Dict):
        pk = wallet_info['private_key']
        proxy = wallet_info.get('proxy')
        note = wallet_info.get('note', 'Unknown')

        request_kwargs = {'proxy': proxy} if proxy else {}
        w3 = AsyncWeb3(AsyncHTTPProvider(self.rpc_url, request_kwargs=request_kwargs))
        account = Account.from_key(pk)

        attempt = 0
        while self.is_running:
            try:
                async with self.semaphore:
                    # Deterministic Output: Combined block and balance check
                    block = await w3.eth.block_number
                    balance_wei = await w3.eth.get_balance(account.address)
                    balance_eth = w3.from_wei(balance_wei, 'ether')

                    logger.info(f"[{note}] {account.address[:8]}... | Block: {block} | Balance: {balance_eth:.4f} | Mode: {self.mode}")

                attempt = 0 # Reset on success
                await asyncio.sleep(15)

            except Exception as e:
                logger.error(f"[{note}] Network Error: {str(e)}")
                attempt += 1
                # Network Robustness: Exponential backoff
                wait_time = min(2 ** attempt, 60)
                logger.info(f"[{note}] Exponential backoff: waiting {wait_time}s...")
                await asyncio.sleep(wait_time)

    async def run(self):
        logger.info(f"Command Center Live | Accounts: {len(self.wallets)}")

        loop = asyncio.get_running_loop()
        for s in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(s, lambda: asyncio.create_task(self.shutdown()))

        tasks = [self.monitor_wallet(w) for w in self.wallets]
        if not tasks:
            logger.error("No active wallets to monitor. Check .env or configs/wallets.json")
            return

        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            pass
        finally:
            logger.info("Command Center offline. Zero-Failure Execution maintained.")

    async def shutdown(self):
        logger.warning("Shutdown received. Closing all circuits...")
        self.is_running = False
        for task in asyncio.all_tasks():
            if task is not asyncio.current_task():
                task.cancel()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="development")
    args = parser.parse_args()

    center = CommandCenter(mode=args.mode)
    try:
        asyncio.run(center.run())
    except KeyboardInterrupt:
        pass
