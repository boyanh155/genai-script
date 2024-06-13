import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv("./data-set/Content Website - DỊCH VỤ.csv")


#  print each row 
# for index, row in data.iterrows():
#     print(row)
    
# print(data.isnull().sum())
# print(data.info()) 

data = data[['NHÓM DỊCH VỤ', 'TÊN DỊCH VỤ', 'GIÁ', 'THÔNG TIN MÔ TẢ',
       'CÁC BƯỚC THỰC HIỆN', 'DANH SÁCH BÁC SĨ CỦA DỊCH VỤ']]
data["tag"] = data["NHÓM DỊCH VỤ"] + " " + data["THÔNG TIN MÔ TẢ"] + " " + data["CÁC BƯỚC THỰC HIỆN"] 


data = data.drop(columns=['NHÓM DỊCH VỤ', 'THÔNG TIN MÔ TẢ', 'CÁC BƯỚC THỰC HIỆN'])
# print(data)

cv=  CountVectorizer(max_features=10000, stop_words='english', )

_fit = cv.fit_transform(data["tag"].values.astype('U')).toarray()


print(_fit)
# print(len(_fit))
print(_fit.shape)
cosine_similarity = cosine_similarity(_fit)


