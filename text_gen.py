from embedding import search_query
from transformers import pipeline

from datetime import date





# model list 
##  - Qwen/Qwen-VL-Cha
##  - vinai/PhoGPT-4B-Chat 
##  - openai-community/gpt2
##  - NlpHUST/gpt2-vietnamese



if __name__ == '__main__':
    query ="Tôi nhiều lông quá, có sản phẩm nào triệt lông không?"
    docs = search_query(query)
    with open("conversation.txt", "a", encoding='utf-8') as f:
        f.write('-----------------------------------\n')
        f.write("Conversation:"+ date.today().strftime("%d/%m/%Y") + "\n")
        f.write(f"Question: {query}\n")
    generator = pipeline("text-generation", model="NlpHUST/gpt2-vietnamese",trust_remote_code=True)
    
    result = []
    
    for i, doc in enumerate(docs):
        _name = doc["name"]
        if not _name:
            continue
        res = generator("Thông tin sản phẩm: "+ doc["name"], max_length=300, num_return_sequences=1)
        result.append("Tên sản phẩm: " + _name + "\n"+ "" + res[0]["generated_text"] + "\n")
        with open("conversation.txt", "a", encoding='utf-8') as f:
            f.write("Answer - "+ str(i)+ ":\n")
            f.write(result[i])
        print(result[i])
    # res = generator("Đặc trị mụn viêm, bọc, mủ cao cấp", max_length=200, num_return_sequences=5)
    
    # print(res)
    