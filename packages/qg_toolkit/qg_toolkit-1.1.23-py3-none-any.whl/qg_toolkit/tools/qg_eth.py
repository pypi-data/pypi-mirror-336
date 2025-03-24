import base64
import binascii
import inspect
import json
import random
from decimal import Decimal
from pathlib import Path

import requests
from eth_account import Account
from eth_account.messages import encode_defunct, encode_typed_data
from retry import retry
from web3 import Web3
from web3.auto import w3

from qg_toolkit.tools.qg_log import logger

from qg_toolkit.tools.qg_file import QGFile
from qg_toolkit.tools.rpc import endpoints, apis, bases


class QGEth:
    def __init__(self, index, address=None, private_key=None, mnemonic=None, chain_instances=None, endpoint=None, show_log=False):
        self.index = index
        self.address = address
        self.private_key = private_key
        self.mnemonic = mnemonic
        self.chain_instances = chain_instances or {}
        self.show_log = show_log
        self.endpoints = endpoint or endpoints
        if self.address is None:
            self.address = Account.from_key(private_key).address

    @retry(tries=2, delay=1, backoff=1, max_delay=3)
    def init_chains(self, *chain_names):
        try:
            for name in chain_names:
                web3 = getattr(self, f"{name}_w3", None)
                if web3 is None:
                    self.add_chain(name)
                    self.add_balance(name)
            chains_info = []
            for chain_name, web3_instance in self.chain_instances.items():
                chains_info.append(f"{chain_name}余额:{self.get_balance_by_chain(chain_name)}")
            logger.info(f"【{self.address}】【{self.index}】余额情况 {','.join(chains_info)}")
        except Exception as e:
            raise Exception("初始化失败！")

    @retry(tries=2, delay=1, backoff=1, max_delay=3)
    def init_chain_v2(self, chain_info):
        try:
            if isinstance(chain_info, tuple):
                chain_name,rpc_url = chain_info
                web3 = Web3(Web3.HTTPProvider(rpc_url))
                self.chain_instances[chain_name] = web3
                setattr(self, f"{chain_name}_w3", web3)
                balance = Web3.from_wei(web3.eth.get_balance(self.address), 'ether')
                setattr(self, f"{chain_name}_balance", balance)
            chains_info = []
            for chain_name, web3_instance in self.chain_instances.items():
                chains_info.append(f"{chain_name}余额:{self.get_balance_by_chain(chain_name)}")
            logger.info(f"【{self.address}】【{self.index}】余额情况 {','.join(chains_info)}")
        except Exception as e:
            raise Exception("初始化失败！")

    def add_chain(self, chain_name):
        endpoint = self.endpoints.get(chain_name)
        if endpoint:
            web3 = Web3(Web3.HTTPProvider(endpoint))
            self.chain_instances[chain_name] = web3
            setattr(self, f"{chain_name}_w3", web3)

    def add_balance(self, chain_name):
        web3 = getattr(self, f"{chain_name}_w3", None)
        if web3:
            balance = Web3.from_wei(web3.eth.get_balance(self.address), 'ether')
            setattr(self, f"{chain_name}_balance", balance)

    def get_balance(self, chain_name, address=None):
        web3 = self.chain_instances.get(chain_name)
        if web3:
            if address:
                balance = Web3.from_wei(web3.eth.get_balance(address), 'ether')
            else:
                balance = Web3.from_wei(web3.eth.get_balance(self.address), 'ether')
            return balance
        else:
            return None

    def get_balance_from_web3(self, w3, addr):
        """获取指定地址的余额"""
        balance = Web3.from_wei(w3.eth.get_balance(addr), 'ether')
        return balance

    def get_balance_by_chain(self, chain_name):
        web3_balance = getattr(self, f"{chain_name}_balance", None)
        return web3_balance

    def get_token_balance(self, w3, contract_address):
        """
        查询指定代币的余额
        """
        balance_of_method_id = w3.keccak(text="balanceOf(address)").hex()[:10]
        data = balance_of_method_id + self.address.lower()[2:].zfill(64)
        token_balance = w3.eth.call({
            'to': Web3.to_checksum_address(contract_address),
            'data': data
        })
        hex_balance = binascii.hexlify(token_balance).decode()
        balance = Web3.from_wei(int(hex_balance, 16), 'wei')
        logger.info(f'【{self.address}】【{self.index}】【合约代币：{contract_address}】余额：{balance}')
        return balance

    def get_token_by_w3(self, w3, to_address):
        """
        查询指定代币的余额
        """
        balance = Web3.from_wei(w3.eth.get_balance(Web3.to_checksum_address(to_address)), 'ether')
        logger.info(f'【{self.address}】【{self.index}】余额：{balance}')
        return balance

    def get_token_balance_by_abi(self, w3, contract_address):
        ERC20_ABI = [
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "payable": False,
                "stateMutability": "view",
                "type": "function",
            },
            {
                "constant": True,
                "inputs": [],
                "name": "decimals",
                "outputs": [{"name": "", "type": "uint8"}],
                "payable": False,
                "stateMutability": "view",
                "type": "function",
            },
        ]
        # 获取代币合约实例
        contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=ERC20_ABI)
        # 获取代币余额
        balance = contract.functions.balanceOf(Web3.to_checksum_address(self.address)).call()
        # 将余额转换为代币单位（以太为例，小数点18位）
        decimals = contract.functions.decimals().call()
        balance_in_units = balance / (10 ** decimals)
        logger.info(f'【{self.address}】【{self.index}】【合约代币：{contract_address}】余额：{balance_in_units}')
        return balance_in_units

    def get_that_token_balance_by_abi(self, w3, contract_address, addr):
        ERC20_ABI = [
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "payable": False,
                "stateMutability": "view",
                "type": "function",
            },
            {
                "constant": True,
                "inputs": [],
                "name": "decimals",
                "outputs": [{"name": "", "type": "uint8"}],
                "payable": False,
                "stateMutability": "view",
                "type": "function",
            },
        ]
        # 获取代币合约实例
        contract = w3.eth.contract(address=contract_address, abi=ERC20_ABI)
        # 获取代币余额
        balance = contract.functions.balanceOf(Web3.to_checksum_address(addr)).call()
        # 将余额转换为代币单位（以太为例，小数点18位）
        decimals = contract.functions.decimals().call()
        balance_in_units = balance / (10 ** decimals)
        logger.info(f'【{addr}】【合约代币：{contract_address}】余额：{balance_in_units}')
        return balance_in_units

    def get_token_by_w3_and_address(self, w3, contract_address, addr):
        abi_json = [{"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "id", "type": "uint256"},
                                                    {"indexed": False, "internalType": "address", "name": "to", "type": "address"},
                                                    {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"},
                                                    {"indexed": False, "internalType": "string", "name": "data", "type": "string"}],
                     "name": "CFXsCreated",
                     "type": "event"},
                    {"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "id", "type": "uint256"}],
                     "name": "CFXsDeleted",
                     "type": "event"}, {"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "id", "type": "uint256"},
                                                                       {"indexed": False, "internalType": "address", "name": "to", "type": "address"},
                                                                       {"indexed": False, "internalType": "uint256", "name": "amount",
                                                                        "type": "uint256"},
                                                                       {"indexed": False, "internalType": "string", "name": "data",
                                                                        "type": "string"}],
                                        "name": "CFXsEvent", "type": "event"}, {"anonymous": False, "inputs": [
                {"indexed": True, "internalType": "uint256", "name": "CFXsId", "type": "uint256"},
                {"indexed": False, "internalType": "uint256", "name": "etherAmount", "type": "uint256"},
                {"indexed": False, "internalType": "uint256", "name": "locktime", "type": "uint256"}], "name": "CFXsLocked", "type": "event"},
                    {"anonymous": False, "inputs": [{"indexed": True, "internalType": "uint256", "name": "CFXsId", "type": "uint256"}],
                     "name": "CFXsUnlocked",
                     "type": "event"},
                    {"inputs": [], "name": "CFXsCounter", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                     "stateMutability": "view",
                     "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "name": "CFXss",
                                           "outputs": [{"internalType": "uint256", "name": "id", "type": "uint256"},
                                                       {"internalType": "address", "name": "owner", "type": "address"},
                                                       {"internalType": "uint256", "name": "amount", "type": "uint256"},
                                                       {"internalType": "string", "name": "data", "type": "string"}], "stateMutability": "view",
                                           "type": "function"},
                    {"inputs": [], "name": "CreateCFXs", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {
                        "inputs": [{"internalType": "uint256", "name": "CFXsId", "type": "uint256"},
                                   {"internalType": "address", "name": "_to", "type": "address"},
                                   {"internalType": "uint256", "name": "_amount", "type": "uint256"}], "name": "DangerTransfer", "outputs": [],
                        "stateMutability": "nonpayable", "type": "function"},
                    {"inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "name": "LockedCFXs",
                     "outputs": [{"internalType": "uint256", "name": "_ether", "type": "uint256"},
                                 {"internalType": "uint256", "name": "locktime", "type": "uint256"}], "stateMutability": "view", "type": "function"},
                    {
                        "inputs": [{"internalType": "uint256", "name": "CFXsId", "type": "uint256"},
                                   {"internalType": "uint256", "name": "_ether", "type": "uint256"},
                                   {"internalType": "uint256", "name": "locktime", "type": "uint256"}], "name": "LockingScript", "outputs": [],
                        "stateMutability": "nonpayable", "type": "function"},
                    {"inputs": [{"internalType": "uint256", "name": "CFXsId", "type": "uint256"}], "name": "OwnerUnlockingScript", "outputs": [],
                     "stateMutability": "nonpayable", "type": "function"},
                    {"inputs": [{"internalType": "uint256", "name": "CFXsId", "type": "uint256"}], "name": "UnlockingScript", "outputs": [],
                     "stateMutability": "payable", "type": "function"},
                    {"inputs": [{"internalType": "address", "name": "_addr", "type": "address"}], "name": "balanceOf",
                     "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
                    {"inputs": [{"internalType": "uint256", "name": "_id", "type": "uint256"}], "name": "getLockStates",
                     "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"},
                    {"inputs": [{"internalType": "uint256", "name": "CFXsId", "type": "uint256"},
                                {"internalType": "string", "name": "_data", "type": "string"}],
                     "name": "inscribe", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"components": [
                {"internalType": "uint256[]", "name": "inputs", "type": "uint256[]"}, {
                    "components": [{"internalType": "address", "name": "owner", "type": "address"},
                                   {"internalType": "uint256", "name": "amount", "type": "uint256"},
                                   {"internalType": "string", "name": "data", "type": "string"}],
                    "internalType": "struct CFXsContract.OutputCFXsData[]",
                    "name": "outputs", "type": "tuple[]"}], "internalType": "struct CFXsContract.Transaction", "name": "_tx", "type": "tuple"}],
                        "name": "processTransaction", "outputs": [],
                        "stateMutability": "nonpayable",
                        "type": "function"},
                    {"inputs": [], "name": "totalSupply", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                     "stateMutability": "view",
                     "type": "function"}, {"stateMutability": "payable", "type": "receive"}]
        # 获取代币合约实例
        contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi_json)
        # 获取代币余额
        balance = contract.functions.balanceOf(Web3.to_checksum_address(addr)).call()
        # 将余额转换为代币单位（以太为例，小数点18位）
        # decimals = contract.functions.decimals().call()
        # balance_in_units = balance / (10 ** decimals)
        logger.info(f'【{addr}】【合约代币：{contract_address}】余额：{balance}')
        return balance

    def tranfer_token_by_abi(self, qw3, contract_address, to_address, val):
        """
        转任意代币(注意单位！！！)
        """
        # 合约 ABI
        abi = [
            {
                "inputs": [
                    {"internalType": "address", "name": "recipient", "type": "address"},
                    {"internalType": "uint256", "name": "amount", "type": "uint256"}
                ],
                "name": "transfer",
                "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
                "stateMutability": "nonpayable",
                "type": "function"
            }
        ]
        # 创建合约对象
        contract = qw3.eth.contract(address=contract_address, abi=abi)
        # 转账操作
        tx_hash = contract.functions.transfer(Web3.to_checksum_address(to_address), val).transact({'from': Web3.to_checksum_address(self.address)})
        # 等待交易确认
        tx_receipt = qw3.eth.waitForTransactionReceipt(tx_hash)
        logger.info(f"【{self.address}】【{self.index}】Token【{contract_address}】转给【{to_address}】成功,数量: {val}， hash: {tx_hash}")

    def get_721_nfts(self, wb3, contract_address, addr=None):
        """
        获取某个账号上的NFT（包括元数据）
        """
        if not addr:
            addr = self.address
        contract_abi = [
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}, {"name": "_index", "type": "uint256"}],
                "name": "tokenOfOwnerByIndex",
                "outputs": [{"name": "tokenId", "type": "uint256"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [{"name": "_tokenId", "type": "uint256"}],
                "name": "tokenURI",
                "outputs": [{"name": "", "type": "string"}],
                "type": "function"
            }
            # ... 其他可能的合约方法 ...
        ]
        # 创建合约实例
        nft_contract = wb3.eth.contract(address=contract_address, abi=contract_abi)
        # 查询该地址拥有的 ERC-721 NFT 总数
        nft_count = nft_contract.functions.balanceOf(addr).call()
        # 查询每个 NFT 的 tokenId
        nft_metadata_list = []
        for i in range(nft_count):
            token_id = nft_contract.functions.tokenOfOwnerByIndex(addr, i).call()
            token_uri = nft_contract.functions.tokenURI(token_id).call()
            if "application/json" in str(token_uri):
                # 解码 Base64 编码的字符串为字节数据
                decoded_utf8 = base64.b64decode(token_uri.split('base64,')[1]).decode('utf-8')
                # 解析 UTF-8 字符串为 JSON 对象
                token_uri = json.loads(decoded_utf8)
            nft_metadata_list.append({"token_id": token_id, "token_uri": token_uri})
        logger.info("NFT Metadata for", addr, ":", nft_metadata_list)
        return nft_metadata_list

    def save_balance_info(self, log_name="余额情况"):
        balance_info = ""
        chains_info = []
        for chain_name, web3_instance in self.chain_instances.items():
            balance_info = f"{balance_info}----【{chain_name}】余额----{self.get_balance_from_attr(chain_name)}"
            chains_info.append(f"{chain_name}余额:{self.get_balance_from_attr(chain_name)}")
        logger.info(f"【{self.address}】【{self.index}】余额情况 {','.join(chains_info)}")
        with open(f"{log_name}.txt", 'a', encoding='utf-8') as f:
            f.write(f'{self.index}----{self.address}----{self.private_key}----{self.mnemonic if self.mnemonic else "无"}----{balance_info}\n')
            f.close()

    def sign_msg(self, w3, msg):
        # 消息签名
        message = encode_defunct(text=msg)
        signed_message = w3.eth.account.sign_message(message, private_key=self.private_key)
        signed_data = signed_message.signature
        # logger.info("签名后:" + signed_data.hex())
        return signed_data.hex()

    def sign_msg_v2(self, msg):
        # 消息签名
        message = encode_defunct(text=msg)
        signed_message = w3.eth.account.sign_message(message, private_key=self.private_key)
        signed_data = signed_message.signature
        # logger.info("签名后:" + signed_data.hex())
        return signed_data.hex()

    def sign_hash_msg(self, msg):
        # 消息签名
        message = encode_defunct(hexstr=msg)
        signed_message = w3.eth.account.sign_message(message, private_key=self.private_key)
        signed_data = signed_message.signature
        # logger.info("签名后:" + signed_data.hex())
        return signed_data.hex()

    def sign_712(self, data):
        encoded_message = encode_typed_data(full_message=data)
        signed_message = Account.sign_message(encoded_message, private_key=self.private_key)
        # logger.info('Signature:', signed_message.signature.hex())
        return signed_message.signature.hex()

    @retry(tries=5, delay=1, backoff=2, max_delay=5)
    def get_data(self, chain_name, req_type, *params):
        url = f"{bases.get(chain_name)}{apis.get(req_type).format(*params)}&page=1&offset=1000&sort=asc"
        resp = requests.Session().get(url)
        # logger.info(resp.json())
        if "Too Many Requests" in resp.text or "Max rate limit reached, please use API Key for higher rate limit" in resp.text:
            raise Exception("重试！")
        return resp.json()['result']

    @classmethod
    def check_tx_found_in_txs(cls, txs, to_addr, search_data=None):
        """
        检查tx是否已存在
        :param txs: 某个链的交易纪录合集
        :param to_addr:
        :param search_data:
        :return:
        """
        if not txs:
            return []
        filter_txs = [obj for obj in txs if
                      obj.get('isError') == '0' and to_addr.lower() in str(obj.get('to')).lower() and obj.get(
                          'txreceipt_status') == '1']
        if search_data:
            filter_txs = [obj for obj in filter_txs if str(search_data).lower() in str(obj.get('input')).lower()]
        return filter_txs

    @staticmethod
    def get_current_gas_info(w3, tx):
        estimated_gas = w3.eth.estimate_gas(tx)
        gas_price = round(w3.from_wei(w3.eth.gas_price, "gwei"), 8)
        return estimated_gas, gas_price

    @staticmethod
    def assemble_tx_with_gas(w3, tx, gas_limit_offset=0.0, gas_price_offset=1.0, fee_eth=0.03):
        estimated_gas, gas_price = QGEth.get_current_gas_info(w3, tx)
        # gas limit偏移
        max_estimated_gas = estimated_gas + gas_limit_offset
        # gas price偏移
        max_fee_per_gas = gas_price + Decimal(gas_price_offset)
        max_priority_fee_per_gas = gas_price + Decimal(gas_price_offset - 0.001)
        # 计算预估手续费
        estimated_fee_eth = (Decimal(max_estimated_gas) * max_fee_per_gas) / 1000000000
        logger.info(f"目标地址【{tx['to']}】:预估Gas:{estimated_gas},预估Gas Price:{gas_price}Gwei,预估手续费:{estimated_fee_eth}Eth")
        # if estimated_fee_eth > fee_eth:
        #     raise Exception(f"手续费：{estimated_fee_eth}过高！跳过！")
        gas_info = {
            "gas": estimated_gas,
            "maxFeePerGas": Web3.to_wei(max_fee_per_gas, "gwei"),  # 最大矿工费用
            'maxPriorityFeePerGas': Web3.to_wei(max_priority_fee_per_gas, 'gwei'),  # 最大优先矿工费用
        }
        tx.update(gas_info)
        return tx

    def build_tx(self, w3, to_address, value, input_data, gas, max_fee_per_gas, max_priority_fee_per_gas):
        tx = {
            'from': Web3.to_checksum_address(self.address),
            'to': Web3.to_checksum_address(to_address),
            'value': Web3.to_wei(value, 'ether'),
            'data': input_data.lower(),
            'nonce': w3.eth.get_transaction_count(Web3.to_checksum_address(self.address)),
            'chainId': w3.eth.chain_id,
            "gas": gas,
            # 'gasPrice': Web3.to_wei("1", "gwei"),
            "maxFeePerGas": Web3.to_wei(f"{max_fee_per_gas}", "gwei"),  # 最大矿工费用
            'maxPriorityFeePerGas': Web3.to_wei(f'{max_priority_fee_per_gas}', "gwei"),  # 最大优先矿工费用
            'type': 2
        }
        return tx

    def send_tx(self, w3, tx, to_address, log_name, is_wait=True):
        """发送交易"""
        try:
            signed_txn = w3.eth.account.sign_transaction(tx, private_key=self.private_key)
            # 发送交易
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            logger.info(f"【{self.address}】【{self.index}】动作：{log_name},目标地址：{to_address},发送tx: {tx_hash.hex()}")
            if is_wait:
                # 等待交易确认
                tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60, poll_latency=5)
                logger.info(f"【{self.address}】【{self.index}】动作：{log_name},目标地址：{to_address},发送成功！tx: {tx_receipt.transactionHash.hex()}")
                # logger.info(f'{log_name}-成功结果',
                #          f'{self.address}----{self.private_key}----{to_address}----{tx_hash.hex()}\n')
            else:
                logger.info(f"【{self.address}】【{self.index}】动作：{log_name},目标地址：{to_address},发送成功（仅发送）！tx: {tx_hash.hex()}")
            return tx_hash.hex()
        except Exception as e:
            logger.info(f"【{self.address}】【{self.index}】动作：{log_name}执行失败,报文：{e}")
            # self.log(f'{log_name}-失败结果', f'{self.address}----{self.private_key}----{to_address}----{e}\n')
            return None

    def sent_tx_with_assembled(self, w3, to_address, value, input_data, action_name, gas_limit_offset=0.0, gas_price_offset=0.1, fee_eth=0.03,
                               is_wait_tx=True):
        """
        组装参数并发送交易
        """
        nonce = w3.eth.get_transaction_count(Web3.to_checksum_address(self.address), 'pending')
        logger.info(f'{self.address} nonce:{nonce}')
        tx = {
            'from': Web3.to_checksum_address(self.address),
            'to': Web3.to_checksum_address(to_address),
            'value': Web3.to_wei(value, 'ether'),
            'data': input_data.lower(),
            # 'nonce': w3.eth.get_transaction_count(Web3.to_checksum_address(self.address)),
            'nonce': nonce,
            'chainId': w3.eth.chain_id,
            'type': 2
        }
        try:
            self.assemble_tx_with_gas(w3, tx, gas_limit_offset=gas_limit_offset, gas_price_offset=gas_price_offset, fee_eth=fee_eth)
            tx_hash = self.send_tx(w3, tx, to_address, action_name, is_wait_tx)
            return tx_hash
        except Exception as e:
            logger.info(f"【{self.address}】【{self.index}】动作【{action_name}】预估会失败，跳过！报文：{e}")
            return None

    def sent_tx_with_assembled_by_type0(self, w3, to_address, value, input_data, action_name, gas=None, gas_price=None, is_wait_tx=True,
                                        is_estimated_tx=False):
        """
        组装参数并发送交易
        """
        try:
            nonce = w3.eth.get_transaction_count(Web3.to_checksum_address(self.address), 'pending')
            logger.info(f'【{self.address}】【{self.index}】 nonce: {nonce}')
            tx = {
                'from': Web3.to_checksum_address(self.address),
                'to': Web3.to_checksum_address(to_address),
                'value': Web3.to_wei(value, 'ether'),
                # 'nonce': w3.eth.get_transaction_count(Web3.to_checksum_address(self.address)),
                'nonce': nonce,
                'chainId': w3.eth.chain_id,
            }
            if input_data:
                tx.update({"data": input_data.lower()})
            if gas and gas_price:
                tx.update({
                    "gas": gas,
                    'gasPrice': Web3.to_wei(gas_price, "gwei")
                })
            else:
                estimated_gas, gas_price = QGEth.get_current_gas_info(w3, tx)
                tx.update({
                    "gas": estimated_gas,
                    'gasPrice': Web3.to_wei(gas_price, "gwei")
                })
            if is_estimated_tx:
                estimated_gas = w3.eth.estimate_gas(tx)
            logger.info(f"【{self.address}】【{self.index}】动作【{action_name}】tx:{tx}")
            return self.send_tx(w3, tx, to_address, action_name, is_wait_tx)
        except Exception as e:
            logger.info(f"【{self.address}】【{self.index}】动作【{action_name}】预估会失败，跳过！报文：{e}")

    def sent_with_full_tx(self, w3, to_address, value, input_data, gas, gas_price, action_name):
        """
        组装完整tx并发送交易(不计算gas,type0)
        """
        tx = {
            'from': Web3.to_checksum_address(self.address),
            'to': Web3.to_checksum_address(to_address),
            'value': Web3.to_wei(value, 'ether'),
            'data': input_data.lower(),
            'nonce': w3.eth.get_transaction_count(Web3.to_checksum_address(self.address)),
            'chainId': w3.eth.chain_id,
            "gas": gas,
            'gasPrice': Web3.to_wei(gas_price, "gwei"),
            # "maxFeePerGas": Web3.to_wei("1.000000019", "gwei"),  # 最大矿工费用
            # 'maxPriorityFeePerGas': Web3.to_wei("1", "gwei"),  # 最大优先矿工费用
            'type': 0
        }
        try:
            self.send_tx(w3, tx, to_address, action_name)
        except Exception as e:
            logger.info(f"【{self.address}】【{self.index}】动作【{action_name}】预估会失败，跳过！报文：{e}")

    def sent_with_full_tx_by_type2(self, w3, to_address, value, input_data, gas, max_fee_per_gas, max_priority_fee_per_gas, action_name):
        """
        组装完整tx并发送交易(不计算gas,type2)
        """
        tx = {
            'from': Web3.to_checksum_address(self.address),
            'to': Web3.to_checksum_address(to_address),
            'value': Web3.to_wei(value, 'ether'),
            'data': input_data.lower(),
            'nonce': w3.eth.get_transaction_count(Web3.to_checksum_address(self.address)),
            'chainId': w3.eth.chain_id,
            "gas": gas,
            # 'gasPrice': Web3.to_wei(gas_price, "gwei"),
            "maxFeePerGas": Web3.to_wei(max_fee_per_gas, "gwei"),  # 最大矿工费用
            'maxPriorityFeePerGas': Web3.to_wei(max_priority_fee_per_gas, "gwei"),  # 最大优先矿工费用
            'type': 2
        }
        try:
            self.send_tx(w3, tx, to_address, action_name)
        except Exception as e:
            logger.info(f"【{self.address}】【{self.index}】动作【{action_name}】预估会失败，跳过！报文：{e}")

    @staticmethod
    def decode_param(input_data):
        if len(input_data) < 10:
            logger.info("全空调用")
            return
        method_id, remaining = input_data[:10], input_data[10:]
        params_hex = [remaining[i:i + 64] for i in range(0, len(remaining), 64)]
        logger.info(f"函数方法:{method_id}")
        for index, param_hex in enumerate(params_hex):
            type_info, decoded_value = '', ''
            if param_hex[:7] == '0000000':
                if param_hex[-12:] == "000000000000":
                    type_info = '占位类型'
                elif param_hex[24:28] == '0000':
                    type_info, decoded_value = '数字类型', f"解码后:{int(param_hex, 16) :<66}"
                else:
                    type_info, decoded_value = '地址类型', f"解码后：0x{param_hex[24:] :<66}"
            else:
                try:
                    decoded_value = binascii.unhexlify(param_hex).decode()
                except Exception as e:
                    decoded_value = param_hex
                type_info, decoded_value = '字符类型', f"解码后:{decoded_value:<66}"
            logger.info(f"参数{str(index).ljust(2)}, {type_info}: {decoded_value}, 原码: {param_hex}")
        logger.info('=' * 100)

    @staticmethod
    def to_hex(obj,length=64):
        if isinstance(obj, str):
            return obj.encode().hex().ljust(length, "0")
        elif isinstance(obj, int):
            return hex(int(obj))[2:].rjust(length, '0')
        else:
            return str(obj)

    @staticmethod
    def create_with_mnemonic():
        """创建一个钱包带私钥和助记词"""
        Account.enable_unaudited_hdwallet_features()
        acct, mnemonic = Account.create_with_mnemonic()
        # logger.info(acct.address)
        acct1 = Account.from_mnemonic(mnemonic)
        # logger.info(acct1.address, Web3.toHex(acct1.key), mnemonic)
        return acct1.address, Web3.to_hex(acct1.key), mnemonic

    @staticmethod
    def generate_wallet(num, filename='生成的ETH钱包.txt'):
        for i in range(num):
            addr, key, mn = QGEth.create_with_mnemonic()
            log = f'{addr}----{key}----{mn}'
            logger.info(log)
            QGFile.save_to_file(f'{filename}', log)

    def random_str(self, length):
        """指定长度的随机字符"""
        str = "abcdefghijklmnopqrstuvwxyz"
        return "".join(random.choice(str) for i in range(length))

