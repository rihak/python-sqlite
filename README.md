python-sqlite
=============
Readability oriented sqlite3 wrapper for python.

Sample Usage
------------
```python
# Don't forget to import the module first!
import db

# Create an instance passing sqlite database filename
mydb = db.DB('test.db')


# Create table 'users' with columns 'id', 'username' and 'email' and columns definition
mydb.create_users(id='INTEGER NOT NULL UNIQUE', username='TEXT UNIQUE', email='TEXT')


# Insert row into 'users'
mydb.insert_users(id=123, username='Rihak', email='dev.rihak@gmail.com')


# Select 'username' and 'email' columns from 'users' table where id is '123'
# This returns a list of tuples
user = mydb.select_users({'id': 123}, 'username', 'email')
# now user is [('Rihak', 'dev.rihak@gmail.com')]


# Updates 'username' column of 'users' table where id is '123'
mydb.update_users({'id': 123}, username='Rihak5')


# Delete from table 'users' where id is '123'
mydb.delete_users({'id': 123})

# And if you like to, you can always run manual queries
# by passing plain sql and the parameters' tuple
mydb.run('SELECT * FROM users WHERE id = ?', (123,))
```

Transactions
------------
This module also supports transactions. You can start a transaction with
```python
mydb.begin_transaction()
```
and when you're done with those queries, you can either
```python
mydb.commit()
# OR
mydb.rollback()
```
Keep in mind that if you don't enable a transaction, every query will be instantaneously committed affecting your database.