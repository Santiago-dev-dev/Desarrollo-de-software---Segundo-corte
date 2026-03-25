from fastapi import FastAPI, Body, HTTPException

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

# Validación 1 y 2: código mayor a cero y mensaje si no existe
@app.get('/productos/{cod}')
def findProducto(cod:int):
    if cod <= 0:
        raise HTTPException(status_code=400, detail="El código debe ser mayor a cero")
    for prod in productos:
        if prod["Código"] == cod:
            return prod
    raise HTTPException(status_code=404, detail=f"No existe un producto con código {cod}")

@app.get('/productos/')
def findProducto_str(nom:str):
    for prod in productos:
        if prod['Nombre'] == nom:
            return prod

# Validación 3 y 4: código consecutivo automático, valor y existencias mayores a cero
@app.post('/productos')
def createProducto(nom:str, val:float, exi:int):
    if val <= 0 or exi <= 0:
        raise HTTPException(status_code=400, detail="El valor y las existencias deben ser mayores a cero")
    cod = max(prod["Código"] for prod in productos) + 1
    productos.append({
        "Código"    :cod,
        "Nombre"    :nom,
        "Valor"     :val,
        "Existencia"    :exi
    })
    return productos

# Validación 3 y 4: código consecutivo automático, valor y existencias mayores a cero
@app.post('/productos_2')
def createProducto_2(nom:str = Body(), 
                   val:float = Body(), 
                   exi:int = Body()):
    if val <= 0 or exi <= 0:
        raise HTTPException(status_code=400, detail="El valor y las existencias deben ser mayores a cero")
    cod = max(prod["Código"] for prod in productos) + 1
    productos.append({
        "Código"    :cod,
        "Nombre"    :nom,
        "Valor"     :val,
        "Existencia"    :exi
    })
    return productos

# Validación 5, 6 y 7: mensaje si no existe, valor y existencias mayores a cero, mostrar antes y después
@app.put('/producto/{cod}')
def updateProductos(cod:int, 
                    nom:str = Body(), 
                    val:float = Body(), 
                    exi:int = Body()):
    if val <= 0 or exi <= 0:
        raise HTTPException(status_code=400, detail="El valor y las existencias deben ser mayores a cero")
    for prod in productos:
        if prod["Código"] == cod:
            antes = prod.copy()
            prod["Nombre"] = nom,
            prod["Valor"] = val,
            prod["Existencia"] = exi
            return {
                "Antes":  antes,
                "Después": prod
            }
    raise HTTPException(status_code=404, detail=f"No existe un producto con código {cod}")

# Validación 8: mensaje si no existe, mostrar producto eliminado
@app.delete('/productos/{cod}')
def deleteProducto(cod:int):
    for prod in productos:
        if prod['Código'] == cod:
            productos.remove(prod)
            return {
                "Mensaje": "Producto eliminado exitosamente",
                "Producto eliminado": prod
            }
    raise HTTPException(status_code=404, detail=f"No existe un producto con código {cod}")