import boto3

"""Task 01: List all available buckets"""

client = boto3.client('s3')
response = client.list_buckets()
print(f"Here are the list of buckets {response}")

"""Task 02: Create a new bucket"""

my_bucket = client.create_bucket(Bucket = 'sayeed21141073-my-bucket')
print("bucket successfully created!")

"""Task 03: Create a text file and upload it to the bucket"""

#Creating the text file
with open('myfile.txt', 'w') as file:
    file.write('This is a text file for uplaod to S3 bucket.')
    print("myfile.txt successfully created!")

#Uploading the text file to bucket
client.upload_file(Filename = "myfile.txt",
                  Bucket = 'sayeed21141073-my-bucket',
                  Key = 'myfileS3.txt')

# Filename = The file I am uploading from my PC
# Key = the file will be saved as this name on S3 bucket
print("File successfully uploaded")

""" Task 04: List all objects """

objects = client.list_objects_v2(Bucket = 'sayeed21141073-my-bucket')
print(f"Here are all objects {objects}")

"""Task 05: Create a URL so that my friend can download the file within the next 5 minutes."""
presigned_url = client.generate_presigned_url(
    ClientMethod='get_object',
    Params={
        'Bucket': 'sayeed21141073-my-bucket',
        'Key': 'myfileS3.txt'
    },
    ExpiresIn=300 # URL will expire in 5 minutes or 300 seconds
)
print(f"Pls click on this link to download the file within 5 minutes.\n{presigned_url}")

"""Task 06: Download the objects and delete it after"""

client.download_file(Bucket = 'sayeed21141073-my-bucket',
                     Key = 'myfileS3.txt',
                     Filename = 'myfile-downloaded1.txt') # Filename means the Key will be downloaded as this name

print("File downloaded successfully!")

"""Task 07: Delete the object"""

client.delete_object(
    Bucket='sayeed21141073-my-bucket',
    Key='myfileS3.txt')
print("Object deleted successfully!")

"""Task 08: Delete the bucket"""

client.delete_bucket(Bucket='sayeed21141073-my-bucket')
print("Bucket deleted successfully!!!")