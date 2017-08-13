from flask_injector import inject
from services.database_helper import TableProvider


class Client(object):
    @inject
    def post(self, client, db: TableProvider):
        db.create(client['name'], client['phone'], client['timezone'])
        return {}, 201

    @inject
    def get(self, id, db: TableProvider):
        rec = db.read(id)
        if rec is None:
            return {}, 200
        return rec, 200

    @inject
    def put(self, client, db:TableProvider):
        id = client.pop("id")
        if db.read(id) is None:
            return {"error": "Record does not exist"}, 400
        db.update(id, {'name': client['name'], 'phone': client['phone'], 'timezone': client['timezone']})
        return {}, 200

    @inject
    def delete(self, id, db: TableProvider):
        if db.read(id) is None:
            return {"error": "Record does not exist"}, 400
        db.delete(id)
        return {}, 200


@inject
def by_filter(db: TableProvider, query, page=1, count=5):
    rec = db.search(query)
    if len(rec) < (page-1)*count+1:
        return rec[:count], 200
    return rec[(page-1)*count:page*count], 200

client = Client()
