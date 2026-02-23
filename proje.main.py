from pathlib import Path 
import json
import random
import string
class bank:
    database = "data.json"
    data = [] # ye data json mai save hoga 

    try:
        if Path(database).exists():
            print("file Exists..")
            with open(database) as fs:
                data = json.loads(fs.read())

        else:
            print("no such file exists...")

    except Exception as err:
        print("Error Occured")  


             
#creat user 

    @classmethod
    def update(cls):
        with open(bank.database,'w')as fs:
            fs.write(json.dumps(cls.data))

    @staticmethod
    def generateAcc():
        digits = random.choices(string.digits,k=4) 
        alpha = random.choices(string.ascii_letters,k=4) 
        id = digits+alpha
        random.shuffle(id)
        return " ".join(id)

    def creatAccount(self):
        info = { 
            'name': input('Enter your name:  '),
            'age' :int(input("Enter your Age..")),
            'email': input('enter your email: '),
            'pin':int(input('enter your pin:  ')),
            'Account': bank.generateAcc(),
            'balance':0,
            'mobile_no': int(input("Enter your moble_no"))
        }
        if info['age']>18 and len(str(info['pin'])) == 4 and len(str(info['mobile_no'])) == 10:
            bank.data.append(info)
            bank.update()
            print('data added in list')
        else:
            print("Credintials are not valid")    
            print(bank.data)
    def depositemoney(self):
        accountno=input("enter your account no.  ")
        pin=(int(input("enter your 4 digit pin.  ")))

        user_data = [i for i in bank.data if i ['Account']==accountno and i['pin']==pin ] 
        if user_data == False:
            print("user not found") 
        else:
            amount = int(input("paisa"))
            if amount <= 0:
                print("Invailed Amount") 
            elif amount >10000:
                print("Greter than 10000")
            else:
                user_data[0]['balance'] +=amount
                bank.update()
                print('Amount credited')             
    def withdrawmoney(self):    
         accountno=input("enter your account no.  ")
         pin=(int(input("enter your 4 digit pin.  ")))

         user_data = [i for i in bank.data if i ['Account']==accountno and i ['pin']==pin]
         if user_data == False:
            print("user not found") 
         else:
            amount = int(input("paisa"))
            if amount <= 0:
                print("Invailed Amount") 
            elif amount >10000:
                print("Amount exceeds 10000")
            else: 
                user_data[0]['balance'] -=amount
                bank.update()
                print('Amount debited')  



    def details(self):
        accountno=input("enter your account no.  ")
        pin=(int(input("enter your 4 digit pin.  ")))

        user_data = [i for i in bank.data if i ['Account']==accountno and i ['pin']==pin]
        if user_data == False:
            print('User not found')
        #     print(user_data)
        # else:
        #     balance = int(input('Amount:  '))
        #     user_data[0]['balance'] +=balance
        else:
            print(user_data)  


    def update(self):
            accountno=input("enter your accountno: ")
            pin = int(input('Enter your 4 digit pin: '))

            user_data = [i for i in bank.data if i['accountno.']==accountno and i['pin']==pin]  
            if user_data == False:
                print("user not found") 
            else:
                print('Aap Account No. aur Balance Update/Change nahi kar sakte ho')

                print("Enter your details to update or just press enter to skip them")

            new_data = {
            "name":input("please tell your name: "),
            "email":input("please tell your mail: "),
            "phone no.":int(input("Tell your phone number")),
            "pin":int(input("please tell your pin (4 digit)"))
        }  
            if new_data['name'] == "":
              new_data['name'] = user_data[0]['name']

            if new_data['email'] == "":
              new_data['email'] = user_data[0]['email']

            if new_data['phone no.'] == "":
              new_data['phone no.'] = user_data[0]['phone no.']
            else:
              new_data["phone no."] = int(new_data['phone no.'])    

            if new_data['pin'] == "":
               new_data['pin'] = user_data[0]['pin'] 
            else:
              new_data["pin."] = int(new_data['pin.'])

            new_data['Account No. '] == user_data[0]['Account No. ']
            new_data['balance'] = user_data[0]['balance']
        
            user_data[0].update(new_data)
            bank.update()    


    def delet(self):
      accountno=input("enter your account no.  ") 
      pin=(int(input("enter your 4 digit pin.  ")))

      user_data = [i for i in bank.data if i ['Account']==accountno and i ['pin']==pin]
      if user_data == False:         
          print("no such user exists")

      else:
          print("are you sure you went to delet your Account ? (yes/no)")
          choice = input()
          if choice == "yes":
              ind = bank.data.index(user_data[0])
              bank.data.pop(ind) 
              bank.update()
              print("Account deleted successfully")
          else:
              print("operation terminated")        

obj=bank()
obj.update()
print("press 1 for creating Account")
print("press 2 for deposting money")
print("press 3 for withdrawing Account")
print("press 4 for Account details")
print("press 5 for updating Account Details")
print("press 6 for deleting Account")
# choice = int(input("enter your choice"))
# if choice == 1:
#     obj.creatAccount()

# elif choice == 2:
#     obj.depositemoney()

# elif choice == 3:
#     obj.withdrawmoney()

# elif choice == 4:
#     obj.details()

# elif choice == 5:
#     obj.update()

# elif choice == 6:
#     obj.delet()   


#obj.creatAccount()
#obj.depositmoney()
# obj.withdrawmoney()
# obj.details()









# obj.show()     
# obj.update()   


 

#read 
#update
#delete
   
