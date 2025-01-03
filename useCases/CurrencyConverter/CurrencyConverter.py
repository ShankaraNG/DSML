# We need to scrape the list of books and availability along with the price and converter the price according to the currency of that country
# based on the user request


import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import pandas as pd

#base_url = "https://books.toscrape.com/"
########URL to Scrape###############
base_url = "https://books.toscrape.com/catalogue/category/books_1/page-1.html"
#######Path for the extraction###########
file_path = 'C:/Users/Lenovo/Desktop/data/books_inventory.xlsx'


############This is to red from the website and add the data###################################
def webReader(base_url,symbol,currency,sf,file_path):
    source_url=base_url
    result=[]
    ################Header Section#################################
    sub=['Book Name', 'Price in {}'.format(sf) , 'Availability']
    result.append(sub)
    ##############NOTE We are scraping the data 50 times because there are 50 pages in the website###########################
    for i in range(1,51,1):
        home_page = requests.get(base_url)
        if home_page.status_code == 200:
            home_page = requests.get(base_url)
            soup = BeautifulSoup(home_page.content,"html.parser")
            firstbook = soup.find_all(name = "li", class_= "col-xs-6 col-sm-4 col-md-3 col-lg-3")
            for i in range(len(firstbook)):
                sub=[]
                #pricetag=firstbook[i].find(name= "p", class_="price_color").get_text().strip()
                #####################Extracting the Data#######################
                title=firstbook[i].find(name= "h3").find('a')['title'].strip()
                price = float(re.sub(r'[^\d.]', '', firstbook[i].find(name= "p", class_="price_color").get_text().strip()))*currency
                pricetag="{}{:.2f}".format(symbol, price)
                status=firstbook[i].find(name= "p", class_="instock availability").get_text().strip()
                sub.append(title)
                sub.append(pricetag)
                sub.append(status)
                result.append(sub)           
        else:
            print(f"Failed, status code: {home_page.status_code}")
            break
    ####################Inserting the data to Excel sheet##############################
    df = pd.DataFrame(result[1:], columns=result[0])
    df.to_excel(file_path , index=False, engine='openpyxl')
        
   
    
##########To take the conversion factor required for the data############################
def CurrencyConverter(base_url,cur,file_path):
    x=None
    y=None
    sf=None
    currency={"USD": 1.23,
              "GBP": 1.00,
              "EUR": 1.13,
              "JPY": 165.00,
              "CHF": 1.11,
              "CAD": 1.50,
              "AUD": 1.85,
              "INR": 101.00,
              "CNY": 9.50,
              "BRL": 6.10,
              "ZAR": 23.00,
              "RUB": 96.00,
              "MXN": 24.00,
              "SGD": 1.64,
              "NZD": 1.95,
              "HKD": 9.30,
              "TRY": 29.00,
              "IDR": 17500.00,
              "SAR": 4.50,
            }
    symbol={"USD": "$",
            "GBP": "£",
              "EUR": "€",
              "JPY": "¥",
              "CHF": "CHF",
              "CAD": "CA$",
              "AUD": "AU$",
              "INR": "₹",
              "CNY": "CNY¥",
              "BRL": "R$",
              "ZAR": "R",
              "RUB": "₽",
              "MXN": "MX$",
              "SGD": "S$",
              "NZD": "NZ$",
              "HKD": "HK$",
              "TRY": "₺",
              "IDR": "Rp",
              "SAR": "ر.س",
            }
    for key, value in currency.items():
        if(key==cur):
            sf=key
            x=value
            break
    
    for key, value in symbol.items():
        if(key==cur):
            y=value
            break
    webReader(base_url,y,x,sf,file_path)

#########################################Main Method##################################

currency_dict = {
    "Currency":"Currency-Code",
    "British Pound":"GBP",
    "United States Dollar": "USD",
    "Euro": "EUR",
    "Japanese Yen": "JPY",
    "Swiss Franc": "CHF",
    "Canadian Dollar": "CAD",
    "Australian Dollar": "AUD",
    "Indian Rupee": "INR",
    "Chinese Yuan": "CNY",
    "Brazilian Real": "BRL",
    "South African Rand": "ZAR",
    "Russian Ruble": "RUB",
    "Mexican Peso": "MXN",
    "Singapore Dollar": "SGD",
    "New Zealand Dollar": "NZD",
    "Hong Kong Dollar": "HKD",
    "Turkish Lira": "TRY",
    "Indonesian Rupiah": "IDR",
    "Saudi Riyal": "SAR"
}

for key, value in currency_dict.items():
    print("{}\t\t\t:\t\t{}".format(key,value))
    
cur=input("Enter the Currency Code from the above menu ").upper()
pattern = r"^https://.*\.com"
pattern2= r".*\.xlsx$"
try:
    if(len(base_url)!=0 and bool(re.match(pattern, base_url)) and len(file_path)!=0 and bool(re.match(pattern2, file_path))):
        if(len(cur)==3 and cur in currency_dict.values()):
            try:
                home_page = requests.get(base_url)
                if home_page.status_code == 200:
                    CurrencyConverter(base_url,cur,file_path)
                    print("Extraction Successfull")
                    print("Please check in the path {}".format(file_path))
                else:
                    raise Exception("Failed unable to access the URL, status code: {}".format(home_page.status_code))
            except Exception as e:
                print(e) 
        else:
            print("Wrong Currency Code")
    else:
        raise Exception("Invalid Path or URL Please check")
except Exception as e:
    print(e)

      

