
import sagemaker
from sagemaker import get_execution_role
from sagemaker.amazon.amazon_estimator import NTM

role = get_execution_role()
s3_data = 's3://ai620-pe06-velze/preprocessed-data-location'
s3_output = 's3://ai620-pe06-velze/output-location'

ntm = NTM(
    role=role,
    train_instance_count=1,
    train_instance_type='ml.m4.xlarge',
    num_topics=10,
    output_path=s3_output,
    base_job_name='ntm-news-headlines'
)

ntm.fit({'train': s3_data})
print("Model training complete.")
