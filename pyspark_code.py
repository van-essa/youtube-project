import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from botocore.exceptions import ClientError  # Import AWS error handling

# @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Predicate pushdown to filter data from the Glue Data Catalog
predicate_pushdown = "region in ('ca','gb','us')"

# Create DynamicFrame from S3
AmazonS3_node = glueContext.create_dynamic_frame.from_options(
    format_options={"withHeader": True, "separator": ","},  # CSV format options
    connection_type="s3",
    format="csv",  # Since the file encountered was a CSV, update format to "csv"
    connection_options={"paths": ["s3://vanessandersson-deproject-on-youtube-cleansed-useast1-dev/youtube/raw_statistics/"], "recurse": True},
    transformation_ctx="AmazonS3_node"
)

# Create DynamicFrame from Glue Data Catalog with predicate pushdown
try:
    AWSGlueDataCatalog_node = glueContext.create_dynamic_frame.from_catalog(
        database="de-youtube-raw",
        table_name="raw_statistics",
        transformation_ctx="AWSGlueDataCatalog_node",
        push_down_predicate=predicate_pushdown  # Apply the predicate pushdown
    )
except ClientError as e:
    if e.response['Error']['Code'] == 'EntityNotFoundException':
        print(f"Error: The specified database or table was not found. Details: {e}")
        sys.exit(1)
    else:
        raise

# Combine data from both sources (optional, if they have the same schema)
combined_data = AmazonS3_node.union(AWSGlueDataCatalog_node)

# Transform combined data to DataFrame
output_data = combined_data.toDF()

# Convert back to DynamicFrame for writing
df_final_output = DynamicFrame.fromDF(output_data, glueContext, "df_final_output")

# Write the final output back to S3
datasink = glueContext.write_dynamic_frame.from_options(
    frame=df_final_output,
    connection_type="s3",
    connection_options={"path": "s3://vanessandersson-deproject-on-youtube-cleansed-useast1-dev/youtube/processed_data/", "partitionKeys": ["region"]},
    format="parquet",  # Writing the final data in Parquet format
    transformation_ctx="datasink"
)

job.commit()
