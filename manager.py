from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from database import db

def runmigrate(app):
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    manager.run()