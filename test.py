import pandas as pd
from data_cleaning import overall_summary

df = pd.read_csv("./data/data.csv")
print(overall_summary)

'''
31/10/2026,Spin,1.25,Yes,Stockport,Yes,80.68
31/10/2026,Rambo,1.571,Yes,Wycombe,Yes,80.68
31/10/2026,Beth,1.571,Yes,Port Vale,80.68
31/10/2026,Grizz,1.2,Yes,Middlesborough,80.68
31/10/2026,Zed,1.571,Yes,Wolves,80.68
07/11/2026,Spin,1.571,No,Hamilton
07/11/2026,Rambo,1.111,Yes,Arsenal
07/11/2026,Beth,1.25,Yes,Colchester
07/11/2026,Grizz,1.2,Yes,Barnsley
07/11/2026,Zed,1.4,No,Middlesborough
'''