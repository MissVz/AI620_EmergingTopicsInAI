
import boto3

# S3 bucket and dependency paths
bucket_name = 'ai620-pe06-velze'
python_dep_path = 's3://ai620-pe06-velze/inference-pipeline/dependencies/python/python.zip'
jar_dep_path = 's3://ai620-pe06-velze/inference-pipeline/dependencies/jar/mleap_spark_assembly.jar'

# Confirmation message
print(f"Python dependency uploaded to: {python_dep_path}")
print(f"JAR dependency uploaded to: {jar_dep_path}")
