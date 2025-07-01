import dlt

@dlt.table(
    name="silver_fix_messages",
    comment="Bronze table cleaned"
)
def my_streaming_table():
    return (
        spark.readStream.table("bronze_fix_messages")
    )