# a3mongo

English | [简体中文](README_ZH.md)

`a3mongo` is a simple wrapper around `pymongo` to make it easier to use.

## 1. Introduction

* Multiple MongoDB services can be configured at the same time.
* Some commonly used methods have been encapsulated.

## 2. Usage

### Install

```shell
pip install a3mongo

```

### Examples

```python
CONF = {
    'site_a': {
        "host": "127.0.0.1",
        "port": 27017,
        "username": "username",
        "password": "password",
        "authSource": "site_a",
        "authMechanism": "SCRAM-SHA-256"
    },
    'site_b': {
        "host": "127.0.0.1",
        "port": 27018,
        "username": "username",
        "password": "password",
        "authSource": "site_b",
        "authMechanism": "SCRAM-SHA-256"
    }
}


from a3mongo import MongoClientFactory, MongoTable


class SiteUser(MongoTable):
    table_name = 'site_user'
    db_conf_name = 'site_a'

    
if __name__ == '__main__':
    MongoClientFactory.init_mongo_clients(conf=CONF)
    site_user = SiteUser()
    site_user.create_table()
    site_user.create_index_list(['name', 'gender', 'email'])
    site_user.upsert_many([
        {'name': 'Alice', 'gender': 'female', 'email': 'alice@example.com'},
        {'name': 'Bob', 'gender':'male', 'email': 'bob@example.com'},
        {'name': 'Charlie', 'gender': 'male', 'email': 'charlie@example.com'},
    ])
    male_users = site_user.find({'gender':'male'})

```
