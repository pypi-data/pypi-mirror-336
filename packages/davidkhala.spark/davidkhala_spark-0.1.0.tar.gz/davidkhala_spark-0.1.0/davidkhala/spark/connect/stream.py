from pyspark.sql.connect.dataframe import DataFrame
from pyspark.sql.connect.streaming import StreamingQuery

from davidkhala.spark.sink.stream import ForeachBatchWriter


def startAny(df: DataFrame, writer: ForeachBatchWriter) -> StreamingQuery:
    assert df.isStreaming

    return df.writeStream.foreachBatch(writer.on_batch).start()
