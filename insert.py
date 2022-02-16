# import firebase_admin
from firebase import firebase

firebase = firebase.FirebaseApplication("https://chatbot-fur-default-rtdb.asia-southeast1.firebasedatabase.app/",None)
mydata = {
    'fname':'nithan',
    'lname':'subkaewyod',
    'email':'game9794@gmail.com',
    'phone':'0970850775'
}

result = firebase.post('dbcustomer/customer',mydata)

print(result)