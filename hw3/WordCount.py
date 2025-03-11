from pyspark.sql import SparkSession
from pyspark.sql.functions import split, size, sum

# Initialize Spark Session
spark = SparkSession.builder.appName("WordCount").getOrCreate()

df = spark.read.text("hamlet.txt").cache()
df = df.withColumn("words", split(df["value"], " ")).drop("value")
df = df.withColumn("word_count_per_row", size(df["words"])).drop("words")

total_word_count = df.agg(sum("word_count_per_row").alias("total_word_count")).collect()[0]["total_word_count"]
spark.stop()

print(f"Total word count: {total_word_count}")
