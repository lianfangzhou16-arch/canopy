import os
import asyncio
import logging
from typing import Optional
from decimal import Decimal
from dotenv import load_dotenv
from web3 import AsyncWeb3
from web3.providers import AsyncHTTPProvider
from web3.exceptions import Web3Exception
from eth_account import Account
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# --- Configuration & Philosophy ---
# Log Art: [✅] (Success), [⚠️] (Risk/Skip), [🔥] (Fatal/Stop)
class Web3Formatter(logging.Formatter):
    def format(self, record):
        if record.levelno >= logging.ERROR:
            prefix = f"{Fore.RED}[🔥] {Style.BRIGHT}"
        elif record.levelno >= logging.WARNING:
            prefix = f"{Fore.YELLOW}[⚠️] {Style.NORMAL}"
        else:
            prefix = f"{Fore.GREEN}[✅] {Style.NORMAL}"
        return f"{prefix}{record.getMessage()}{Style.RESET_ALL}"

logger = logging.getLogger("Web3Quant")
logger.setLevel(logging.INFO)

# Stream Handler (Colored)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(Web3Formatter())
logger.addHandler(stream_handler)

# File Handler (Persistent logs)
os.makedirs("logs", exist_ok=True)
file_handler = logging.FileHandler("logs/wallet_check.log")
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# --- Web3 Iron Laws Implementation ---

class WalletMonitor:
    def __init__(self):
        load_dotenv()
        self.rpc_url = os.getenv("RPC_URL", "https://testnet.rpc.neuraprotocol.io/")
        self.private_key = os.getenv("PRIVATE_KEY")
        self.w3 = AsyncWeb3(AsyncHTTPProvider(self.rpc_url))
        self.semaphore = asyncio.Semaphore(int(os.getenv("MAX_CONCURRENT_REQUESTS", 5)))

    def pre_flight_check(self, balance_wei: int, required_wei: int, fee_wei: int, margin_wei: int) -> bool:
        """
        Iron Law: Pre-flight Balance Check
        current_balance > (required_amount + priority_fee + safety_margin)
        """
        total_needed = required_wei + fee_wei + margin_wei
        return balance_wei > total_needed

    async def get_balance(self, address: str) -> int:
        async with self.semaphore:
            return await self.w3.eth.get_balance(address)

    async def check_wallet(self, required_amount_eth: float = 0.0):
        if not self.private_key or self.private_key == "your_private_key_here":
            logger.error("Environment Isolation Violation: Private key not found in .env")
            return

        try:
            account = Account.from_key(self.private_key)
            address = account.address
            logger.info(f"Checking Wallet: {address}")

            balance_wei = await self.get_balance(address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')

            logger.info(f"Current Balance: {balance_eth} {os.getenv('SYMBOL', 'ANKR')}")

            # Define margins and fees
            margin_eth = Decimal(os.getenv("SAFETY_MARGIN_ETH", "0.01"))
            fee_gwei = Decimal(os.getenv("PRIORITY_FEE_GWEI", "1.5"))
            # Estimated gas for simple transfer (21000)
            estimated_fee_wei = self.w3.to_wei(fee_gwei, 'gwei') * 21000

            required_wei = self.w3.to_wei(Decimal(str(required_amount_eth)), 'ether')
            margin_wei = self.w3.to_wei(margin_eth, 'ether')

            if self.pre_flight_check(balance_wei, int(required_wei), int(estimated_fee_wei), int(margin_wei)):
                logger.info("Pre-flight Balance Check PASSED")
            else:
                logger.warning(f"Pre-flight Balance Check FAILED: Insufficient funds for safe execution.")
                logger.warning(f"Needed (incl. margin): {self.w3.from_wei(int(required_wei + estimated_fee_wei + margin_wei), 'ether')} ETH")

        except Web3Exception as e:
            logger.error(f"Network Robustness Error: {str(e)}")
        except Exception as e:
            logger.error(f"Fatal Execution Error: {str(e)}")

async def main():
    monitor = WalletMonitor()
    await monitor.check_wallet()

if __name__ == "__main__":
    asyncio.run(main())
