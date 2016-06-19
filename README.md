# AliexpressOrders
Now track your aliexpress orders easily. This python script generates a json representation of all your orders

### Whats working:
1. Awaiting Shipments orders details
2. Awaiting Delivery Order details

### Work In Progress
1. Order Tracking ID retrieval
2. Implement pagination for the above sections
3. Google Sheets Integration ( Dump to Google Sheets)

### To Do
1. Integrate Tracking ID with an existing tracker to get package updates
2. Desktop App with UI

### Installation
* As of the current state, The package is dependant on lxml, pyquery, selenium and Chromedriver/PhantomJS Pa*ckage. 
* For lxml pacakge, the WHL file for windows is hardcoded in requiremensts file. So the requirements file will nott work on other platforms. I will fork out the reuiremments file for different platforms
* You need to edit the path to Chromexdriver in the file
* Also, setup the Aliexpress Username and Password as environment variables. This is a makeshiift arrangement to pass on the credentials. A more permanent solution will be used once this sotware gets a destop app
