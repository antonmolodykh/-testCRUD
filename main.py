from connexion import RestyResolver
import connexion
from injector import Binder
from flask_injector import FlaskInjector, inject
from services.database_helper import TableProvider



def configure(binder: Binder):
    binder.bind(TableProvider, TableProvider())
    return binder


if __name__ == '__main__':
    app = connexion.App(__name__, specification_dir='swagger/')
    app.add_api('schema.yaml', resolver=RestyResolver('api'))
    FlaskInjector(app=app.app, modules=[configure])
    app.run(5000)