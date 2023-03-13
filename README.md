
# Scrape_bot

## Rocketreach

The rocketreach website which appears to use a combination of public data sources and machine learning algorithms to gather and verify their data. They claim to scan millions of websites, social media profiles, and professional directories to collect information on professionals and companies. They also use machine learning algorithms to validate and update their data in real-time.

## Data available in rocketreach

- **Contact Information** - such as email addresses, phone numbers, and social media profiles.

- **Industry and Sector** - what the company does and the industry they operate in.

- **Revenue and Employee Size** - annual revenue, number of employees, and the company's funding history.

- **Technologies used** - the technologies used by the company on its website, such as analytics and advertising tools.

- **Key People** - executives and employees at the company, with their job titles and contact information.

## Why rocketreach

- **Accurate and up-to-date information :** RocketReach uses advanced algorithms and artificial intelligence (AI) to collect, verify, and update contact information for millions of professionals and businesses. This ensures that the information you get is accurate and up-to-date.

- **Wide coverage :** RocketReach has a large database of over 450 million professionals and 17 million businesses from all around the world. This makes it a one-stop-shop for anyone looking to find contact information for professionals and businesses.

## Difficulites faced in scraping

Rocketreach is a leading website for finding and verifying business email addresses and phone numbers. One of the reasons that Rocketreach stands out from other similar websites is its approach to prevent data scraping. Rather than relying solely on the page source, Rocketreach fetches data directly through API calls and website AJAX, which allows for more reliable and up-to-date information. As a result, the required data is not readily available in the page source, making it necessary to use XPath to directly locate the data and Selenium's WebDriverWait function to ensure the bot waits until the data is available. This approach ensures accurate and up-to-date data retrieval.

## Installing dependecies

    pip install -r requirements.txt

- Place the requirements.txt in the folder and run above code to install the required libraries.

## To run the code

    python scrape_bot.py

**Note** : that the above code may vary according to the IDE you use.

## Working

#### **Fetching the links of every company**

- The bot starts by opening the Rocketreach website using Selenium in incognito mode. the login popup appears so to bypass the login popup, the bot sends the login credentials to the appropriate fields and clicks the login button.

- the popup will appear to install the rocketreach so it is bypassed by skip this step.

- After logging in, the bot selects the "Companies" option to refine the search and get a list of companies.

- The bot then scrapes the href link present in each company section using a loop and appends it to a list. It then clicks the "Next Page" button to move to the next page of search results and repeats the process until it reaches the last page of results.

#### **Getting company information**

#### Basic company information
- The web scraping process involves looping through all the company links present in the list. Firstly, WebDriverWait is used to wait until the page loads and then the table size where all the basic information about the company is located is obtained. However, the website dynamically includes empty rows in between the tables which throws an error that prevents scraping by the bot. To overcome this issue, we have implemented try and except blocks and used all possible XPaths of the table to ensure that the scraping process is not interrupted by these empty rows and  scraped all the available data.

- Then bot press the email format button. 

#### E-Mail Format
- The WebDriverWait is used to make bot wait until the table data is available then get the table size to itterate through to scrap the data.

- Then loop the rows where bot scrap the the possible email formats used by the company employees by combining the first name, last name with common email domains and their percentage of success.

- Then the managment button is pressed.

#### Managment

- In some cases, a popup may appear during the scraping process, so try and except blocks are used to bypass it if it appears.

- The employee names and their designations are scraped, but the webpage structure makes it difficult to iterate through each employee detail by hiding the total number of cells.

- To overcome this issue, the number displayed next to the "Show More" button is used to calculate the total number of employees and iterate through each cell.

#### **Storing it in database**
- all the above data is stored in directories in each iteration which will be then the directories is appended to the table in database.

## Advantage and Future Reusablity

- The free version of RocketReach allows the bot to scrape data from only 2 pages, which limits the amount of company information that can be extracted. However, with a premium account, the bot can scrape all companies' information reliably. With minor changes, the bot can also scrape company information from other regions or countries around the world. This provides a significant advantage for those who require a large amount of company information for their business or research purposes.

#### **Proxy**

- When making around 400,000 requests from the same IP address every day, it is highly likely that the IP will get banned. To prevent this, a rotating proxy has been implemented to send requests with a different IP each time.

- To obtain a list of proxies, an API link is fetched from the geonode website, and the response is a JSON with free proxies.

- Each proxy is tested by sending a request to Google and checking if the webpage loads within 5 seconds. If the proxy works, it is added to the valid_proxies list.

- The bot randomly selects a proxy from the list and passes it to Selenium for every request, so each request is sent from a different IP.

        Note : that due to the low uptime and downtime of free proxies, they may not be reliable. Instead, paid and reliable proxies are recommended for optimal performance. 
        Additionally, the list of proxies can be fetched in real-time during the execution of the bot each day.


