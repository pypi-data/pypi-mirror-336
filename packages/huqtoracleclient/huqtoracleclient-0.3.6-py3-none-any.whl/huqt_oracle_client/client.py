from enum import Enum
from typing import Dict, List, Optional, Tuple
import grpc
import certifi
from .protos import exchange_pb2 as exchange
from .protos import exchange_pb2_grpc
from .protos import marketdata_pb2 as marketdata
from .protos import marketdata_pb2_grpc
from .protos import admin_pb2
from .protos import admin_pb2_grpc

from dataclasses import dataclass

@dataclass
class Response:
    status: str
    message: str
    
@dataclass
class PublicOrder:
    symbol: str
    size: int
    price: int
    

@dataclass
class ResponseList:
    response: Optional[Response]
    order_responses: List[Response]

class OrderSide(Enum):
    BUY = 0
    SELL = 1
    
class OrderTif(Enum):
    DAY = 0
    IOC = 1

def get_channel(url, secure):
    # Load the CA bundle from certifi
    if not secure:
        return grpc.insecure_channel(url)
    else:
        with open(certifi.where(), "rb") as f:
            trusted_certs = f.read()
        # Create secure channel credentials using the trusted certificates
        credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
        return grpc.secure_channel(url, credentials)

def get_async_channel(url, secure):
    # Load the CA bundle from certifi
    if not secure:
        return grpc.aio.insecure_channel(url)
    else:
        with open(certifi.where(), "rb") as f:
            trusted_certs = f.read()
        # Create secure channel credentials using the trusted certificates
        credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
        return grpc.aio.secure_channel(url, credentials)
        

class Trader():
    def __init__(self, account, api_key, url, secure = True):
        self.channel = get_channel(url, secure)
        self.stub = exchange_pb2_grpc.ExchangeStub(self.channel)
        self.api_key = api_key
        self.account = account
    
    def submit_order(self, symbol: str, size: int, price: int, side: OrderSide, tif: OrderTif) -> Response:
        return submit_order(self.stub, symbol, size, price, side, tif, self.account, self.api_key)
    
    def cancel_order(self, order_id: str) -> Response:
        return cancel_order(self.stub, order_id, self.account, self.api_key)
    
    def cancel_orders(self, order_ids: List[str]) -> ResponseList:
        return cancel_orders(self.stub, order_ids, self.account, self.api_key)

class Listener():
    def __init__(self, account, api_key, url, secure = True):
        self.channel = get_async_channel(url, secure)
        self.stub = marketdata_pb2_grpc.MarketDataServiceStub(self.channel)
        self.api_key = api_key
        self.account = account
    
    async def listen(self):
        await listen(self.stub, self.account, self.api_key)
        
class Admin():
    def __init__(self, account, api_key, url, secure = True):
        self.channel = get_channel(url, secure)
        self.stub = admin_pb2_grpc.AdminServiceStub(self.channel)
        self.api_key = api_key
        self.account = account
    
    def add_partition(self, partition: str):
        return add_partition(
            stub=self.stub,
            partition=partition,
            account=self.account,
            api_key=self.api_key
        )

    def add_account_type_to_partition(self, partition: str, account_type: str):
        return add_account_type_to_partition(
            stub=self.stub,
            partition=partition,
            account_type=account_type,
            account=self.account,
            api_key=self.api_key
        )

    def add_symbol(self, partition: str, id: str, display_name: str):
        return add_symbol(
            stub=self.stub,
            partition=partition,
            id=id,
            name=display_name,
            account=self.account,
            api_key=self.api_key
        )

    def start_partition(self, partition: str):
        return start_partition(
            stub=self.stub,
            partition=partition,
            account=self.account,
            api_key=self.api_key
        )

    def pause_partition(self, partition: str):
        return pause_partition(
            stub=self.stub,
            partition=partition,
            account=self.account,
            api_key=self.api_key
        )

    # Analogues for the remaining Admin RPC functions:

    def end_partition(self, partition: str):
        return end_partition(
            stub=self.stub,
            partition=partition,
            account=self.account,
            api_key=self.api_key
        )

    def settle_partition(self, partition: str, settle_prices: Dict[str, int]):
        """
        settle_prices: Dict mapping symbol to price
        """
        prices = []
        for key in settle_prices:
            prices.append((key, str(settle_prices[key])))
        return settle_partition(
            stub=self.stub,
            partition=partition,
            settle_prices=prices,
            account=self.account,
            api_key=self.api_key
        )

    def open_exchange(self):
        return open_exchange(
            stub=self.stub,
            account=self.account,
            api_key=self.api_key
        )

    def close_exchange(self):
        return close_exchange(
            stub=self.stub,
            account=self.account,
            api_key=self.api_key
        )

    def set_position(self, account: str, symbol: str, value: int):
        return set_position(
            stub=self.stub,
            account=account,
            symbol=symbol,
            value=str(value),
            admin_account=self.account,
            api_key=self.api_key
        )

    def adjust_position(self, account: str, symbol: str, value: int):
        return adjust_position(
            stub=self.stub,
            account=account,
            symbol=symbol,
            value=str(value),
            admin_account=self.account,
            api_key=self.api_key
        )

    def set_account_fee(self, account: str, fee: int):
        return set_account_fee(
            stub=self.stub,
            account=account,
            fee=str(fee),
            admin_account=self.account,
            api_key=self.api_key
        )

    def set_enable_fee(self, symbol: str, enable: bool):
        return set_enable_fee(
            stub=self.stub,
            symbol=symbol,
            enable=enable,
            account=self.account,
            api_key=self.api_key
        )
    
    def set_position_limits(self, account: str, symbol: str, lower_bound: float, upper_bound: float):
        if lower_bound == -float('inf'):
            lower_bound = "-Infinity"
        else:
            lower_bound = int(lower_bound)
        if upper_bound == float('inf'):
            upper_bound = "Infinity"
        else:
            upper_bound = int(upper_bound)
        return set_position_limits(
            stub=self.stub,
            account=account,
            symbol=symbol,
            lower_bound=str(lower_bound),
            upper_bound=str(upper_bound),
            admin_account=self.account,
            api_key=self.api_key
        )

    def register_named_account(self, account: str):
        return register_named_account(
            stub=self.stub,
            account=account,
            admin_account=self.account,
            api_key=self.api_key
        )
    
    def register_bot_account(self, account: str):
        return register_bot_account(
            stub=self.stub,
            account=account,
            admin_account=self.account,
            api_key=self.api_key
        )
    
    def send_private_message(self, account: str, message: str):
        return send_private_message(
            stub=self.stub,
            account=account,
            message=message,
            admin_account=self.account,
            api_key=self.api_key
        )
    def send_public_message(self, partition: str, message: str):
        return send_public_message(
            stub=self.stub,
            partition=partition,
            message=message,
            admin_account=self.account,
            api_key=self.api_key
        )
    def get_position(self, account: str, symbol: str) -> int:
        return get_position(
            stub=self.stub,
            account=account,
            symbol=symbol,
            admin_account=self.account,
            api_key=self.api_key
        )

        
    

def submit_order(stub: exchange_pb2_grpc.ExchangeStub, symbol: str, size: int, price: int, side: OrderSide, tif: OrderTif, account: str, api_key: str) -> Response: 
    request = exchange.OrderRequest(symbol = symbol, logging = "", size = str(size), price = str(price), side = side.value, tif = tif.value, account = account, api_key = api_key)
    response = stub.SubmitOrder(request)
    return Response(status = response.status, message = response.message)
    

    
def cancel_order(stub: exchange_pb2_grpc.ExchangeStub, order_id: str, account: str, api_key: str) -> Response:
    request = exchange.CancelOrderRequest(order_id = order_id, account = account, api_key = api_key)
    response = stub.CancelOrder(request)
    return Response(status = response.status, message = response.message)

def cancel_orders(stub: exchange_pb2_grpc.ExchangeStub, order_ids: List[str], account: str, api_key: str) -> ResponseList:
    request = exchange.CancelOrdersRequest(order_ids = order_ids, account = account, api_key = api_key)
    response = stub.CancelOrders(request)
    if response.HasField("response"):
        return ResponseList(response = response.response, order_responses = response.order_responses)
    else:
        return ResponseList(response = None, order_responses = response.order_responses)
    
def add_account_type_to_partition(
    stub: admin_pb2_grpc.AdminServiceStub, 
    partition: str, 
    account_type: str, 
    account: str, 
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=account, api_key=api_key)
    request = admin_pb2.AddAccountTypeToPartitionRequest(
        partition=partition, 
        account_type=account_type, 
        auth=auth
    )
    response = stub.AddAccountTypeToPartition(request)
    return Response(status=response.status, message=response.message)

def end_partition(
    stub: admin_pb2_grpc.AdminServiceStub, 
    partition: str, 
    account: str, 
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=account, api_key=api_key)
    request = admin_pb2.EndPartitionRequest(
        partition=partition, 
        auth=auth
    )
    response = stub.EndPartition(request)
    return Response(status=response.status, message=response.message)

def pause_partition(
    stub: admin_pb2_grpc.AdminServiceStub, 
    partition: str, 
    account: str, 
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=account, api_key=api_key)
    request = admin_pb2.PausePartitionRequest(
        partition=partition, 
        auth=auth
    )
    response = stub.PausePartition(request)
    return Response(status=response.status, message=response.message)

def start_partition(
    stub: admin_pb2_grpc.AdminServiceStub, 
    partition: str, 
    account: str, 
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=account, api_key=api_key)
    request = admin_pb2.StartPartitionRequest(
        partition=partition, 
        auth=auth
    )
    response = stub.StartPartition(request)
    return Response(status=response.status, message=response.message)

def settle_partition(
    stub: admin_pb2_grpc.AdminServiceStub, 
    partition: str, 
    settle_prices: List[Tuple[str, str]], 
    account: str, 
    api_key: str
) -> Response:
    """
    settle_prices: list of tuples (symbol, price)
    """
    auth = admin_pb2.AdminAuthInfo(account=account, api_key=api_key)
    settlements = [
        admin_pb2.Settlement(symbol=symbol, price=price)
        for symbol, price in settle_prices
    ]
    request = admin_pb2.SettlePartitionRequest(
        partition=partition, 
        settle_prices=settlements, 
        auth=auth
    )
    response = stub.SettlePartition(request)
    return Response(status=response.status, message=response.message)

def open_exchange(
    stub: admin_pb2_grpc.AdminServiceStub, 
    account: str, 
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=account, api_key=api_key)
    request = admin_pb2.OpenExchangeRequest(auth=auth)
    response = stub.OpenExchange(request)
    return Response(status=response.status, message=response.message)

def close_exchange(
    stub: admin_pb2_grpc.AdminServiceStub, 
    account: str, 
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=account, api_key=api_key)
    request = admin_pb2.CloseExchangeRequest(auth=auth)
    response = stub.CloseExchange(request)
    return Response(status=response.status, message=response.message)

def add_symbol(
    stub: admin_pb2_grpc.AdminServiceStub, 
    partition: str, 
    id: str, 
    name: str, 
    account: str, 
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=account, api_key=api_key)
    request = admin_pb2.AddSymbolRequest(
        partition=partition, 
        id=id, 
        name=name, 
        auth=auth
    )
    response = stub.AddSymbol(request)
    return Response(status=response.status, message=response.message)

def set_position(
    stub: admin_pb2_grpc.AdminServiceStub, 
    account: str, 
    symbol: str, 
    value: str, 
    admin_account: str,
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=admin_account, api_key=api_key)
    request = admin_pb2.SetPositionRequest(
        account=account, 
        symbol=symbol, 
        value=value, 
        auth=auth
    )
    response = stub.SetPosition(request)
    return Response(status=response.status, message=response.message)

def adjust_position(
    stub: admin_pb2_grpc.AdminServiceStub, 
    account: str, 
    symbol: str, 
    value: str, 
    admin_account: str,
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=admin_account, api_key=api_key)
    request = admin_pb2.AdjustPositionRequest(
        account=account, 
        symbol=symbol, 
        value=value, 
        auth=auth
    )
    response = stub.AdjustPosition(request)
    return Response(status=response.status, message=response.message)

def set_account_fee(
    stub: admin_pb2_grpc.AdminServiceStub, 
    account: str, 
    fee: str, 
    admin_account: str,
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=admin_account, api_key=api_key)
    request = admin_pb2.SetAccountFeeRequest(
        account=account, 
        fee=fee, 
        auth=auth
    )
    response = stub.SetAccountFee(request)
    return Response(status=response.status, message=response.message)

def set_enable_fee(
    stub: admin_pb2_grpc.AdminServiceStub, 
    symbol: str, 
    enable: bool, 
    account: str, 
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=account, api_key=api_key)
    request = admin_pb2.SetEnableFeeRequest(
        symbol=symbol, 
        enable=enable, 
        auth=auth
    )
    response = stub.SetEnableFee(request)
    return Response(status=response.status, message=response.message)

def set_position_limits(
    stub: admin_pb2_grpc.AdminServiceStub, 
    account: str, 
    symbol: str, 
    lower_bound: str, 
    upper_bound: str, 
    admin_account: str,
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=admin_account, api_key=api_key)
    request = admin_pb2.SetPositionLimitsRequest(
        account=account, 
        symbol=symbol, 
        lower_bound=lower_bound, 
        upper_bound=upper_bound, 
        auth=auth
    )
    response = stub.SetPositionLimits(request)
    return Response(status=response.status, message=response.message)

def register_named_account(
    stub: admin_pb2_grpc.AdminServiceStub, 
    account: str,
    admin_account: str, 
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=admin_account, api_key=api_key)
    request = admin_pb2.RegisterNamedAccountRequest(
        account=account, 
        auth=auth
    )
    response = stub.RegisterNamedAccount(request)
    return Response(status=response.status, message=response.message)

def register_bot_account(
    stub: admin_pb2_grpc.AdminServiceStub, 
    account: str,
    admin_account: str, 
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=admin_account, api_key=api_key)
    request = admin_pb2.RegisterBotAccountRequest(
        account=account, 
        auth=auth
    )
    response = stub.RegisterBotAccount(request)
    return Response(status=response.status, message=response.message)

def add_partition(
    stub: admin_pb2_grpc.AdminServiceStub, 
    partition: str, 
    account: str, 
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=account, api_key=api_key)
    request = admin_pb2.AddPartitionRequest(
        partition=partition, 
        auth=auth
    )
    response = stub.AddPartition(request)
    return Response(status=response.status, message=response.message)

def send_private_message(
    stub: admin_pb2_grpc.AdminServiceStub, 
    account: str, 
    message: str,
    admin_account: str,
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=admin_account, api_key=api_key)
    request = admin_pb2.SendPrivateMessageRequest(
        account=account, 
        message=message,
        auth=auth
    )
    response = stub.SendPrivateMessage(request)
    return Response(status=response.status, message=response.message)

def send_public_message(
    stub: admin_pb2_grpc.AdminServiceStub, 
    partition: str, 
    message: str,
    admin_account: str,
    api_key: str
) -> Response:
    auth = admin_pb2.AdminAuthInfo(account=admin_account, api_key=api_key)
    request = admin_pb2.SendPublicMessageRequest(
        partition=partition, 
        message=message,
        auth=auth
    )
    response = stub.SendPublicMessage(request)
    return Response(status=response.status, message=response.message)

def get_position(
    stub: admin_pb2_grpc.AdminServiceStub, 
    account: str, 
    symbol: str,
    admin_account: str,
    api_key: str
) -> int:
    auth = admin_pb2.AdminAuthInfo(account=admin_account, api_key=api_key)
    request = admin_pb2.GetPositionRequest(
        account=account, 
        symbol=symbol,
        auth=auth
    )
    response = stub.GetPosition(request)
    return int(response.message)

    
async def listen(stub: marketdata_pb2_grpc.MarketDataServiceStub, account: str, api_key: str):
    # Build your subscription request. Adjust fields as needed.
    request = marketdata.SubscriptionRequest(
        api_key=api_key,
        account=account
    )
    
    # Calling the streaming RPC method.
    stream = stub.StreamStatus(request)
    
    # Iterate over the stream of responses.
    async for market_data in stream:
        print("Received market data:", market_data)