import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua=UserAgent()
headers = {'User-Agent': ua.random}

class Screener:
    def __init__(self,ticker):
        self.ticker=ticker
        self.tickerId=0

    def top_ratio(self):
        
        url=f"https://www.screener.in/company/{self.ticker}/consolidated/"
        html_response=requests.get(url,headers=headers)
        soup=BeautifulSoup(html_response.text,'html.parser')

        ratio_params={"Ratio":[],"Value":[]}
        ratios=soup.find_all('ul' ,id="top-ratios")
        for i in ratios[0].find_all('span',class_="name"):
            if (i.text).strip()=='High / Low':
                ratio_params["Ratio"].append("High")
                ratio_params["Ratio"].append("Low")
                continue
            ratio_params["Ratio"].append((i.text).strip())

        for j in ratios[0].find_all('span',class_="number"):
            ratio_params["Value"].append(((j.text).strip()))
        top_ratio_df=pd.DataFrame(ratio_params)

        #api code

        x=soup.find_all("div",class_='flex flex-align-center gap-8')[0]
        x=(str(x))
        for i in x.split("/"):
            if i.isdigit():
                self.tickerId=i
        return top_ratio_df

    def high_delivery(self):
        pass






if __name__=="__main__":
    obj=Screener("tcs")
    print(obj.top_ratio())
    print(obj.high_delivery())