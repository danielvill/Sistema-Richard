from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost:27017'

def dbConnection():
    try:
        client = MongoClient(MONGO_URI)
        db = client["modatatis"]
        print("Conexión a MongoDB exitosa.")
    except ConnectionError:
        print('Error de conexión con la bdd')
    return db