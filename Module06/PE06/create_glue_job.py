
import boto3

# Glue client
glue_client = boto3.client('glue')

response = glue_client.create_job(
    Name="PreprocessDataJob",
    Role='arn:aws:iam::your-role-arn',  # Replace with your SageMaker IAM Role ARN
    Command={'Name': 'glueetl', 'ScriptLocation': 's3://ai620-pe06-velze/inference-pipeline/dependencies/preprocess_data.py'},
    DefaultArguments={'--job-language': 'python'},
    MaxRetries=1,
    GlueVersion="2.0",
    Timeout=600
)

print("Glue job created successfully:", response)
