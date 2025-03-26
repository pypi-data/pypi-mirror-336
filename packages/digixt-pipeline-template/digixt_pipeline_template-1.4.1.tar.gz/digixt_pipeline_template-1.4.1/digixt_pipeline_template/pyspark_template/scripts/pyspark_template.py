from pyspark.sql.functions import *
from bs4 import BeautifulSoup
from pyspark.sql.types import StructType
from pyspark.sql.functions import lit

# Custom Dependencies
# TODO: this is added to help airflow detect common_utils as module
import sys
sys.path.append("/workflows/pyspark_template/")

from common_utils.scripts.common_utilities import CommonLogging, CommonIcebergUtilities
from common_utils.scripts.helper.common_helper_utilities import CommonProcessHelperUtils


logging = CommonLogging.get_logger()

# ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****

MOUNT_BUCKET = '/workflows'

class DefaultPySparkScript:
    def get_dummy_data():
        data = [
            {
                "full_name":"Ali Abdu",
                "date_of_birth":  "1980-02-09",
                "position": "Senior  Data Scientist",
                 "salary": 35000.00
            },
            {
                "full_name":"Hana Senay",
                "date_of_birth":  "1984-11-23",
                "position": "Software Engineer",
                 "salary": 27600.00
            },
            {
                "full_name":"Merhawi Kiflemaraim ",
               "date_of_birth":  "1985-01-16",
                "position": "Data Engineer",
                 "salary": 30000.00
            }
        ]
        return data
    
    def ingest_data(spark, output_warehouse_fq_table, output_wh_table_load_strategy, catalog_minio_bucket:str = None, location: str = None
                    ,auto_table_creation=False
                    ):
        from pyspark.sql.types import StructType, StructField, StringType, DoubleType, DateType

        data = DefaultPySparkScript.get_dummy_data()
        schema = StructType([
            StructField("full_name", StringType(), True),
            StructField("date_of_birth", StringType(), True),
            StructField("position", StringType(), True),
            StructField("salary", DoubleType(), True)
        ])
        
        data_df = spark.createDataFrame(data, schema=schema)\
                .withColumn("date_of_birth", to_date(col("date_of_birth"), "yyyy-MM-dd"))
        
        data_df = data_df.withColumn("ingested_at", to_timestamp(lit(current_timestamp())))

        script_adding_columns = ["ingested_at"]
        
        data_df.printSchema()
        data_df.cache()
        logging.info("Input parameters -> auto_table_creation: {auto_table_creation}, output_warehouse_fq_table -> {output_warehouse_fq_table}")
        if auto_table_creation and not CommonIcebergUtilities.table_exists(output_warehouse_fq_table=output_warehouse_fq_table, spark=spark):
            logging.warning(f""">>Table '{output_warehouse_fq_table}' is not available!!!""")
            CommonIcebergUtilities.create_table(output_warehouse_fq_table=output_warehouse_fq_table,
                                            spark=spark,
                                             data_df=data_df,
                                             catalog_minio_bucket=catalog_minio_bucket,
                                             location=location
                                             )
            
        data_df.show(10, truncate=False)

        CommonIcebergUtilities.iceberg_load_operation(spark=spark,
                                                        output_wh_table_load_strategy=output_wh_table_load_strategy,
                                                        data_df=data_df,
                                                        output_warehouse_fq_table=output_warehouse_fq_table,
                                                        script_adding_columns=script_adding_columns
                                                    )
       
        data_df.unpersist()
        logging.info(">>Data ingestion completed...")
        warehouse_catalog, warehouse_schema, warehouse_ref_table = output_warehouse_fq_table.split(".")

        CommonIcebergUtilities.optimize_commands(spark, warehouse_catalog, warehouse_schema, warehouse_ref_table)


def main():
    try:
       
        db_details = spark_job_args.get("db_details", {})
        operation_type = spark_job_args.get("operation_type", "default")

        
        # Arguments - DW output table
        output_warehouse_fq_table = spark_job_args["output_warehouse_fq_table"]
        output_wh_table_load_strategy = spark_job_args.get("output_wh_table_load_strategy", "APPEND")
        output_table_snapshots_delete_period = spark_job_args.get("output_table_snapshots_delete_period", 60)
        location = spark_job_args.get("output_table_location", None)
        catalog_minio_bucket = spark_job_args.get("catalog_minio_bucket", None) #This is from ENV var, no need to add in the config,
        auto_table_creation = bool(spark_job_args.get("auto_table_creation", False)) #whethere to create table if not exist
        
        

        logging.info("""output_warehouse_fq_table: %s, output_wh_table_load_strategy: %s, output_table_snapshots_delete_period: %s
                """.format(output_warehouse_fq_table, output_wh_table_load_strategy, output_table_snapshots_delete_period))

        DefaultPySparkScript.ingest_data(spark=spark
                                ,output_warehouse_fq_table=output_warehouse_fq_table
                                ,output_wh_table_load_strategy=output_wh_table_load_strategy
                                ,location=location
                                ,catalog_minio_bucket=catalog_minio_bucket
                                ,auto_table_creation=auto_table_creation
                                )
    except Exception as ex:
        logging.error(ex)
        sc.stop()
        raise Exception('! Something went wrong with this job')

    finally:
        logging.info('Stopping...')
        sc.stop()


if __name__ == '__main__':
    # Provide Spark Session additional config options as dictionary
    spark_options = {
        "spark.sql.shuffle.partitions": "10",
        "spark.default.parallelism": "10",
    }
    spark, sc, spark_app_name, spark_job_args, cluster_details_spark_args, minio_s3_credentials,\
    credentials  = CommonProcessHelperUtils.\
                                            initialize_read_arguments(spark_options=spark_options, mount_bucket_name=MOUNT_BUCKET)
    logging.info(f"spark_job_args: {spark_job_args}")

    main()
    exit()
