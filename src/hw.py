from fastapi import FastAPI
# so in this like type hinting is very much important
# so this is our basics like localhost:9999 'we are running here'
# / is our index
#/todos are our like all todos
# /todos/2 is our endpoint with the id like /todos/{2} in code but in real just 2 
#then comes the query parameter --> like
# --> for eg localhost:9999//todos?first_n=3 here from question mark we are providing our query parameter here we are specifying first n == 3

#creating first api

api = FastAPI()   #so here we defined the api


# this will be our simulated database
all_todos : list = [
    {'todo_id':1, 'todo_name':'Sports', 'todo_description': 'Go to the gym'},
    {'todo_id':2, 'todo_name':'Read', 'todo_description': 'Read 10 pages'},
    {'todo_id':3, 'todo_name':'Shop', 'todo_description': 'Go shopping'},
    {'todo_id':4, 'todo_name':'Study', 'todo_description': 'study for exam'},
    {'todo_id':5, 'todo_name':'Meditate', 'todo_description': 'meditate 20 mins'},
]

#GET,POST,PUT,DELETE --- get to get, post to post, put means replacing , deleting is deleting


@api.get('/')   #this is self explanatory like we are passong the path and using get method to retrieve
def index():
    return {'message' : 'world'}  #here we returning json msg

# @api.get('/todos')
# def get_todos():
#      return all_todos

@api.get('/todos/{todo_id}')  #here you can see that / is a path and the defined in this -> {} is a our path parameter
def get_todo(todo_id : int):           #if we had the real database we could have used async progarmming
      for todo in all_todos:
           if todo['todo_id'] == todo_id:
                return {'result':todo}
#by default our int was considered str so we have to use here type hinting          
@api.get('/todos')
def get_todos(first_n : int | None = None):
     if first_n:
          return all_todos[:first_n]  # so this like a mini forloop like up until the specified index all data will be printed
     else:
          return all_todos
     
#so now we will be creating the post endpoint but without using pydantic
#so by default there is we have endpoint /docs to perform the post request
@api.post('/todos')
def create_todo(todo: dict):
     new_todo_id  = max(todo['todo_id'] for todo in all_todos) + 1

     new_todo = {
          'todo_id' : new_todo_id,
          'todo_name' : todo['todo_name'],
          'todo_description' : todo['todo_description']

     }

     all_todos.append(new_todo)
     return new_todo

# below is not good code
#here is the put operation for the endpoint keep in mind up until now we havent used any pydantic only typehinting
@api.put('/todos/{todo_id}')
def update_todo(todo_id: int, updated_todo:dict):
     for todo in all_todos:
          if todo['todo_id'] == todo_id:
               todo['todo_name'] = updated_todo['todo_name']
               todo['todo_description'] = updated_todo['todo_description']
               return todo
     return "not found"


@api.delete('/todos/{todo_id}')
def delete_todo(todo_id : int):
     for index, todo in enumerate(all_todos):
          if todo['todo_id'] == todo_id:
               deleted_todo = all_todos.pop(index)
               return deleted_todo
     return "error not found"
               
