# To Extract data from the given csv file with a list of hotels and calculate NPS,No of Promoters,No of Detractors,
# No of Passive customers, Total count of Customers and the average Rating.
# NPS is given as below

# Promoter Percentage: (Number of Promoters/Total Respondents)x100

# Detractor Percentage: (Number of Detractors/Total Respondents)×100

# NPS=Percentage of Promoters−Percentage of Detractors

# The result will range from -100 to +100.


import pandas as pd

# Step 1: Read the dataset from the CSV file
datapath='C:/Users/Lenovo/Desktop/data/hotel_ratings.csv'
file_path='C:/Users/Lenovo/Desktop/data/hotel_NPS_ratings.csv'

def npsCalculator(df,file_path):
    result=[]
    sub=["Hotel Name" , "NPS" , "No of Promoters", "Percentage of Promoters" , "No of Detractors" ,
         "Percentage of Detractors" , "No of Passives" , "Percentage of Passive", "Total No of Customers" , "Average Rating"]
    result.append(sub)
    uniqueHotels=set (df['Hotel Name'])
    uniqueHotels_list=list(uniqueHotels)
    for i in range(len(uniqueHotels_list)):
        nps=0
        np=0
        nd=0
        nop=0
        count=0
        sumR=0
        AvgRating=0
        sub=[]
        for j in range(len(df)):
            if(uniqueHotels_list[i]==df['Hotel Name'][j]):
                count+=1
                sumR+=df['Rating'][j]
                if(df['Rating'][j]>=9):
                    np+=1
                elif(df['Rating'][j]>=7 and df['Rating'][j]<9):
                    nop+=1
                else:
                    nd+=1
        pnp=round((np/count)*100,2)
        pnd=round((nd/count)*100,2)
        pnop=round((nop/count)*100,2)
        nps=int(round((pnp-pnd),0))
        AvgRating=float(round(sumR/count,1))
        sub.append(uniqueHotels_list[i])
        sub.append(nps)
        sub.append(np)
        sub.append(pnp)
        sub.append(nd)
        sub.append(pnd)
        sub.append(nop)
        sub.append(pnop)
        sub.append(count)
        sub.append(AvgRating)
        result.append(sub)
    df = pd.DataFrame(result[1:], columns=result[0])
    df.to_csv(file_path , index=False)


################Main Code###################################

try:
    if(len(file_path)!=0 and len(datapath)!=0):
        df = pd.read_csv(datapath)
        if(len(df)>1):
            npsCalculator(df,file_path)
            print("Data Collection Successful")
        else:
            print("The Data set is empty")
    else:
        raise Exception("The Input is Invalid Please check")
except Exception as e:
    print(e)
