from pymongo import MongoClient

# ส่วนเชื่อมต่อกับdatabase
client = MongoClient('localhost', 27017)
db = client.mydatabase # ชื่อ DB -> mydatabase
tb = db['tweet'] # ชื่อ table -> word

# ดึงข้อมูลมาจากmongoDB โดยสามารถระบุได้ว่าอยากได้ข้อมูลไหน ถ้าไม่ระบุจะดึงทั้งหมด
listDict = tb.find_one()

# print(listDict) # เช็คข้อมูล เอาออกได้