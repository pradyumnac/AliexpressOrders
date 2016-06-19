import os
import json
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

UA_STRING = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"

DEBUG = True
def parse_orders_page(src):
    node = pq(src)
    return([
        {
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
        } for e in node('.order-item-wraper')
    ])
    
def parse_orders(driver='', order_json_file='', cache_mode='webread'):
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
    
    
    return parse_orders_page(source)
    
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
    driver.set_window_size(1120, 550)
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
    if DEBUG:        
        open("orders.json","w").write(json.dumps(aliexpress))
        
if __name__ == "__main__":
    print(get_open_orders("chatterjee.pra@gmail.com",os.environ['AE_passwd'],"Chrome","D:\Projects\projects\cams\chromedriver.exe"))