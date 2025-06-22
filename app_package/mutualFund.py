from mftool import Mftool
import pandas as pd
mft=Mftool()

class MF():
    def __init__(self):
        self.text=""

    def addMF(self,text):
        self.text=text
        with open(r"mf_list.txt","a") as f:
            f.write(self.text)
            f.write("\n")

    def readMF(self):
        with open(r"mf_list.txt","r") as f:
            mf_list=f.readlines()
            return mf_list
        
    def mfSchemeDetails(self,schemecode):
        self.schemecode=schemecode
        return mft.get_scheme_quote(self.schemecode)
    
    def get_historicalData(self,schemecode):
        self.schemecode=schemecode
        mf_df=mft.get_scheme_historical_nav(self.schemecode,as_Dataframe=True)
        mf_df["nav"]=mf_df["nav"].astype(float)
        mf_df.index=pd.to_datetime(mf_df.index,dayfirst=True)
        mf_df.sort_index(inplace=True)
        mf_df["44 DMA"]=mf_df["nav"].rolling(window=100).mean()
        return (mf_df.iloc[-252:,:])
    

if __name__=="__main__":
    obj=MF()
    print(obj.mfSchemeDetails(101672))
    print(obj.get_historicalData(101672))
    
