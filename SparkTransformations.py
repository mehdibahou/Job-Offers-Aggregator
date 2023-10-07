from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace, split, current_timestamp, expr, col
from pyspark.sql.types import IntegerType
from pyspark.sql import DataFrame

# Initialize a Spark session
spark = SparkSession.builder.appName("MongoDBTransformation").getOrCreate()

# Load data from MongoDB
mongo_uri = "mongodb://your_mongodb_uri"
df = spark.read.format("mongo").option("uri", mongo_uri).load()

# Transformation 1: Remove unnecessary text from 'PublishDuration'
df = df.withColumn("PublishDuration", regexp_replace(
    df["PublishDuration"], r'\sago·More\.\.\.$', ''))

# Transformation 2: Extract 'Post_Period'
df = df.withColumn("Post_Period", split(df["PublishDuration"], " ")[0])

# Transformation 3: Remove 'Reposted' from 'PublishDuration'
df = df.withColumn("PublishDuration", regexp_replace(
    df["PublishDuration"], "Reposted", ""))

# Transformation 4: Remove leading/trailing spaces
df = df.withColumn("PublishDuration", expr("trim(PublishDuration)"))

# Transformation 5: Remove ' ago' and additional spaces
df = df.withColumn("PublishDuration", regexp_replace(
    df["PublishDuration"], " ago", ""))

# Transformation 6: Replace 'weeks' with 'w', 'week' with 'w', and 'days' with 'd'
df = df.withColumn("PublishDuration", regexp_replace(
    df["PublishDuration"], "weeks?", "w"))
df = df.withColumn("PublishDuration", regexp_replace(
    df["PublishDuration"], "days?", "d"))

# Transformation 7: Convert to timedelta
df = df.withColumn("PublishDuration", expr("interval(PublishDuration)"))

# Calculate the date 'X time ago' from the current date
current_date = current_timestamp()
df = df.withColumn("DateXTimeAgo", current_date - df["PublishDuration"])

# Calculate the difference in days and store it in a new column
df = df.withColumn("DaysDifference", (current_date -
                   df["DateXTimeAgo"]).cast(IntegerType()))

# Drop the 'Post_Period' column
df = df.drop("Post_Period")

# Transformation 8: Clean 'Region'
df = df.withColumn("Region", regexp_replace(df["Region"], r'\(.*\)', ""))
df = df.withColumn("Region", expr("trim(Region)"))

# Transformation 9: Add 'Platform_Posted' column
df = df.withColumn("Platform_Posted", expr("'LinkedIn'"))

# Specify the Cassandra keyspace and table
cassandra_keyspace = "your_keyspace"
cassandra_table = "your_table"

# Write the DataFrame to Cassandra
df.write \
    .format("org.apache.spark.sql.cassandra") \
    .option("spark.cassandra.connection.host", "your_cassandra_host") \
    .option("spark.cassandra.auth.username", "your_username") \
    .option("spark.cassandra.auth.password", "your_password") \
    .options(table=cassandra_table, keyspace=cassandra_keyspace) \
    .mode("append") \
    .save()

# Stop the Spark session
spark.stop()
