# import firebase_admin
from firebase import firebase

firebase = firebase.FirebaseApplication("https://chatbot-fur-default-rtdb.asia-southeast1.firebasedatabase.app/",None)
firebase.delete('dbcustomer/customer/', '-Mw1A556JXbVqUXwk9j3')
print('recorde has been delete')