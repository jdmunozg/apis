from flask import Flask, request, jsonify
import random

app = Flask(__name__)
customer = []
bodega = []
buy = {}
contCompra = 0
total = 0

def generarCodigo():
    return random.randint(1,5000)

def buscadorCliente(codigo):
    global customer
    estado = False
    cont = 0
    while(cont < len(customer) and estado == False):
        if customer[cont][0] == codigo:
            estado = True
        cont+=1
    return estado

def retornoDatos(codigo):
    global customer
    estado = False
    cont = 0
    datos = ""
    while(cont < len(customer) and estado == False):
        if customer[cont][0] == codigo:
            estado = True
            datos = customer[cont]
        cont+=1
    return datos



@app.route("/clients/api", methods=["POST"])
def cliente():
    global customer
    respuest = ""
    estado = False
    codigo = 0
    jsons = request.get_json()
    nombre = jsons["nombre"]
    apellido = jsons["apellido"]
    while(estado == False):
        if(buscadorCliente(generarCodigo) == False):
            codigo = generarCodigo()
            estado = True
    customer.append([codigo,nombre,apellido])
    for x in customer:
        respuest += str(x[0])+","
    respuestas = {"Clients": f"{respuest}"}
    return jsonify(respuestas)

@app.route("/product/api", methods=["POST"])
def productos():
    global total
    global contCompra
    global bodega
    auxiliar = []
    respuesta = {}
    jsons = request.get_json()
    producto = jsons["producto"]
    codigo = jsons["codigo"]
    if (buscadorCliente(codigo)):
        for x in producto:
            auxiliar.append([x["codigo"],x["nombrePro"],x["precio"]])
            total += x["precio"]
        respuesta = {"": f"EL CODIGO{contCompra} SE REGISTRO"}
        buy[contCompra]=[auxiliar.copy(),total,retornoDatos(codigo)]
        bodega.append(auxiliar.copy())
        contCompra+=1
        total = 0
    else:
        respuesta = {"RESP": f"USUARIO {codigo} NO HAY, NO JODA"}
    return jsonify(respuesta)

@app.route("/buy/api", methods=["GET"])
def compra():
    global buy
    respuesta = {}
    buycod = request.args.get("buycod")
    if (buycod in buy):
            respuesta = {"Info": f"Compra con el cod {buycod} "+
                                        f"{buy[buycod][0]} Total: ${buy[buycod][1]}  "
                                        + f"Client: {buy[buycod][2]}"}
    else:
        respuesta = {"Res": f"Compra {buycod} no hay, joda"}
    return jsonify(respuesta)

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)