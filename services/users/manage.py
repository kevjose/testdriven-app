from flask.cli import FlaskGroup
import unittest
from project import create_app, db
from project.api.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def test():
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@cli.command('seed_db')
def seed_db():
    """Seeds the database."""
    # new
    db.session.add(User(
        username='michael',
        email='michael@reallynotreal.com',
        password='greaterthaneight'
    ))
    # new
    db.session.add(User(
        username='michaelherman',
        email='michael@mherman.org',
        password='greaterthaneight'
    ))
    db.session.commit()

if __name__ == '__main__':
    cli()
