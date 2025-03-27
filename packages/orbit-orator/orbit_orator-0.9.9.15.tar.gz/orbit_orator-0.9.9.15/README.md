# Orbit-Orator

A simple ORM for Python, forked from Orator.

## Installation

```bash
pip install orbit-orator
```

## Basic Usage

```python
from orbit_orator import DatabaseManager, Model

config = {
    'mysql': {
        'driver': 'mysql',
        'host': 'localhost',
        'database': 'database',
        'user': 'root',
        'password': '',
        'prefix': ''
    }
}

db = DatabaseManager(config)
Model.set_connection_resolver(db)

class User(Model):
    pass

users = User.where('votes', '>', 100).take(10).get()

for user in users:
    print(user.name)
```

## License

MIT License 