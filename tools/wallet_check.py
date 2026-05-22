import os
import json
import asyncio
import logging
from typing import List, Dict
from decimal import Decimal
from dotenv import load_dotenv
from web3 import AsyncWeb3
from web3.providers import AsyncHTTPProvider
from web3.exceptions import Web3Exception
from eth_account import Account
from colorama import init, Fore, Style

# Initialize colorama
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

logger = logging.getLogger("WalletCheck")
logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
sh.setFormatter(Web3Formatter())
logger.addHandler(sh)

class WalletMonitor:
    def __init__(self):
        load_dotenv()
        self.rpc_url = os.getenv("RPC_URL", "https://testnet.rpc.neuraprotocol.io/")
        self.semaphore = asyncio.Semaphore(int(os.getenv("MAX_CONCURRENT_REQUESTS", 5)))
        self.wallets = self._load_wallets()

    def _load_wallets(self) -> List[Dict]:
        """
        Iron Law: Environment Isolation
        Mandatory use of .env via os.getenv.
        """
        # Priority 1: Multi-wallet JSON path from .env
        wallet_path = os.getenv("WALLETS_JSON_PATH")
        if wallet_path and os.path.exists(wallet_path):
            with open(wallet_path, 'r') as f:
                return json.load(f)

        # Priority 2: Single private key fallback from .env
        pk = os.getenv("PRIVATE_KEY")
        if pk and pk != "your_private_key_here":
            return [{"private_key": pk, "proxy": os.getenv("GLOBAL_PROXY"), "note": "Default"}]

        logger.warning("No configuration found in os.getenv('WALLETS_JSON_PATH') or os.getenv('PRIVATE_KEY')")
        return []

    async def check_wallet(self, wallet_info: Dict):
        pk = wallet_info['private_key']
        proxy = wallet_info.get('proxy')
        note = wallet_info.get('note', 'Unknown')
        rpc_url = wallet_info.get('rpc_url', self.rpc_url)

        # Setup provider with proxy if exists
        request_kwargs = {}
        if proxy:
            request_kwargs['proxy'] = proxy

        w3 = AsyncWeb3(AsyncHTTPProvider(rpc_url, request_kwargs=request_kwargs))

        try:
            async with self.semaphore:
                account = Account.from_key(pk)
                balance_wei = await w3.eth.get_balance(account.address)
                balance_eth = w3.from_wei(balance_wei, 'ether')

                status = "PASSED" if balance_wei > 0 else "EMPTY"
                color = Fore.GREEN if balance_wei > 0 else Fore.YELLOW

                logger.info(f"[{note}] {account.address} | Balance: {balance_eth} | Proxy: {proxy or 'Direct'}")

        except Exception as e:
            logger.error(f"[{note}] Failed: {str(e)}")

    async def run_all(self):
        if not self.wallets:
            logger.error("No wallets found in configs/wallets.json or .env")
            return

        tasks = [self.check_wallet(w) for w in self.wallets]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    monitor = WalletMonitor()
    asyncio.run(monitor.run_all())
