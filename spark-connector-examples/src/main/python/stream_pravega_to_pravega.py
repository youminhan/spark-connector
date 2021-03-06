from pyspark.sql import SparkSession
import os

controller = os.getenv("PRAVEGA_CONTROLLER", "tcp://127.0.0.1:9090")
scope = os.getenv("PRAVEGA_SCOPE", "examples")

spark = (SparkSession
         .builder
         .getOrCreate()
         )

(spark
    .readStream 
    .format("pravega") 
    .option("controller", controller) 
    .option("scope", scope) 
    .option("stream", "streamprocessing1")
    # If there is no checkpoint, start at the earliest event.
    .option("start_stream_cut", "earliest")
    .load()
    .selectExpr("event", "cast(event as string) as routing_key") 
    .writeStream 
    .trigger(processingTime="3 seconds") 
    .outputMode("append") 
    .format("pravega") 
    .option("controller", controller) 
    .option("scope", scope) 
    .option("stream", "streamprocessing2") 
    .option("checkpointLocation", "/tmp/spark-checkpoints-stream_pravega_to_pravega") 
    .start() 
    .awaitTermination()
 )
