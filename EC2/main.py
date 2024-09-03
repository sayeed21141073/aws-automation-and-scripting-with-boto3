"""We will do two tasks. 1. Create EC2. 
2. Do SSH connection using Paramiko."""

import boto3
import paramiko

client = boto3.client('ec2')

"""Task01: Create an EC2 instance"""

# Step01: Create a security group and add inbound rule
security_group_name = "security-group-for-sayeed-boto3-learnings"
security_group_description = "Just another security group......."

security_group = client.create_security_group(
    Description=security_group_description,
    GroupName=security_group_name,
)

# We need the 'GroupId'
security_group_id = security_group['GroupId']
print(security_group_id)

# Add inbound rules (Allowing port 22 for SSH connection)
client.authorize_security_group_ingress(
    GroupId=security_group_id,
    IpProtocol='tcp',
    FromPort=22,
    ToPort=22,
    CidrIp='0.0.0.0/0'
)

print("Security Group Created Successfully!!!")

# Step02: Creating Key-Pair
key_pair_name = 'my-key-pair-4'

response = client.create_key_pair(KeyName=key_pair_name)

key_pair_material = response['KeyMaterial']  # KeyMaterial is the private key

# Save the key pair material to a file named 'my-key-pair.pem' in the current directory
with open('my-key-pair-4.pem', 'w') as f:
    f.write(key_pair_material)

print("Key-Pair Created Successfully!")


# Step03: Launch the EC2 instance

instance_type = 't2.micro'
image_id = 'ami-066784287e358dad1'  # Amazon Linux ami ID

response = client.run_instances(
    ImageId=image_id,
    InstanceType=instance_type,
    MinCount=1,
    MaxCount=1,
    KeyName=key_pair_name,
    SecurityGroupIds=[security_group_id]
)

instance_id = response['Instances'][0]['InstanceId']
print(f"Instance Id is {instance_id}")

# Step 04: Wait for the instance to run, otherwise we can not proceed further.
    # we need to use waiter
waiter = client.get_waiter('instance_running')
waiter.wait(InstanceIds=[instance_id])
print("Instance is in running state. Great!")

"""Task02: Doing a SSH connection."""
# Get public IP first
instance = client.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
public_ip = instance['PublicIpAddress']

print("Got Public IP")
# Remember, we are using paramiko package from now on, not boto3.
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print("AutoAddPolicy() done")


# Load private key
private_key = paramiko.RSAKey.from_private_key_file('my-key-pair-4.pem')
print("Got Private IP")

# Connect to the instance
ssh.connect(hostname=public_ip, username='ec2-user', pkey=private_key) 
print("SSH connection done!")

# Execute commands on the instance
stdin, stdout, stderr = ssh.exec_command('ls')
print(stdout.read().decode())
print("Command Execution Done")

# Close the SSH connection
ssh.close()

"""Important: Terminate EC2"""

ec2_termination = client.terminate_instances(
    InstanceIds=[instance_id]
)

print("EC2 terminated successfully.")
