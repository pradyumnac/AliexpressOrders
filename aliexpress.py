import os
import json
import time
# import pdb
import sheets
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select

UA_STRING = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"

DEBUG = True
DEBUG_READ = False
def parse_orders_page(src, driver = None):
    node = pq(src)
    l_orders = []
    for e in node('.order-item-wraper'):
        order = {
        "order_id":        pq(e)('.order-head .order-info .first-row .info-body')[0].text,
        "order_url":       pq(e)('.order-head .order-info .first-row .view-detail-link')[0].attrib['href'],
        "order_dt":        pq(e)('.order-head .order-info .second-row .info-body')[0].text,
        "order_store":     pq(e)('.order-head .store-info .first-row .info-body')[0].text,
        "order_store_url": pq(e)('.order-head .store-info .second-row a')[0].attrib['href'],
        "order_amount": pq(e)('.order-head .order-amount .amount-body .amount-num')[0].text,
            "product_list": [{
            "title": pq(f)('.product-right .product-title a').attr['title'],
            "url": pq(f)('.product-right .product-title a').attr['href'],
            "amount": pq(f)('.product-right .product-amount').text().strip(),
            "property": pq(f)('.product-right .product-policy a').attr['title'],
            } for f in pq(e)('.order-body .product-sets')],
        "status": pq(e)('.order-body .order-status .f-left').text(),
        "status_days_left": pq(e)('.order-body .order-status .left-sendgoods-day').text().strip()
        }
        
        # GET Tracking id
        # import pdb
        # pdb.set_trace()
        if driver:
            try:
                # TODO - handle not found exception
                t_button = driver.find_element_by_xpath('//*[@button_action="logisticsTracking" and @orderid="{}"]'.format(order['order_id']))
                hover = ActionChains(driver).move_to_element(t_button).perform()
                time.sleep(5)
                
                order['tracking_id'] = driver.find_element_by_css_selector('.ui-balloon b').text.strip().split(':')[1].strip()
                try:
                    # if present, It means, tracking has begun
                    order['tracking_status'] = driver.find_element_by_css_selector('.ui-balloon .event-line-key').text
                except:
                    # Check for no event which means tracking has nto started or has not begun
                    try:
                        order['tracking_status'] = driver.find_element_by_css_selector('.ui-balloon .no-event').text.strip()
                        # If above passed, copy the tracking link and past for manual tracking
                        order['tracking_status'] = "Manual Tracking: " + driver.find_element_by_css_selector('.ui-balloon .no-event a').get_attribute('href').strip()
                    except:
                        order['tracking_status'] = '<Tracking Parse Error>'
            except:
                order['tracking_id'] = '<Error in Parsing Tracking ID>'
                order['tracking_status'] = '<Tracking Parse Error due to Error in Parsing Tracking ID>'
                print("Tracking id retrieval failed for order:"+order['order_id'])
                pass
        
        l_orders.append(order)
        
    return l_orders
    
    
def parse_orders(driver='', order_json_file='', cache_mode='webread'):
    orders = []
    if cache_mode == 'webread':
        if driver is '':
            raise Exception("No Selenium driver found in webread mode.")
        # Verify number of orders and implement pagination
        
        source = driver.find_element_by_id("buyer-ordertable").get_attribute("innerHTML")
    elif cache_mode == 'localwrite' :
        if order_json_file is '':
            raise Exception("Filename Missing. Please passa vali filename to order_json_file.")
        source = driver.find_element_by_id("buyer-ordertable").get_attribute("innerHTML")
        open(order_json_file,'wb').write(source.encode('utf-8'))
    elif cache_mode == "localread":
        source = open(order_json_file, 'rb').read()
    else:
        raise Exception("Invalid cache_mode selected.")
    
    break_loop = False
    try:
        cur_page,total_page = (int(i) for i in driver.find_element_by_xpath('//*[@id="simple-pager"]/div/label').text.split('/'))
        while(1):        
            source = driver.find_element_by_id("buyer-ordertable").get_attribute("innerHTML")
            orders.extend(parse_orders_page(source,driver=driver))
            if break_loop:
                break
            elif cur_page < total_page:
                link_next = driver.find_element_by_xpath('//*[@id="simple-pager"]/div/a[text()="Next "]')
                # pdb.set_trace()
                link_next.click()
                cur_page,total_page = (int(i) for i in driver.find_element_by_xpath('//*[@id="simple-pager"]/div/label').text.split('/'))
            # pdb.set_trace()
            print("Page:%d/%d"%(cur_page,total_page))
            if cur_page == total_page:
                break_loop = True # to break after parsing the next time
        return orders
    except Exception as e:
        print(e)
        return([])
    
def get_open_orders(email,passwd, drivertype, driver_path=''):
    if drivertype == "Chrome":
        if driver_path is '':
            raise Exception("Driverpath cannot be blank for Chrome")
        from selenium.webdriver.chrome.options import Options
        opts = Options()
        opts.add_argument("user-agent="+UA_STRING)
        driver = webdriver.Chrome(driver_path,chrome_options=opts)
    elif drivertype == "PhantomJS":
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (UA_STRING)
        driver = webdriver.PhantomJS(desired_capabilities=dcap)
    else:
        raise Exception("Invalid Driver Type:" + drivertype)
    driver.set_window_size(1366, 680)
    driver.get("https://login.aliexpress.com/express/mulSiteLogin.htm?spm=2114.11010108.1000002.7.9c5Rcg&return=http%3A%2F%2Fwww.aliexpress.com%2F")
    driver.switch_to_frame(driver.find_element_by_id("alibaba-login-box"))
    element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "fm-login-id"))
    )
    element.send_keys(email)
    driver.find_element_by_xpath("//*[@id=\"fm-login-password\"]").send_keys(passwd)
    driver.find_element_by_id("fm-login-submit").click()
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search-key"))
    )
    driver.get("http://trade.aliexpress.com/orderList.htm?spm=2114.11010108.1000002.18.bT7Uae")
    
    # ua = driver.find_element_by_id("nav-user-account")
    # hov = ActionChains(driver).move_to_element(ua)
    # hov.perform()
    # 1/0
    aliexpress = {}
    
    elemAwaitingShipment = driver.find_element_by_id("remiandTips_waitSendGoodsOrders")
    intAwaitingShipment = elemAwaitingShipment.get_attribute("innerText").split("(")[1].strip(")")
    elemAwaitingShipment.click()
    aliexpress['Not Shipped'] = parse_orders(driver, 'ae1.html','webread')
    
    elemAwaitingDelivery = driver.find_element_by_id("remiandTips_waitBuyerAcceptGoods")
    intAwaitingDelivery = elemAwaitingDelivery.get_attribute("innerText").split("(")[1].strip(")")
    elemAwaitingDelivery.click()
    aliexpress['Shipped'] = parse_orders(driver, 'ae2.html','webread')
    
    
    elemAwaitingShipment = driver.find_element_by_id("remiandTips_waitBuyerPayment")
    intAwaitingShipment = elemAwaitingShipment.get_attribute("innerText").split("(")[1].strip(")")
    elemAwaitingShipment.click()
    aliexpress['Order Awaiting Payment'] = parse_orders(driver, 'ae3.html','webread')
    
    driver.find_element_by_id("switch-filter").click()
    Select(driver.find_element_by_id("order-status")).select_by_value('FINISH')
    driver.find_element_by_id("search-btn").click()
    
    # intCompleted = elemCompleted.get_attribute("innerText").split("(")[1].strip(")")
    aliexpress['Order Completed'] = parse_orders(driver, 'ae4.html','webread')
    
    
    if DEBUG:        
        open("orders.json","w").write(json.dumps(aliexpress))
        
    return(aliexpress)
        
if __name__ == "__main__":
    
    
    if DEBUG_READ:        
        orders = json.loads(open("orders.json","r").read())
    else:
        orders = get_open_orders(os.environ['AE_username'],os.environ['AE_passwd'],"Chrome","D:\Projects\projects\cams\chromedriver.exe")
    
    print(orders.keys())
    sheets.clear_google_sheet(sheets.URL, sheets.SHEET_NAME)
    sheets.save_aliexpress_orders(orders)