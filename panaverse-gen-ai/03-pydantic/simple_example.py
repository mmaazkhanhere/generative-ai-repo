from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    account_id: int
    
user = User(name='Maaz', email='maaz@gmail.com', account_id = 5)
print(user)

#user = User(name='Maaz', email='maaz@gmail.com', account_id = 'Hello')

user = User(name='Maaz', email='maaz@gmail.com', account_id = '5')
print(user)
print(user.account_id)