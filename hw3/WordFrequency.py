from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode, col, count, regexp_replace, lower, desc

# Initialize Spark Session
spark = SparkSession.builder.appName("WordFrequency").getOrCreate()

df = spark.read.text("hamlet.txt").cache()
df = df.withColumn("word", explode(split(col("value"), " "))).drop("value")
df = df.withColumn("word", regexp_replace(col("word"), "[^a-zA-Z0-9]", ""))
df = df.filter(col("word") != "").withColumn("word", lower(col("word")))

wc_df = df.groupBy("word").agg(count("word")).orderBy(desc("count(word)")).limit(20)
wc_df.show()

spark.stop()

