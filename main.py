from fastapi import FastAPI, Body, HTTPException
import csv

app = FastAPI()

ARCHIVO = "productos.csv"


def leer_productos():
    productos = []
    try:
        with open(ARCHIVO, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                productos.append({
                    "Código": int(row["Código"]),
                    "Nombre": row["Nombre"],
                    "Valor": float(row["Valor"]),
                    "Existencias": int(row["Existencias"])
                })
    except FileNotFoundError:
        return []
    return productos


def guardar_productos(productos):
    with open(ARCHIVO, mode='w', newline='', encoding='utf-8') as f:
        campos = ["Código", "Nombre", "Valor", "Existencias"]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(productos)


@app.get('/')
def mensaje():
    return "Bienvenido a FastAPI Ingenieros de Sistemas"


@app.get('/uno/')
def mensaje_3(edad:int, nombre_2:str):
    return f"Hola {nombre_2} Su edad es: {edad}"


# LISTAR PRODUCTOS
@app.get('/productos')
def listProductos():
    return leer_productos()


# BUSCAR POR CÓDIGO
@app.get('/productos/{cod}')
def findProducto(cod:int):
    productos = leer_productos()

    if cod <= 0:
        raise HTTPException(status_code=400, detail="El código debe ser mayor a cero")

    for prod in productos:
        if prod["Código"] == cod:
            return prod

    raise HTTPException(status_code=404, detail=f"No existe un producto con código {cod}")


# BUSCAR POR NOMBRE
@app.get('/productos/')
def findProducto_str(nom:str):
    productos = leer_productos()

    for prod in productos:
        if prod["Nombre"].lower() == nom.lower():
            return prod

    raise HTTPException(status_code=404, detail=f"No existe un producto con nombre {nom}")


# CREAR PRODUCTO (query params)
@app.post('/productos')
def createProducto(nom:str, val:float, exi:int):
    productos = leer_productos()

    if val <= 0 or exi <= 0:
        raise HTTPException(status_code=400, detail="El valor y las existencias deben ser mayores a cero")

    cod = max([prod["Código"] for prod in productos], default=0) + 1

    nuevo = {
        "Código": cod,
        "Nombre": nom,
        "Valor": val,
        "Existencias": exi
    }

    productos.append(nuevo)
    guardar_productos(productos)

    return nuevo


# CREAR PRODUCTO (Body)
@app.post('/productos_2')
def createProducto_2(
    nom:str = Body(), 
    val:float = Body(), 
    exi:int = Body()
):
    productos = leer_productos()

    if val <= 0 or exi <= 0:
        raise HTTPException(status_code=400, detail="El valor y las existencias deben ser mayores a cero")

    cod = max([prod["Código"] for prod in productos], default=0) + 1

    nuevo = {
        "Código": cod,
        "Nombre": nom,
        "Valor": val,
        "Existencias": exi
    }

    productos.append(nuevo)
    guardar_productos(productos)

    return nuevo


# ACTUALIZAR PRODUCTO
@app.put('/producto/{cod}')
def updateProductos(
    cod:int,
    nom:str = Body(),
    val:float = Body(),
    exi:int = Body()
):
    productos = leer_productos()

    if val <= 0 or exi <= 0:
        raise HTTPException(status_code=400, detail="El valor y las existencias deben ser mayores a cero")

    for prod in productos:
        if prod["Código"] == cod:
            antes = prod.copy()

            prod["Nombre"] = nom
            prod["Valor"] = val
            prod["Existencias"] = exi

            guardar_productos(productos)

            return {
                "Antes": antes,
                "Después": prod
            }

    raise HTTPException(status_code=404, detail=f"No existe un producto con código {cod}")


# ELIMINAR PRODUCTO
@app.delete('/productos/{cod}')
def deleteProducto(cod:int):
    productos = leer_productos()

    for prod in productos:
        if prod["Código"] == cod:
            productos.remove(prod)
            guardar_productos(productos)

            return {
                "Mensaje": "Producto eliminado exitosamente",
                "Producto eliminado": prod
            }

    raise HTTPException(status_code=404, detail=f"No existe un producto con código {cod}")