import asyncio
from huqt_oracle_client import client


# def run():
#     # Create a channel to the server at the given address (e.g., localhost:50051).
#     trader = client.Trader("account", "sigma", 'localhost:50051', secure=False)
#     trader2 = client.Trader("account2", "rigma", 'localhost:50051', secure=False)
    
#     # Prepare a request message
#     response = trader.submit_order(symbol = "BTC", size = 2, price = 100, side = 0, tif = 0)
#     print(response)
    
#     id = response.message
#     response = trader2.cancel_order(order_id = id)
#     print(response)
    
#     response = trader.cancel_order(order_id = id)
#     print(response)
    
#     response = trader.submit_order(symbol = "BTC", size = 2, price = 100, side = 0, tif = 0)
#     print(response)
    
#     ids = []
    
#     response = trader2.submit_order(symbol = "BTC", size = "2", price = "98", side = 1, tif = 0)
#     print(response)
    
#     ids.append(response.message)
    
#     response = trader2.submit_order(symbol = "BTC", size = "2", price = "98", side = 1, tif = 0)
#     print(response)
    
#     ids.append(response.message)
    
#     response = trader2.submit_order(symbol = "BTC", size = "2", price = "98", side = 1, tif = 0)
#     print(response)
    
#     ids.append(response.message)
    
#     response = trader.cancel_orders(order_ids = ids)
#     print(response)
    
#     response = trader2.cancel_orders(order_ids = ids)
#     print(response)
    
#     response = trader2.cancel_orders(order_ids = [])
#     print(response)
    
#     trader3 = client.Trader("account2", "trigma", 'localhost:50051', secure=False)
    
#     response = trader3.cancel_orders(order_ids = ids)
#     print(response)

# async def listen():
#     listener = client.Listener("account", "sigma", 'localhost:50051', secure=False)
#     await listener.listen()
    
# async def main():
#     # Run the asynchronous listener as a task.
#     task1 = asyncio.create_task(listen())
#     # Run the synchronous run() in an executor.
#     loop = asyncio.get_running_loop()
#     task2 = loop.run_in_executor(None, run)
#     await asyncio.gather(task1, task2)
    
def main():
    account = "account"
    admin = client.Admin(account, "sigma", 'huqt-oracle-rust.fly.dev:443', secure=True)
    partition = "BUMMA"
    response = admin.add_partition(partition)
    print(response)
    response = admin.add_symbol(partition, "BMM", "BMM")
    print(response)
    response = admin.start_partition(partition)
    print(response)
    response = admin.add_account_type_to_partition(partition, "admin")
    print(response)
    response = admin.send_public_message("crypto", "sigma")
    print(response)
    response = admin.send_private_message("benafan@mit.edu", "HI")
    print(response)
    # response = admin.set_position(account, "BMM", 10)
    # print(response)
    # response = admin.settle_partition(partition, settle_prices= {'BMM': 10})
    # print(response)
    # response = admin.
if __name__ == '__main__':
    # asyncio.run(main())
    main()