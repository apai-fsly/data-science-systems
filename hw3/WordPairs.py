from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split, lower, regexp_replace, count, array_sort, array

spark = SparkSession.builder.appName("WordPairs").getOrCreate()
df = spark.read.text("hamlet.txt")

# remove punctuation, convert to lowercase, and split into words
df = df.withColumn("words", split(lower(regexp_replace(col("value"), "[^a-zA-Z0-9\s]", "")), "\\s+"))

df = df.withColumn("word1", explode(col("words")))
df = df.withColumn("word2", explode(col("words")))

df = df.withColumn("pair", array_sort(array(col("word1"), col("word2"))))
word_pairs_df = df.groupBy("pair").agg(count("*").alias("count"))

word_pairs_df = word_pairs_df.orderBy(col("count").desc()).limit(20)

word_pairs_df.show()

spark.stop()
