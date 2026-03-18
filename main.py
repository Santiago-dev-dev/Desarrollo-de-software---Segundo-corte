from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def mensaje():
    return "Bienvenido a FastAPI Ingenieros de Sistemas"

@app.get('/{nombre}/{codigo}')
def mensaje_2(nombre:str, codigo:int):
    return f"Bienvenido {nombre}, código {codigo} a FastAPI Ingenieros de Sistemas"

@app.get('/uno/')
def mensaje_3(edad:int, nombre_2:str):
    return f"Hola {nombre_2} Su edad es: {edad}"

