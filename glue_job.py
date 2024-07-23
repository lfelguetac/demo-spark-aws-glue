import boto3

# Crear un cliente de AWS Glue
glue = boto3.client('glue', region_name='us-east-2')

# Crear un trabajo de Glue
response_create = glue.create_job(
    Name='my-glue-job',
    Role='arn:aws:iam::393573696710:role/AWSGlueServiceRole',
    ExecutionProperty={
        'MaxConcurrentRuns': 1
    },
    Command={
        'Name': 'glueetl',
        'ScriptLocation': 's3://my-bucket/scripts/demo_pyspark.py',
        'PythonVersion': '3'
    },
    DefaultArguments={
        '--TempDir': 's3://my-bucket/temp/',
        '--job-bookmark-option': 'job-bookmark-enable',
        '--extra-py-files': 's3://my-bucket/scripts/dependencies.zip'
    },
    MaxRetries=3,
    Timeout=2880,
    NumberOfWorkers=2,
    WorkerType='Standard'
)

print("Job creation response:", response_create)

# Iniciar una ejecución del trabajo de Glue
response_start = glue.start_job_run(JobName='my-glue-job')
print("Job start response:", response_start)

# Obtener el estado de la ejecución del trabajo
response_status = glue.get_job_run(JobName='my-glue-job', RunId=response_start['JobRunId'])
print("Job run status:", response_status)
