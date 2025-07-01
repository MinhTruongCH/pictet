import dlt

@dlt.table(
    name="bronze_fix_messages",
    comment="Table loaded from a txt stream in S3"
)
def my_streaming_table():
    return (
        spark.readStream.format("cloudFiles")
            .option("cloudFiles.format", "csv")
            .option("header", "false")
            .option("cloudFiles.schemaLocation", "s3://awsbucketpictetmtr/schemaLocation/")
            .option("cloudFiles.inferColumnTypes", "true")
            .load("s3://awsbucketpictetmtr/")
    )