# my_pyspark_script.py

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, substring, when, count

# Obtener los argumentos del job
args = getResolvedOptions(sys.argv, [
    'JOB_NAME', 
    'S3_INPUT_PATH', 
    'S3_TEMP_DIR', 
    'S3_OUTPUT_PATH'
])

# Crear un SparkContext y GlueContext
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Crear un job de Glue
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Leer datos desde S3 (archivo CSV, una palabra por línea)
df = spark.read.text(args['S3_INPUT_PATH'])

# Extraer la primera letra de cada palabra
df_with_letters = df.withColumn('first_letter', substring(col('value'), 1, 1))

# Convertir a mayúsculas para asegurar que todas las letras están en el mismo formato
df_with_letters = df_with_letters.withColumn('first_letter', col('first_letter').upper())

# Contar la frecuencia de cada letra del abecedario
letter_counts = df_with_letters.groupBy('first_letter').agg(count('*').alias('count'))

# Escribir los resultados en S3 en formato CSV
letter_counts.write \
  .format("csv") \
  .option("path", args['S3_OUTPUT_PATH']) \
  .option("header", "true") \
  .mode("overwrite") \
  .save()

# Finalizar el job
job.commit()
