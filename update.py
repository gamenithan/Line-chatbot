# import firebase_admin
from firebase import firebase

firebase = firebase.FirebaseApplication("https://chatbot-fur-default-rtdb.asia-southeast1.firebasedatabase.app/",None)
firebase.put('dbcustomer/customer/-Mw1A556JXbVqUXwk9j3','email','test@gmail.com')
print('recorde update')