#codeรอปรับให้เข้ากับ project
#Import Library
import json
import os
from flask import Flask
from flask import request
from flask import make_response

#ส่วนของการเก็บข้อมูล
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
cerds = ServiceAccountCredentials.from_json_keyfile_name("cerds.json", scope)
client = gspread.authorize(cerds)
sheet = client.open("chatbot").worksheet('sheet1') # เป็นการเปิดไปยังหน้าชีตนั้นๆ
#-------------------------------------

#----เชื่อมต่อfirebase----
from random import randint
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate("chatbot-garem-firebase-adminsdk-bufga-83c907a691.json")
firebase_admin.initialize_app(cred)
#-------------------------------------

# Flask
app = Flask(__name__)
@app.route('/', methods=['POST']) 

def MainFunction():

    #รับ intent จาก Dailogflow
    question_from_dailogflow_raw = request.get_json(silent=True, force=True)

    #เรียกใช้ฟังก์ชัน generate_answer เพื่อแยกส่วนของคำถาม
    answer_from_bot = generating_answer(question_from_dailogflow_raw)
    
    #ตอบกลับไปที่ Dailogflow
    r = make_response(answer_from_bot)
    r.headers['Content-Type'] = 'application/json' #การตั้งค่าประเภทของข้อมูลที่จะตอบกลับไป

    return r

def generating_answer(question_from_dailogflow_dict):

    #Print intent ที่รับมาจาก Dailogflow
    print(json.dumps(question_from_dailogflow_dict, indent=4 ,ensure_ascii=False))

    #เก็บต่า ชื่อของ intent ที่รับมาจาก Dailogflow
    intent_group_question_str = question_from_dailogflow_dict["queryResult"]["intent"]["displayName"] 

    #ลูปตัวเลือกของฟังก์ชั่นสำหรับตอบคำถามกลับ
    if intent_group_question_str == 'หิวจัง':
        answer_str = menu_recormentation()
    elif intent_group_question_str == 'คำนวนน้ำหนัก': 
        answer_str = BMI(question_from_dailogflow_dict)
    else: answer_str = "ผมไม่เข้าใจ คุณต้องการอะไร"

    #สร้างการแสดงของ dict 
    answer_from_bot = {"fulfillmentText": answer_str}
    
    #แปลงจาก dict ให้เป็น JSON
    answer_from_bot = json.dumps(answer_from_bot, indent=4) 
    
    return answer_from_bot

def menu_recormentation(): #ฟังก์ชั่นสำหรับเมนูแนะนำ
    database_ref = firestore.client().document('Food/Menu_List')
    database_dict = database_ref.get().to_dict()
    database_list = list(database_dict.values())
    ran_menu = randint(0, len(database_list)-1)
    menu_name = database_list[ran_menu]
    #-------------------------------------
    answer_function = menu_name + ' สิ น่ากินนะ'
    return answer_function

def BMI(respond_dict): #ฟังก์ชั่นสำหรับคำนวนน้ำหนัก

    #เก็บค่าของ Weight กับ Height
    weight1 = float(respond_dict["queryResult"]["outputContexts"][1]["parameters"]["Weight.original"])
    height1 = float(respond_dict["queryResult"]["outputContexts"][1]["parameters"]["Height.original"])
    #เพิ่มเติม
    sheet.insert_row([weight1, height1], 2)
    
    #คำนวนน้ำหนัก
    BMI = weight1/(height1/100)**2
    if BMI < 18.5 :
        answer_function = "ผอมจัง"
    elif 18.5 <= BMI < 23.0:
        answer_function = "สมส่วน"
    elif 23.0 <= BMI < 25.0:
        answer_function = "ค่อนข้างอ้วน"
    elif 25.0 <= BMI < 30:
        answer_function = "อ้วนล่ะนะ"
    else :
        answer_function = "อ้วนมากจ้าา"
    return answer_function

#Flask
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0', threaded=True)
