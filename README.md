python-sqlite
=============
Readability oriented sqlite3 wrapper for python.

Sample Usage
------------
```python
# Create an instance passing sqlite database filename
db = SQLiteDataBase('test.db')


# Create table 'users' with columns 'id', 'username' and 'email' and columns definition
db.create_users(id='INTEGER NOT NULL UNIQUE', username='TEXT UNIQUE', email='TEXT')


# Insert row into 'users'
db.insert_users(id='123', username='Rihak', email='dev.rihak@gmail.com')


# Select 'username' and 'email' columns from 'users' table where id is '123'
# This returns a list of tuples
user = db.select_users({'id': 123}, 'username', 'email')
# user is [('Rihak', 'dev.rihak@gmail.com')]


# Updates 'username' column of 'users' table where id is '123'
db.update_users({'id': 123}, username='Rihak5')


# Delete from table 'users' where id is '123'
db.delete_users({'id': 123})
```
