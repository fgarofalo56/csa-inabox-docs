# 🗄️ HBase on HDInsight

> __🏠 [Home](../../../README.md)__ | __📖 [Documentation](../../README.md)__ | __🎓 [Tutorials](../README.md)__ | __🚀 Advanced__ | __🗄️ HBase__

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Level](https://img.shields.io/badge/Level-Advanced-red)
![Duration](https://img.shields.io/badge/Duration-90--120_minutes-blue)

__Master HBase on HDInsight. Learn NoSQL design, real-time reads/writes, and integration patterns.__

## 🎯 Learning Objectives

- Understand HBase architecture
- Design schemas for NoSQL
- Perform CRUD operations
- Optimize for performance
- Integrate with Phoenix

## 📋 Prerequisites

- [ ] __HDInsight cluster__ with HBase
- [ ] __NoSQL concepts__ - Row keys, column families
- [ ] __Java or Python__

## 🏗️ HBase Architecture

- __Region Servers__ - Store data
- __Master Server__ - Coordinates regions
- __ZooKeeper__ - Distributed coordination
- __HDFS__ - Underlying storage

## 📊 Schema Design

```bash
# Create table
create 'users', 'profile', 'activity'

# Put data
put 'users', 'user001', 'profile:name', 'John Doe'
put 'users', 'user001', 'profile:email', 'john@example.com'

# Get data
get 'users', 'user001'

# Scan
scan 'users'
```

## 🔍 Phoenix SQL Layer

```sql
-- Create Phoenix table
CREATE TABLE users (
    user_id VARCHAR PRIMARY KEY,
    name VARCHAR,
    email VARCHAR
);

-- Query with SQL
SELECT * FROM users WHERE name = 'John Doe';
```

## 📚 Resources

- [HBase Documentation](https://hbase.apache.org/)
- [Phoenix on HDInsight](https://learn.microsoft.com/azure/hdinsight/hbase/apache-hbase-phoenix-squirrel-linux)

---

*Last Updated: January 2025*
