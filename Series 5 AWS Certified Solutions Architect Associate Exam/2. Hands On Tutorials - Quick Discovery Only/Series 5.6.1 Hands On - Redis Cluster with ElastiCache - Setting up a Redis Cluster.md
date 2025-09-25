# Cloud Foundations Category

> [!IMPORTANT]
> PLEASE REMEMBER TO DELETE THE AWS RESOURCES AFTER TUTORIAL IS DONE !!!

> [!NOTE]
> Amazon ElastiCache is a web service that makes it easy to set up, manage, and scale a distributed in-memory data store or cache environment in the cloud. It provides a high-performance, scalable, and cost-effective caching solution. At the same time, it helps remove the complexity associated with deploying and managing a distributed cache environment.

> Announcing Amazon ElastiCache Serverless.
> Simplified highly available distributed caching with instant scaling and no servers to manage.

> [!IMPORTANT]
> Watch Intros
> https://www.youtube.com/watch?v=G1rOthIU-uo
> https://www.youtube.com/watch?v=jgpVdJB2sKQ

# Tutorial Link
https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/set-up.html

# Read More
https://kekayan.medium.com/redis-on-aws-36ed7054357e

# Helpful
Everything was done under the root account user (I did not create a new user to start)
<br>Some Best Practices for setup here:
<br>https://aws.amazon.com/getting-started/hands-on/setting-up-a-redis-cluster-with-amazon-elasticache/?ref=gsrchandson

> [!TIP]
> Setup ruleS port 22 (SSH), 6379 (REDIS), 6380 (REDIS) rule on security group for instance to connect to box from AWS console:
> https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-connect-prerequisites.html
in EC2 > Security Groups
> https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/GettingStarted.serverless.step2.html

> e.g. Testing REDIS in EC3 Test Instance box
[ec2-user@ip-<MY EC2 INSTANCE IP> redis-stable]$ history 20
    1  sudo yum install gcc
    2  curl -O http://download.redis.io/redis-stable.tar.gz
    3  tar xvzf redis-stable.tar.gz
    4  cd redis-stable
    5  make
    6  clear

> cd redis-stable
> Run the following command:
> ./src/redis-cli -h myawsredisbox.foovql.clustercfg.euw1.cache.amazonaws.com -p 6379
> myawsredisbox.foovql.clustercfg.euw1.cache.amazonaws.com:6379> PING
> PONG

> To set data in REDIS:
> set a "hello"
> get a

> [!CAUTION]
> This did not work for me :( and give me connection refused
> ./src/redis-cli -c -h myawsredisbox.foovql.clustercfg.euw1.cache.amazonaws.com:6379