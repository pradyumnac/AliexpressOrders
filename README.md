# AliexpressOrders
Now track your aliexpress orders easily. This python script generates a json representation of all your orders. It also saved the inforation in a google sheet if you have set up one

### Whats working:
1. Awaiting Shipments orders details
2. Awaiting Delivery Order details
3. Implement pagination for the above sections such that more than 10 orders per section appears
4. Implement google sheet integration

### Work In Progress
1. Order Tracking ID/carrier retrieval
2. Implement batch google sheet update

### To Do
1. Integrate Tracking ID with an existing tracker to get package logistic updates
2. Desktop App with UI

### Installation
* As of the current state, The package is dependant on lxml, pyquery, selenium and Chromedriver/PhantomJS Package. 
* For lxml pacakge, the WHL file for windows is hardcoded in Windows file. Install using the following command:
  * Windows:  `pip install -r requirements.win.txt
  * Windows/Linux/Other platforms where python C mode LXMl can be compiled: `pip install -r requirements.base.txt
* Edit the path to Chromexdriver in the file
* Get Google Service Credentials. Download the credential json in same folder and point the path in the credentials call in file
* You need to share a google sheet and copy the url to an environment variable *AE_gsheet_url*
* Also, setup the Aliexpress Username and Password as environment variables. *AE_username* and *AE_passwd* 
* Why Environment Variables: This is a makeshiift arrangement to pass on the credentials. A more permanent solution will be used once this sotware gets a destop app. Otherwise exposing these information in publicly shared code is a breachof privacy/security

### License
This code ia available as free to use/redistribute under MIT License. Please check the LICENSE File for sharing and attributuon requirements


