from enum import IntEnum
from typing import List, Optional
from fastapi import FastAPI,HTTPException # like previously in code we were sometime returning strings that is not accurate so we will now return the http exception
from pydantic import BaseModel, Field  


api = FastAPI()   #so here we defined the api

class Priority(IntEnum): #this is we making the priority system
     LOW = 3
     MEDIUM = 2
     HIGH = 1


class TodoBase(BaseModel): # inpydantic basemodel is used to define any schema
     todo_name : str = Field(..., min_length=3, max_length=512, description='descriptionof the todo')  #not for openai stuff or any llm, ... represent reqd field
     todo_description : str = Field(...,  description='todosescription')
     priority : Priority = Field(default=Priority.LOW, description='priority of the todo')



class TodoCreate(TodoBase):  # we need todobase to create todo
     pass
   

class Todo(TodoBase):  #this is  a response like it will like give todo base stuff with id  
     todo_id : int = Field(..., description='unique identification id')


class TodoUpdate(BaseModel): #we are using optional as like we might or might not wanna update it and for updating it necessary to make default value none    
     todo_name : Optional[str] = Field(None, min_length=3, max_length=512, description='descriptionof the todo')  #not for openai stuff or any llm, ... represent reqd field
     todo_description : Optional[str] = Field(None,  description='todosescription')
     priority : Optional[Priority] = Field(None, description='priority of the todo')     






# this will be our simulated database updated
all_todos = [
    Todo(todo_id=1, todo_name="Clean house", todo_description="Cleaning the house thoroughly", priority=Priority.HIGH),
    Todo(todo_id=2, todo_name="Sports", todo_description="Going to the gym for workout", priority=Priority.MEDIUM),
    Todo(todo_id=3, todo_name="Read", todo_description="Read chapter 5 of the book", priority=Priority.LOW),
    Todo(todo_id=4, todo_name="Work", todo_description="Complete project documentation", priority=Priority.MEDIUM),
    Todo(todo_id=5, todo_name="Study", todo_description="Prepare for upcoming exam", priority=Priority.LOW)
]

#GET,POST,PUT,DELETE --- get to get, post to post, put means replacing , deleting is deleting


# @api.get('/todos')
# def get_todos():
#      return all_todos

@api.get('/todos/{todo_id}', response_model=Todo) # we here had created an reponse model here that will give us todo class data like specific todo id
def get_todo(todo_id : int):           
      for todo in all_todos:
           if todo.todo_id == todo_id:
                return todo
      raise HTTPException(status_code=404, detail='todo not found')
         


@api.get('/todos', response_model=List[Todo])
def get_todos(first_n : int | None = None):
     if first_n:
          return all_todos[:first_n]  # so this like a mini forloop like up until the specified index all data will be printed
     else:
          return all_todos
     
#so now we will be creating the post endpoint but without using pydantic
#so by default there is we have endpoint /docs to perform the post request
@api.post('/todos', response_model=Todo)
def create_todo(todo: TodoCreate): # so now our hinting is directly to class to make new todo 
     new_todo_id  = max(todo.todo_id for todo in all_todos) + 1

     new_todo = Todo(
          todo_id = new_todo_id,
          todo_name = todo.todo_name,
          todo_description = todo.todo_description,
          priority = todo.priority)
     

     all_todos.append(new_todo)
     return new_todo

# below is not good code
#here is the put operation for the endpoint keep in mind up until now we havent used any pydantic only typehinting
@api.put('/todos/{todo_id}', response_model=Todo)
def update_todo(todo_id: int, updated_todo:TodoUpdate):
     for todo in all_todos:
          if todo.todo_id == todo_id:
              if updated_todo.todo_name is not None:                
                todo.todo_name = updated_todo.todo_name
              if updated_todo.todo_description is not None:                    
                todo.todo_description = updated_todo.todo_description    #focus on name while programming
              if updated_todo.priority is not None:                   
                todo.priority = updated_todo.priority
                return todo
     raise HTTPException(status_code=404,detail='to do not founc')


@api.delete('/todos/{todo_id}', response_model=Todo)
def delete_todo(todo_id : int):
     for index, todo in enumerate(all_todos):
          if todo.todo_id == todo_id:
               deleted_todo = all_todos.pop(index)
               return deleted_todo
    #  return "error not found"
     raise HTTPException(status_code=404, detail='todo not found')
               
