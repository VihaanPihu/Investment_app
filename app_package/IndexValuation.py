import requests
from bs4 import BeautifulSoup
import pandas as pd 


class IndexVal:
    def __init__(self):
        pass

    def topRatios(self,ticker):
        self.ticker=ticker
        url=f"https://www.screener.in/company/{ticker}/consolidated/"
        html_response=requests.get(url)
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
        return top_ratio_df


    def params_plot(self,tickerID,param):
          params = {
        "q": param,
        "days": "365"}
          
          url = f"https://www.screener.in/api/company/{(tickerID)}/chart/"
          headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.screener.in/",
            "Origin": "https://www.screener.in",
            "Content-Type": "application/x-www-form-urlencoded",
             }
          response = requests.get(url, headers=headers, params=params)
          y=response.json()
          data_df=pd.DataFrame(y['datasets'][0]['values'])
          data_df.columns=['Date','Price']
          data_df.set_index('Date',inplace=True)
          data_df['Price']=data_df['Price'].apply(lambda x: float(x))
          data_df["Mean"]=data_df['Price'].mean()

          return data_df

if __name__=="__main__":
    obj=IndexVal()
    print(obj.topRatios("tcs"))