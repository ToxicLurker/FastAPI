

#     id TEXT,
#     first_name TEXT,
#     second_name TEXT,
#     age TEXT,
#     birthdate TEXT,
#     biography TEXT,
#     city TEXT,
#     hashed_password TEXT,
#     disabled TINYINT



# Абрамов Роберт,11,Воткинск


import pandas as pd
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# pwd_context.hash(password)

data = pd.read_csv('people.csv', header=0, names=['full_name', 'age', 'city'])
print(1)
data['id'] = data["full_name"]
print(2)
data['first_name'] = data["full_name"].apply(lambda x: x.split()[0])
print(3)
data['age'] = data["age"].astype(str)
data['second_name'] = data["full_name"].apply(lambda x: x.split()[1])
print(4)
data['birthdate'] = "NULL"
print(5)
data['biography'] = "NULL"
print(6)
data['disabled'] = 0
print(7)
hash_pass = pwd_context.hash('1')
data['hashed_password'] = hash_pass
print(8)
new_data = pd.DataFrame(data=[], columns=["id","first_name" ,"second_name" ,"age" ,"birthdate" ,"biography" ,"city" ,"hashed_password" ,"disabled"])

print(data[["id","first_name" ,"second_name" ,"age" ,"birthdate" ,"biography" ,"city" ,"hashed_password" ,"disabled"]].iloc[:,:10])

print(data.info())

data[["id","first_name" ,"second_name" ,"age" ,"birthdate" ,"biography" ,"city" ,"hashed_password" ,"disabled"]].to_csv('new_people.csv', index=False, encoding='utf-8')


