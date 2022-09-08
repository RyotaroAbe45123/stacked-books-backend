from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import user, stack, book


app = FastAPI()
app.include_router(user.router)
app.include_router(stack.router)
app.include_router(book.router)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# @app.get("/users/find")
# def get_one_user(user_id: int):
#     # int以外リクエストされないはずだが、バリデーション
#     if not isinstance(user_id, int): return "Invalid Input Type Error"
#     result = find_user(user_id)
#     return result

# @app.get("/users")
# def get_all_users():
#     query = "select * FROM Users"
#     result = find_users(query)
#     return result

# @app.post("/users")
# def create_user(name: str):
#     # str以外リクエストされないはずだが、バリデーション
#     if not isinstance(name, str): return "Invalid Input Type Error"
#     create_user_record(name)
    
    
# @app.post("/users/delete")
# def delete_user(user_id: int):
#     # int以外リクエストされないはずだが、バリデーション
#     if not isinstance(user_id, int): return "Invalid Input Type Error"
#     delete_user_record(user_id)
    

# @app.post("/stacks")
# def create_stack(user_id: int, isbn: int):
#     if not (isinstance(user_id, int) and isinstance(isbn, int)): return "Invalid Input Type Error"
#     create_stack_record(user_id, isbn)

# @app.post("/stacks/delete")
# def delete_stack(user_id: int, isbn: int):
#     if not (isinstance(user_id, int) and isinstance(isbn, int)): return "Invalid Input Type Error"
#     delete_stack_record(user_id, isbn)

# @app.get("/stacks/find")
# def get_all_stacks_by_user(user_id: int):
#     # int以外リクエストされないはずだが、バリデーション
#     if not isinstance(user_id, int): return "Invalid Input Type Error"
#     result = get_stacks(user_id)
#     return result

# @app.get("/stacks/num")
# def get_stacks_num_by_user(user_id: int):
#     # int以外リクエストされないはずだが、バリデーション
#     if not isinstance(user_id, int): return "Invalid Input Type Error"
#     result = get_stacks_num(user_id)
#     return result


# @app.post("/books")
# def create_books(isbn: int):
#     # int以外リクエストされないはずだが、バリデーション
#     if not isinstance(isbn, int): return "Invalid Input Type Error"
#     create_book_record(isbn)

# @app.post("/books/delete")
# def delete_books(isbn: int):
#     # int以外リクエストされないはずだが、バリデーション
#     if not isinstance(isbn, int): return "Invalid Input Type Error"
#     delete_book_record(isbn)

# @app.get("/books/find")
# def get_books(user_id: int):
#     # int以外リクエストされないはずだが、バリデーション
#     if not isinstance(user_id, int): return "Invalid Input Type Error"
#     result = get_books_by_user(user_id)
#     return result

