from fastapi import FastAPI, Body

app = FastAPI()

productos = [{
    "Código"    :1,
    "Nombre"    :"Esfero",
    "Valor"     :3500,
    "Existencias"   :10
},
{
    "Código"    :2,
    "Nombre"    :"Cuaderno",
    "Valor"     :5000,
    "Existencias"   :15
},
{
    "Código"    :3,
    "Nombre"    :"Lápiz",
    "Valor"     :200,
    "Existencias"   :12
}]



@app.get('/')
def mensaje():
    return "Bienvenido a FastAPI Ingenieros de Sistemas"

#@app.get('/{nombre}/{codigo}')
#def mensaje_2(nombre:str, codigo:int):
#    return f"Bienvenido {nombre}, código {codigo} a FastAPI Ingenieros de Sistemas"


@app.get('/uno/')
def mensaje_3(edad:int, nombre_2:str):
    return f"Hola {nombre_2} Su edad es: {edad}"


@app.get('/productos')
def listProductos():
    return productos

@app.get('/productos/{cod}')
def findProducto(cod:int):
    for prod in productos:
        if prod["Código"] == cod:
            return prod

@app.get('/productos/')
def findProducto_str(nom:str):
    for prod in productos:
        if prod['Nombre'] == nom:
            return prod
        
@app.post('/productos')
def createProducto(cod:int, nom:str, val:float, exi:int):
    productos.append({
        "Código"    :cod,
        "Nombre"    :nom,
        "Valor"     :val,
        "Existencia"    :exi
    })
    return productos

@app.post('/productos_2')
def createProducto_2(cod:int = Body(), 
                   nom:str = Body(), 
                   val:float = Body(), 
                   exi:int = Body()):
    productos.append({
        "Código"    :cod,
        "Nombre"    :nom,
        "Valor"     :val,
        "Existencia"    :exi
    })
    return productos

@app.put('/producto/{cod}')
def updateProductos(cod:int, 
                    nom:str = Body(), 
                    val:float = Body(), 
                    exi:int = Body()):
    for prod in productos:
        if prod["Código"] == cod:
            prod["Nombre"] = nom,
            prod["Valor"] = val,
            prod["Existencia"] = exi

    return productos
    
@app.delete('/productos/{cod}')
def deleteProducto(cod:int):
    for prod in productos:
        if prod['Código'] == cod:
            productos.remove(prod)
    return productos
