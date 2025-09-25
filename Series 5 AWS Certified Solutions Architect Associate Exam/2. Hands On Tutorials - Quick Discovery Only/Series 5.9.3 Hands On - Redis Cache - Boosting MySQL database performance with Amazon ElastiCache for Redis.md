# Databases

> [!IMPORTANT]
> PLEASE REMEMBER TO DELETE THE AWS RESOURCES AFTER TUTORIAL IS DONE !!!

> [!NOTE]
> Amazon says: In this tutorial, you will learn how to boost the performance of your applications by adding an in-memory caching layer to your relational database. You will implement a cache-aside strategy using Amazon ElastiCache for Redis on top of a MySQL database.

The cache-aside strategy is one of the most popular options for boosting database performance. When an application needs to read data from a database, it first queries the cache. If the data is not found, the application queries the database and populates the cache with the result. There are many ways to invalidate the cache if the relevant records are modified in the underlying database, but for this tutorial we will use the Time To Live (TTL) expiration feature provided by Redis.

> [!IMPORTANT]
> Watch Intros
> https://www.youtube.com/watch?v=Tqaqdfxi-J4
> https://www.youtube.com/watch?v=OqCK95AS-YE

# Tutorial Link
https://aws.amazon.com/getting-started/hands-on/boosting-mysql-database-performance-with-amazon-elasticache-for-redis/?ref=gsrchandson

# Helpful

