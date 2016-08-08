# AliexpressOrders
Now track your own aliexpress orders easily. This python script generates a json representation of all your orders. It also saved the information in a google sheet if you have set up one. 

This will enable you to use powerful spreadsheet filters in google sheets for better order manageent and tracking

### Whats working:
1. Awaiting Shipments orders details
2. Awaiting Delivery Order details
3. Ordr Completed details
4. Orders pending payment details
3. Implement pagination for the above sections such that more than 10 orders per section appears
4. Implement google sheet integration
5. Implement batch google sheet update (Now update to google sheets is much faster - 20s for 200 plus orders)
6. Order tracking ID integrated. Also, the last package delivery status for the tracking id is retrieved

### Work In Progress
1. Order carrier retrieval
2. Fix date and Purchase protection remaining data format for easier filtering in google sheets

### To Do
1. Integrate Tracking ID with an existing tracker to get package logistic updates
2. Desktop App with UI
3. Total Payment Integration ( Order Paid, Order cancelled, Dispute refund) details to be separately tracked
4. Convert selenium integration to headless mode for uninterrupted web scrapping in the background

### Installation
* As of the current state, The package is dependant on lxml, pyquery, selenium and Chromedriver/PhantomJS Package. 
* For lxml pacakge, the WHL file for windows is hardcoded in Windows file. Install using the following command:
  * Windows without library building support:  `pip install -r requirements.win.txt
  * Windows/Linux/Other platforms where python C extension for lxml can be compiled/built: `pip install -r requirements.base.txt
* Edit the path to Chromexdriver in the file
* Get Google Service Credentials. Download the credential json in same folder and point the path in the credentials call in file
* You need to share a google sheet and copy the url to an environment variable **AE_gsheet_url**
* Also, setup the Aliexpress Username and Password as environment variables. **AE_username** and **AE_passwd**
* Why Environment Variables: This is a makeshiift arrangement to pass on the credentials. Otherwise exposing these information in publicly shared code is a breach of privacy/security. A more permanent solution will be used once this sotware gets a desktop app. 

### License
This code ia available as free to use/redistribute under MIT License. Please check the LICENSE File for sharing and attributuon requirements
