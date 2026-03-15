import pymysql

# 1. Install as MySQLdb
pymysql.install_as_MySQLdb()

# 2. Fake the version number to satisfy Django's requirements
pymysql.version_info = (2, 2, 7, "final", 0)