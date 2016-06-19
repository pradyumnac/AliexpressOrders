import gspread
import pdb
import datetime
from oauth2client.service_account import ServiceAccountCredentials
url = 'https://docs.google.com/spreadsheets/d/1ZP9ZAPxPwdu4gCCTn1kjUJB8M6JafdxmLUi4TuGLskc/edit?usp=sharing'
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('CAMSCAS-6ac566f0e517.json', scope)

def get_sheet_dict(sheet_url,worksheet_name):
    gc = gspread.authorize(credentials)
    wkb = gc.open_by_url(sheet_url)
    wks = wkb.worksheet(worksheet_name)
    
    v_list = wks.get_all_values()
    heading = v_list[0]
    v_list_of_dict = []
    for v in v_list[2:]:
        # pdb.set_trace()
        v_list_of_dict.append(dict((heading[i],v[i]) for i in range(len(v))))
        
    return v_list_of_dict
    

# Add a record to the end of google sheet url supplied
# no need to pass index
def add_record_from_dict(sheet_url, worksheet_name, dict_rec):
    
    gc = gspread.authorize(credentials)
    wkb = gc.open_by_url(sheet_url)
    wks = wkb.worksheet(worksheet_name)
    values_list = [ i for i in wks.row_values(1) if i]
    if not set(dict_rec.keys()) == set(values_list):
        raise Exception("Dictionary is not well formed for the sheet.")
    new_row = []
    new_row.append(wks.row_count) #index = row_count + 1(next item) - 1(1st row heading)
    for i in values_list:
        new_row.append(dict_rec[i])
    wks.append_row(new_row)

# index is handled in insertion logic
def create_order_dict(order_id, title, tracking_id, carrier, status, order_dt, recv_dt, price, updated_on):
    return {
        "#"          :'',
        "Order ID"   :order_id,
        "Title"      :title,
        "Tracking ID":tracking_id,
        "Carrier"    :carrier,
        "Status"     :status,
        "Order Date" :order_dt,
        "Recv Date"  :recv_dt,
        "Price"      :price,
        "Updated On" :updated_on
    }
    
def save_aliexpress_orders(dict_orders):
    list_awaiting_shipment = dict_orders['Not Shipped']
    list_awaiting_delivery = dict_orders['Shipped']
    
    #tracking, carrier, status should be item wise, not order wise
    # for awaiting shipment, tracking id is sent as blank
    
    for i in list_awaiting_shipment:
        for j in i['product_list']:
            dict_save = create_order_dict(
            i['order_id'],
            j['title'],
            '',
            i['carrier'],
            i['status'],
            i['order_dt'],
            '',
            j['amount'],
            str(datetime.datetime.now())
            )
            
            add_record_from_dict(url,"Sheet2",dict_save)
    for i in list_awaiting_delivery:
        for j in i['product_list']:
            dict_save = create_order_dict(
            i['order_id'],
            j['title'],
            i['tracking_id'],
            i['carrier'],
            i['status'],
            i['order_dt'],
            '',
            j['amount'],
            str(datetime.datetime.now())
            )
            
            add_record_from_dict(url,"Sheet2",dict_save)
            
if __name__ == '__main__':
    add_record_from_dict(url,"Sheet2",create_order_dict('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', str(datetime.datetime.now())))