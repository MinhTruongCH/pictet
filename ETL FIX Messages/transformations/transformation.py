import dlt

@dlt.table(
    name="bronze_fix_messages",
    comment="Table loaded from a txt stream in S3"
)
def bronze_fix_messages():
    return (
        spark.readStream.format("cloudFiles")
            .option("cloudFiles.format", "csv")
            .option("header", "false")
            .option("cloudFiles.schemaLocation", "s3://awsbucketpictetmtr/schemaLocation/")
            .option("cloudFiles.inferColumnTypes", "true")
            .load("s3://awsbucketpictetmtr/")
    )

from pyspark.sql.functions import split, regexp_extract, col, to_timestamp, coalesce

@dlt.table(
    name="silver_fix_messages",
    comment="Bronze table cleaned and parsed"
)
def silver_fix_messages():
    return (
        spark.read.table("bronze_fix_messages")
        .filter("_c0 LIKE '%8=FIX.4.2%'")
        .select(
            regexp_extract("_c0", r'8=([^|]+)', 1).alias("BeginString"),
            regexp_extract("_c0", r'9=([^|]+)', 1).cast("int").alias("BodyLength"),
            regexp_extract("_c0", r'35=([^|]+)', 1).alias("MsgType"),
            regexp_extract("_c0", r'34=([^|]+)', 1).cast("int").alias("MsgSeqNum"),
            regexp_extract("_c0", r'49=([^|]+)', 1).alias("SenderCompID"),
            coalesce(
                to_timestamp(regexp_extract("_c0", r'52=([^|]+)', 1), "yyyyMMdd-HH:mm:ss.SSS"),
                to_timestamp(regexp_extract("_c0", r'52=([^|]+)', 1), "yyyy-MM-dd-HH:mm:ss.SSS")
            ).alias("SendingTime"),
            regexp_extract("_c0", r'56=([^|]+)', 1).alias("TargetCompID"),
            regexp_extract("_c0", r'11=([^|]+)', 1).alias("ClOrdID"),
            regexp_extract("_c0", r'1=([^|]+)', 1).alias("Account"),
            regexp_extract("_c0", r'55=([^|]+)', 1).alias("Symbol"),
            regexp_extract("_c0", r'54=([^|]+)', 1).cast("int").alias("Side"),
            regexp_extract("_c0", r'15=([^|]+)', 1).alias("Currency"),
            coalesce(
                to_timestamp(regexp_extract("_c0", r'60=([^|]+)', 1), "yyyyMMdd-HH:mm:ss.SSS"),
                to_timestamp(regexp_extract("_c0", r'60=([^|]+)', 1), "yyyy-MM-dd-HH:mm:ss.SSS")
            ).alias("TransactTime"),
            regexp_extract("_c0", r'59=([^|]+)', 1).cast("int").alias("TimeInForce"),
            regexp_extract("_c0", r'10=([^|]+)', 1).cast("int").alias("CheckSum")
        )
        .dropDuplicates()
    )

@dlt.table(
    name="gold_fix_messages",
    comment="Gold table business aggregates"
)
def gold_fix_messages():
    return (
        spark.read.table("silver_fix_messages")
    )