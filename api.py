from eve import Eve
from eve_mongoengine import EveMongoengine

# init application
from public.models import *

MONGODB_SETTINGS = {

    # 'MONGO_HOST': 'localhost',
    #     'MONGO_PORT': 27017,
    #     'MONGO_USERNAME' : None,
    # 'MONGO_PASSWORD': None,
    'MONGO_DBNAME': 'ashrm3',
    'DOMAIN': {'student': {}}
}

app = Eve(settings=MONGODB_SETTINGS)
# init extension
ext = EveMongoengine(app)
# register model to eve
ext.add_model(Student)
ext.add_model(BusRoute)

# let's roll
app.run()
