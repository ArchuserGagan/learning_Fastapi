from typing import Any

from fastapi import FastAPI, HTTPException, Depends
import uvicorn

api = FastAPI()


#this can really become an dashboard

users = [
    {"name": "Ore", "password": "jkzvdgwya12"},
    {"name": "Uche", "password": "lga546"},
    {"name": "Seke", "password": "SK99!"},
    {"name": "Afi", "password": "Afi@144"},
    {"name": "Sam", "password": "goTiger72*"},
    {"name": "Ozi", "password": "xx%hI"},
    {"name": "Ella", "password": "Opecluv18"},
    {"name": "Claire", "password": "cBoss@14G"},
    {"name": "Sena", "password": "SenDaBoss5"},
    {"name": "Ify", "password": "184Norab"}  
]

#dependency using class for like user authentication

class UserAuth():
    def __init__(self, name:str, password:str) -> None:
        self.name = name
        self.password = password


    def __call__(self):
        #we are  checking here that if given name and pass corresponding with the  our given data
        for user in users:
            if user["name"] == self.name and user["password"] == self.password:
                pass
            #if no match found , raise an error

            raise HTTPException(status_code=401, detail='invalid user')
#  Note that __call__ doesn't return a value in this example. It simply raises an HTTPException if authentication fails. 
# The __call__ method makes the class instance callable, allowing FastAPI to invoke it like a regular function.       
#Injecting the class dependency into a path operation
@api.get("/user/dashboard")
def get_dashboard(user: UserAuth = Depends(UserAuth)):
    return {"message": f"Access granted to {user.name}"}



    

##this down here is all about functional dependency
# '''
# # this is the dependency function
# def user_dep(name:str, password:str):
#     for u in users:
#         if u["name"] == name and u["password"] == password:
#             return {'name' : name, 'valid': True}
        



# #now i will make the get api point


# @api.get("/users/{user}")
# def get_user(user = Depends(user_dep)) -> dict:
#     if not user:
#         raise HTTPException(status_code=401, detail='invalid user')
#     return user
# '''


    
