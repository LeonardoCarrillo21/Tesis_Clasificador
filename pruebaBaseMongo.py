import pymongo

client = pymongo.MongoClient("localhost",27017)

db = client['basePrueba']

collection = db['alumnos']

# documentoEjemplo = {
#                     'name':'leonardo javier',
#                     'lastName':'Carrillo Mártinez',
#                     'age':23,
#                     'nationality':'Mexican',
#                     }

# insertResult = collection.insert_one(documentoEjemplo)

# print(insertResult)
# print(f'documento insertado: ',insertResult.inserted_id)

# encontrado = collection.find_one({'age':23})

# print(encontrado)

encontrados = collection.find()

for next in encontrados:
    print(next)