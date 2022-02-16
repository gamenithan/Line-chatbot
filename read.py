# import firebase_admin
from firebase import firebase

firebase = firebase.FirebaseApplication("https://chatbot-fur-default-rtdb.asia-southeast1.firebasedatabase.app/",None)
result = firebase.get('dbcustomer/customer','')
print(result['-Mw1A556JXbVqUXwk9j3']['email'])