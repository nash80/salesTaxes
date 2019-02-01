from dir.cart import Cart, Product

import json


carts_data_path = '../data/carts.json'
with open(carts_data_path) as f:
    carts_data = json.load(f)

cart_list = list()
for (c_k, c_v) in carts_data.items():
    print(c_k)
    cart = Cart()
    for p in c_v:
        pp = Product(
            label=p['label'],
            group=p['group'],
            count=p['count'],
            price=p['price'],
            imported=p['imported']
        )
        cart.add_product(pp)
    
    print(cart)
    print()