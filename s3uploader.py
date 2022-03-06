import boto3
import os

from dotenv import load_dotenv

dotenvvals = load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('REGION_NAME')

# Let's use Amazon S3
s3 = boto3.resource('s3')
print("Conectando al bucket...")

for bucket in s3.buckets.all():
    print(bucket.name)

print("Enviando archivo...")

# s3.Object('infoloteria','temp_bot.jpg').upload_file(r'.\source-images\temp_bot.jpg')
s3.Object('infoloteria','post20220302.jpg').upload_file(r'.\source-images\post20220302.jpg')

print("Archivo cargado")