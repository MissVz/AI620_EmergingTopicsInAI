from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, StopWordsRemover, CountVectorizer, IDF
from pyspark.ml import Pipeline
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import col
import sys

# 1. Validate and retrieve arguments
args = getResolvedOptions(
    sys.argv,
    ['S3_INPUT_BUCKET', 'S3_INPUT_KEY_PREFIX', 'S3_INPUT_FILENAME', 'S3_OUTPUT_BUCKET', 'S3_OUTPUT_KEY_PREFIX']
)

# Assign input and output paths
input_path = f"s3://{args['S3_INPUT_BUCKET']}/{args['S3_INPUT_KEY_PREFIX']}/{args['S3_INPUT_FILENAME']}"
output_path = f"s3://{args['S3_OUTPUT_BUCKET']}/{args['S3_OUTPUT_KEY_PREFIX']}/features"
print(f"Input Path: {input_path}")
print(f"Output Path: {output_path}")

# 2. Initialize Spark session
spark = SparkSession.builder.appName("DataPreprocessing").getOrCreate()
print("Spark session initialized.")

# 3. Read input data
data = spark.read.option("header", "true").csv(input_path)
print("Reading data from S3...")
print(f"Schema: {data.printSchema()}")
print(f"Sample Data: {data.show(5)}")

# 4. Define transformations
tokenizer = Tokenizer(inputCol="headline_text", outputCol="words")
remover = StopWordsRemover(inputCol="words", outputCol="filtered")
vectorizer = CountVectorizer(inputCol="filtered", outputCol="tf", vocabSize=200, minDF=2)
idf = IDF(inputCol="tf", outputCol="features")

# 5. Build and execute pipeline
pipeline = Pipeline(stages=[tokenizer, remover, vectorizer, idf])
model = pipeline.fit(data)

# Debugging: Check transformations
print("Transforming data...")
features = model.transform(data)
print(f"Sample Transformed Data: {features.show(5)}")

# 6. Convert complex types and save output
features_string_df = features.withColumn("features", col("features").cast("string"))

# Debugging: Check the converted data
print("Converted DataFrame:")
features_string_df.show(5)

# Save the converted DataFrame to CSV
features_string_df.select("features").write.option("delimiter", "\t").csv(output_path)
print("Preprocessing completed successfully. Data saved to S3.")
