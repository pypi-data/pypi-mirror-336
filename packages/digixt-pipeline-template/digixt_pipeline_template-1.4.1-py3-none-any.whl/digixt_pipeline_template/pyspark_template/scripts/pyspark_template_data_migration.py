# from pyspark.sql.functions import 
from pyspark.sql.functions import to_date, col, to_timestamp, lit, current_timestamp
from pyspark.sql import SparkSession, DataFrame
from typing import Union, List, Tuple
from datetime import datetime, timedelta
# Custom Dependencies
# TODO: this is added to help airflow detect common_utils as module
import sys
sys.path.append("/workflows/pyspark_template/")
print("Sys Path:", sys.path)


from common_utils.scripts.common_utilities import CommonLogging, CommonIcebergUtilities
from common_utils.scripts.helper.common_helper_utilities import CommonBasicUtilities, CommonProcessHelperUtils
from common_utils.scripts.data.common_data_utilities import CommonDataUtilities
from common_utils.scripts.batch_calculator_utils import BatchCalculatorUtils

from common_utils.scripts.db_operations.db_operations_factory import DBOperationsFactory
from common_utils.scripts.db_operations.db_operations import BaseDBOperations


logging = CommonLogging.get_logger()

# ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** ***** *****

MOUNT_BUCKET = '/workflows'

class Constants:
    DEFAULT_RECORDS_PER_BATCH = 1_00_000
    DEFAULT_NUMBER_OF_PARTITIONS = 1
    DEFAULT_LOWER_BOUND = 0
    DEFAULT_UPPER_BOUND = DEFAULT_RECORDS_PER_BATCH
    DEFAULT_IS_COL_FOR_PARTITION_NULL_SUPP=False

class CustomUtils:
    @staticmethod
    def create_db_properties(db_details= None):
        db_properties = {}

        if db_details:
            db_properties['url'] = db_details.get("url", None)
            db_properties['dbtype'] = db_details.get("dbtype", None)
            db_properties['user'] = db_details.get("user", None)
            db_properties['password'] = db_details.get("password", None)

        return db_properties

    # @staticmethod
    # def calculate_batches(
    #     lower_bound: Union[str, int, float], 
    #     upper_bound: Union[str, int, float], 
    #     num_partitions: int, 
    #     records_per_batch: int,
    #     batch_by: str = "month"
    # ) -> List[Tuple[Union[int, float, str], Union[int, float, str]]]:
    #     """
    #     Generates batches within lower and upper bounds for both numerical and date-based partitions.
    #     Supports partitioning by months or fixed-day intervals.
        
    #     :param lower_bound: Start date (str in 'YYYY-MM-DD') or numeric lower bound.
    #     :param upper_bound: End date (str in 'YYYY-MM-DD') or numeric upper bound.
    #     :param num_partitions: Number of partitions for parallel execution.
    #     :param records_per_batch: Number of records to include in each batch.
    #     :param batch_by: Strategy for splitting ('month').
    #     :return: List of (start, end) tuples representing each batch.
    #     """

    #     # Detect if partitioning is based on dates
    #     is_datetime_partitioning = isinstance(lower_bound, str) and isinstance(upper_bound, str)
    #     print(f"""Start of batches calculation -> is_datetime_partitioning: {is_datetime_partitioning}, 
    #           lower_bound: {lower_bound}, upper_bound: {upper_bound}, batch_by: {batch_by}""")
        
    #     if is_datetime_partitioning:
    #         try:
    #             lower_bound = datetime.strptime(lower_bound, "%Y-%m-%d")
    #             upper_bound = datetime.strptime(upper_bound, "%Y-%m-%d")
    #         except ValueError:
    #             raise ValueError("Date format must be 'YYYY-MM-DD'.")
        
    #     if lower_bound > upper_bound:
    #         raise ValueError(f"lower_bound must be less than upper_bound -> lower_bound:{lower_bound}, upper_bound:{upper_bound}.")
        
    #     if not is_datetime_partitioning and (lower_bound < 0 or upper_bound < 0):
    #         raise ValueError(f"lower_bound or upper_bound cannot be negative -> lower_bound:{lower_bound}, upper_bound:{upper_bound}.")
        
    #     if records_per_batch <= 0:
    #         raise ValueError(f"records_per_batch must be positive -> records_per_batch:{records_per_batch}.")
        
    #     batches = []

    #     if is_datetime_partitioning:
    #         batches = CustomUtils.generate_batches(lower_bound, upper_bound, batch_by)
    #     else:
    #         # Handle integer/float increments
    #         start = lower_bound
    #         while start <= upper_bound:
    #             end = min(start + records_per_batch - 1, upper_bound)
    #             if (end + 1) == upper_bound:
    #                 end += 1  # Include the upper_bound
    #             batches.append((start, end))
    #             start = end + 1  # Move to the next batch start point
        
    #     return batches

    # @staticmethod
    # def generate_batches(lower_bound: datetime, upper_bound: datetime, batch_by="month"):
    #     """
    #     Splits the given date range into batches based on the specified batch_by parameter.

    #     :param lower_bound: Start date as a datetime object.
    #     :param upper_bound: End date as a datetime object.
    #     :param batch_by: Strategy for splitting ('month').
    #     :return: List of (start_date, end_date) tuples representing each batch.
    #     """
    #     batches = []
    #     current_date = lower_bound

    #     while current_date <= upper_bound:
    #         if batch_by == "month":
    #             # Move to the last day of the current month
    #             next_date = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    #         # TODO: per date will add in future
    #         # elif batch_by.endswith("d"):  # Example: '7d', '30d'
    #         #     days_to_add = int(batch_by[:-1])
    #         #     next_date = current_date + timedelta(days=days_to_add - 1)
    #         else:
    #             raise ValueError("Invalid batch_by parameter. Use 'month'")

    #         # Ensure we don't exceed the upper bound
    #         if next_date > upper_bound:
    #             next_date = upper_bound

    #         batches.append((current_date.strftime("%Y-%m-%d"), next_date.strftime("%Y-%m-%d")))
    #         current_date = next_date + timedelta(days=1)

    #     return batches

    
class DataMigrationFromDB:

    @staticmethod
    def load_and_optimize(spark:SparkSession, data_df: DataFrame, output_warehouse_fq_table:str, 
                output_wh_table_load_strategy:str, merge_data_join_fields: str=None,
                ):
        
        data_df.cache()

         # Spark V 3.1 does not support data_df.isEmpty(), it's new on 3.3
        # count = data_df.count() # It's expensive, don't use it unless it's there is no other option.
        tmp_df = data_df.take(1)
        logging.info("Read info -> take_one_record from Dataframe len {}".format(len(tmp_df)))
        if len(tmp_df) >= 1:
            script_adding_columns = []
            # Adding this to remove duplicates - we may get duplicates
            if "ingested_at" not in data_df.columns:
                data_df = data_df.withColumn("ingested_at", to_timestamp(lit(current_timestamp())))

                script_adding_columns.append("ingested_at")

            logging.info(">> Dataframe schema: " + str(data_df.schema))
            data_df.show(10)
            CommonIcebergUtilities.iceberg_load_operation(spark, output_wh_table_load_strategy, data_df,output_warehouse_fq_table,
                                                                        script_adding_columns,merge_data_join_fields=None)
        logging.info(f""">>Ingestion to table '{output_warehouse_fq_table}' completed,""")

        data_df.unpersist()
        
        warehouse_catalog, warehouse_schema, warehouse_ref_table = output_warehouse_fq_table.split(".")

        CommonIcebergUtilities.optimize_commands(spark, warehouse_catalog, warehouse_schema, warehouse_ref_table)


    @staticmethod
    def read_and_load_data(dbOps: BaseDBOperations, spark, table_name, column_for_partitioning, selected_columns, 
                            lower_bound, upper_bound,  num_partitions, output_warehouse_fq_table, output_wh_table_load_strategy,
                            is_col_for_partition_null_supp=False, records_per_batch=1_00_000, catalog_minio_bucket:str =None, 
                            location:str = None, auto_table_creation= False
                            ):
        logging.info(f""">>Table info -> auto_table_creation: {auto_table_creation}, table_name: {table_name},  output_warehouse_fq_table: {output_warehouse_fq_table}
                     column_for_partitioning: {column_for_partitioning}, num_partitions: {num_partitions},""")
        
        if auto_table_creation and not CommonIcebergUtilities.table_exists(output_warehouse_fq_table=output_warehouse_fq_table, spark=spark):
            logging.warning(f""">>Table '{output_warehouse_fq_table}' is not available!!!""")
            if CommonBasicUtilities.isEmpty(selected_columns) :
                selected_columns = "*"
            # query  = f"select {selected_columns} from {table_name} limit 1"
            data_df: DataFrame = dbOps.read_data(table_name=table_name,limit=1)
            
            CommonIcebergUtilities.create_table(output_warehouse_fq_table=output_warehouse_fq_table,
                                            spark=spark,
                                             data_df=data_df,
                                             catalog_minio_bucket=catalog_minio_bucket,
                                             location=location
                                             )
        if not column_for_partitioning:
            logging.info(f""">>Reading a table: {table_name} where  column_for_partitioning is None/Empty or not provided.
                        If `column_for_partitioning` is not provided or None/Empty, 
                        no batching or partitioning will happen -entire table will load into one executor at one time!!""")
        
            data_df: DataFrame = dbOps.read_data(table_name=table_name, column_names=selected_columns)

            DataMigrationFromDB.load_and_optimize(spark=spark, data_df=data_df,output_warehouse_fq_table=output_warehouse_fq_table, 
                                                   output_wh_table_load_strategy=output_wh_table_load_strategy)
        else:
            # column_for_partitioning is provided
            iteration_num = 1

            batches = BatchCalculatorUtils.calculate_batches(lower_bound=lower_bound, upper_bound=upper_bound,num_partitions=num_partitions,records_per_batch=records_per_batch)
            logging.info(""">>Batches -> {}""".format(batches))
            for batch in batches:
                start, end = batch

                logging.info(f""">>Iteration : {iteration_num}, lower_bound: {start}, upper_bound: {end}""" )
                
                data_df: DataFrame = dbOps.read_data(table_name=table_name,column_names=selected_columns,column_for_partitioning=column_for_partitioning,
                                        lower_bound=start,upper_bound=end,num_partitions=num_partitions)
                
                DataMigrationFromDB.load_and_optimize(spark=spark, data_df=data_df,output_warehouse_fq_table=output_warehouse_fq_table, 
                                                    output_wh_table_load_strategy=output_wh_table_load_strategy)
                iteration_num +=1

            # check if there is/are any null values for partitioning column and ingest it if is_col_for_partition_null_supp is True
            if is_col_for_partition_null_supp and column_for_partitioning is not None:
                logging.info(f""">>Read Null values for table_name: {table_name},  column_for_partitioning: {column_for_partitioning}, 
                            num_partitions: {num_partitions}, is_col_for_partition_null_supp: {is_col_for_partition_null_supp}""")
                
                if CommonBasicUtilities.isEmpty(selected_columns) :
                    selected_columns = "*"
                # query  = f"select {selected_columns} from {table_name} where {column_for_partitioning} is null"
                where_clause = "{column_for_partitioning} is null"
                data_df: DataFrame = dbOps.read_data(table_name=table_name,column_names=selected_columns, where_clause=where_clause)

                DataMigrationFromDB.load_and_optimize(spark=spark, data_df=data_df,output_warehouse_fq_table=output_warehouse_fq_table, 
                                                   output_wh_table_load_strategy=output_wh_table_load_strategy)


    @staticmethod        
    def run_ingestion_pipeline(spark: SparkSession, output_wh_table_load_strategy, output_warehouse_fq_table, 
                               output_table_snapshots_delete_period, db_details,location:str = None, 
                               catalog_minio_bucket:str = None, auto_table_creation= False
                               ):                                             
      
        db_properties = CustomUtils.create_db_properties(db_details=db_details)
        table_name  = db_details.get("db_table", None)
        column_for_partitioning  = db_details.get("partitioning_column", None)
        lower_bound  = db_details.get("lower_bound", Constants.DEFAULT_LOWER_BOUND)
        upper_bound  = db_details.get("upper_bound", Constants.DEFAULT_UPPER_BOUND)
        num_partitions  = db_details.get("num_partitions", Constants.DEFAULT_NUMBER_OF_PARTITIONS)
        selected_columns  = db_details.get("selected_columns", [])
        is_col_for_partition_null_supp  = bool(db_details.get("is_col_for_partition_null_supp", Constants.DEFAULT_IS_COL_FOR_PARTITION_NULL_SUPP))
        records_per_batch  = db_details.get("records_per_batch", Constants.DEFAULT_RECORDS_PER_BATCH)
        
        
        formated_selected_columns = CommonDataUtilities.parse_selected_columns(selected_columns, column_for_partitioning)
        logging.info("selected_columns: {}".format(str(formated_selected_columns)))

        dbOps: BaseDBOperations = DBOperationsFactory().create(db_properties, spark)
        
        
        DataMigrationFromDB.read_and_load_data(dbOps, spark, table_name, column_for_partitioning, formated_selected_columns, lower_bound, 
                                        upper_bound, num_partitions, output_warehouse_fq_table, output_wh_table_load_strategy, 
                                        is_col_for_partition_null_supp,
                                        records_per_batch=records_per_batch
                                        ,catalog_minio_bucket=catalog_minio_bucket
                                        ,location=location
                                        ,auto_table_creation=auto_table_creation
                                        
                                        )


def main():
    try:
       
        db_details = spark_job_args.get("db_details", {})
        operation_type = spark_job_args.get("operation_type", "default")

        
        # Arguments - DW output table
        output_warehouse_fq_table = spark_job_args["output_warehouse_fq_table"] #fq is fully qualified <catalog>.<schema>.<table>
        output_wh_table_load_strategy = spark_job_args.get("output_wh_table_load_strategy", "APPEND")
        output_table_snapshots_delete_period = spark_job_args.get("output_table_snapshots_delete_period", 60)
        location = spark_job_args.get("output_table_location", None)
        catalog_minio_bucket = spark_job_args.get("catalog_minio_bucket", None) #This is from ENV var, no need to add in the config,
        auto_table_creation = bool(spark_job_args.get("auto_table_creation", False)) #whethere to create table if not exist
        
        operation_type = spark_job_args.get("operation_type", None) #

        logging.info("""output_warehouse_fq_table: %s, output_wh_table_load_strategy: %s, output_table_snapshots_delete_period: %s
                """.format(output_warehouse_fq_table, output_wh_table_load_strategy, output_table_snapshots_delete_period))

        if operation_type and operation_type.lower() == 'migration':
            DataMigrationFromDB.run_ingestion_pipeline(spark=spark
                                                        ,output_wh_table_load_strategy=output_wh_table_load_strategy
                                                        ,output_warehouse_fq_table=output_warehouse_fq_table
                                                            ,output_table_snapshots_delete_period=output_table_snapshots_delete_period
                                                            ,db_details=db_details
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
