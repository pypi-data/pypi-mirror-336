# Orbit-Orator

Orbit-Orator 是一个简单而优雅的 Python ORM，基于 Orator ORM 进行二次开发。

## 安装

```bash
pip install orbit-orator
```

## 快速开始

```python
from orbit_orator import DatabaseManager, Model

# 配置数据库连接
config = {
    'mysql': {
        'driver': 'mysql',
        'host': 'localhost',
        'database': 'database',
        'user': 'user',
        'password': 'password',
        'prefix': ''
    }
}

# 初始化数据库连接
db = DatabaseManager(config)
Model.set_connection_resolver(db)

# 定义模型
class User(Model):
    __fillable__ = ['name', 'email']

# 创建记录
user = User.create(name='John', email='john@example.com')

# 查询记录
user = User.where('name', 'John').first()
```

## 特性

- 简单而优雅的 API
- 支持多种数据库（MySQL, PostgreSQL, SQLite）
- 支持模型关系
- 支持查询构建器
- 支持数据库迁移
- 支持事务处理

## 文档

详细文档请访问 [文档网站](https://github.com/yourusername/orbit-orator/wiki)

## 许可证

MIT License 