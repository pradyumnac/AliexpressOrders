import sheets
import json

lo = json.loads(open('orders.json','r').read())
sheets.save_aliexpress_orders(lo)