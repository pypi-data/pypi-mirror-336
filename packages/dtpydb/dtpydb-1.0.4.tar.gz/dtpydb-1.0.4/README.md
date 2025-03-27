# Database Management Package

A Python package for managing database connections, sessions, and ORM operations using SQLAlchemy. This package supports both synchronous and asynchronous database interactions with PostgreSQL.

## Features
- **Database Configuration:** Set database credentials and connection parameters easily.
- **Synchronous and Asynchronous Support:** Provides both sync (`SQLAlchemy`) and async (`SQLAlchemy + asyncpg`) connections.
- **Connection Pooling & Monitoring:** Efficient resource management with connection pooling and active connection tracking.
- **ORM Base Model:** Provides a structured base model with `id`, `created_at`, and `updated_at` fields.
- **Query and Filtering Utilities:** Simplified filtering, searching, and condition-building for complex queries.
- **Upsert Operations:** Supports bulk insert, update, and upsert operations for optimized database interactions.

## Installation
```bash
pip install dtpydb
```

## Usage

### 1. Configure the Database
```python
from dtpydb.database import DatabaseConfig, DatabaseInstance

config = DatabaseConfig()
(
    config
    .set_db_user("user")
    .set_db_password("password")
    .set_db_host("localhost")
    .set_db_port(5432)
    .set_db_name("my_database")
    .set_db_ssl(False)
    .set_db_pool_size(10)
    .set_db_max_overflow(5)
)

db_instance = DatabaseInstance(config)
```

### 2. Creating Tables
```python
db_instance.create_tables()
```

### 3. Using Synchronous Sessions
```python
with db_instance.get_db_cm() as db:
    result = db.execute("SELECT * FROM users").fetchall()
    print(result)
```

### 4. Using Asynchronous Sessions
```python
async def fetch_data():
    async with db_instance.async_get_db_cm() as db:
        result = await db.execute("SELECT * FROM users")
        print(result.fetchall())
```

### 5. Defining ORM Models
```python
from sqlalchemy import Column, String
from dtpydb.model import ModelBase

class User(db_instance.base, ModelBase):
    __tablename__ = "users"
    name = Column(String, nullable=False)
```

### 6. Performing Upsert Operations

```python
from dtpydb.utilities import upsert_data

data = [{"id": 1, "name": "John Doe"}]
upsert_data(data, User, db_instance.session_local())
```

## Database Health Check
```python
if db_instance.check_database_health():
    print("Database is healthy!")
else:
    print("Database connection failed.")
```
