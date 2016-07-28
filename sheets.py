import gspread
# import pdb
import datetime
import os
from oauth2client.service_account import ServiceAccountCredentials
URL = os.environ['AE_gsheet_url']
SHEET_NAME = 'Sheet2'
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
    
def clear_google_sheet(sheet_url, worksheet_name):
    gc = gspread.authorize(credentials)
    wkb = gc.open_by_url(sheet_url)
    wks = wkb.worksheet(worksheet_name)
    
    wks.resize(rows=1)
    
# Add a record to the end of google sheet url supplied
# no need to pass index
def add_record_from_dict(sheet_url, worksheet_name, dict_rec):
    # one at a time
    gc = gspread.authorize(credentials)
    wkb = gc.open_by_url(sheet_url)
    wks = wkb.worksheet(worksheet_name)
    values_list = [ i for i in wks.row_values(1) if i]
    dict_rec["#"] = wks.row_count #index = row_count + 1(next item) - 1(1st row heading)
    if not set(dict_rec.keys()) == set(values_list):
        raise Exception("Dictionary is not well formed for the sheet.")
    new_row = []
    for i in values_list:
        new_row.append(dict_rec[i])
    wks.append_row(new_row)
    

# index is handled in insertion logic
def create_order_dict(order_id, title, tracking_id, carrier, status, order_dt, recv_dt, price, updated_on):
    return {
        "Order ID"   :order_id,
        "Title"      :title,
        "Tracking ID":tracking_id,
        "Tracking Status"    :carrier,
        "Status"     :status,
        "Order Date" :order_dt,
        "Days Left"  :recv_dt,
        "Price"      :price,
        "Updated On" :updated_on
    }
    
def batch_update_gsheet(sheet_url, worksheet_name, list_rec, ts):
    gc = gspread.authorize(credentials)
    wkb = gc.open_by_url(sheet_url)
    wks = wkb.worksheet(worksheet_name)
    
    rc = len(list_rec)
    # cc = len(list_rec[0].keys())
    # cc = len(list_rec[0])
    print("number of rows:"+str(wks.row_count))
    wks.resize(rc+10,10)
    print("number of rows after resize:"+str(wks.row_count))
    # wks.add_rows(rc+10-wks.row_count)
    print('A2:J'+str(rc+1))
    cell_list = wks.range('A2:J'+str(rc+1))
    i = 0
    j = 0
            
    for cell in cell_list:
        # print(list_rec[i])
        if(j==0):
            cell.value = str(i+1)
        elif(j==1):
            cell.value = list_rec[i]['Order ID']
        elif(j==2):
            cell.value = list_rec[i]['Title'] 
        elif(j==3):
            cell.value = list_rec[i]['Tracking ID'] 
        elif(j==4):
            cell.value = list_rec[i]['Tracking Status'] 
        elif(j==5):
            cell.value = list_rec[i]['Status']
        elif(j==6):
            cell.value = list_rec[i]['Order Date']
        elif(j==7):
            cell.value = list_rec[i]['Days Left']
        elif(j==8):
            cell.value = list_rec[i]['Price']
        elif(j==9):
            cell.value = str(datetime.datetime.now())
            j=-1 # made0 in increment step
            i+=1
        # elif(j==10):
            # j=0
            # i += 1 
            # continue
        j += 1
        # cell.value = 'O_o'
    
    wks.update_cells(cell_list) # Update in batch

    
def save_aliexpress_orders(dict_orders):
    list_awaiting_shipment = dict_orders['Not Shipped']
    list_awaiting_delivery = dict_orders['Shipped']
    
    # batch update
    batch_save_list = []
    
    #tracking, carrier, status should be item wise, not order wise
    # for awaiting shipment, tracking id is sent as blank
    
    for i in list_awaiting_shipment:
        for j in i['product_list']:
            dict_save = create_order_dict(
            i['order_id'],
            j['title'],
            '',
            '',
            i['status'],
            i['order_dt'],
            '',
            j['amount'],
            str(datetime.datetime.now())
            )
            
            # add_record_from_dict(URL,SHEET_NAME,dict_save)
            
            # Append to batch list
            batch_save_list.append(dict_save)
            
    for i in list_awaiting_delivery:
        for j in i['product_list']:
            try:
                
                dict_save = create_order_dict(
                i['order_id'],
                j['title'],
                i['tracking_id'],
                i['tracking_status'],
                i['status'],
                i['order_dt'],
                ''.join(i['status_days_left'].strip('Your order will be closed in:').strip().split(' ')),
                j['amount'],
                str(datetime.datetime.now())
                )
                
                # add_record_from_dict(URL,SHEET_NAME,dict_save)
                
                # Append to batch list
                batch_save_list.append(dict_save)
            except:
                print(j.keys())
                import sys
                print(sys.exc_info())
                print('Error in saving order'+i['order_id'])
    
    batch_update_gsheet(URL,SHEET_NAME, batch_save_list, str(datetime.datetime.now()))
    
if __name__ == '__main__':
    # clear_google_sheet(URL, SHEET_NAME)
    # add_record_from_dict(URL,SHEET_NAME,create_order_dict('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', str(datetime.datetime.now())))
    batch_update_gsheet(URL,
        SHEET_NAME, [
        create_order_dict('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', str(datetime.datetime.now())),
        create_order_dict('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', str(datetime.datetime.now())),
        create_order_dict('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', str(datetime.datetime.now())),
        create_order_dict('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', str(datetime.datetime.now()))],
        str(datetime.datetime.now()))