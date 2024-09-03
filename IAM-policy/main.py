"""The IAM user boto3 is connected to has full administrative access.
Otherwise the below code will not work."""

import boto3

client = boto3.client('iam')

"""Task 01: List all users"""

response = client.list_users()
print(response)

"""Task02: List all groups"""

result = client.list_groups()
print(result)

"""Task 03: Create a new user"""

user = client.create_user(
    UserName='SayeedZaman',
    Tags=[
        {
            'Key': 'Developer',
            'Value': 'EC2 related all access given'
        },
    ]
)
print(user)

"""Task 04: Create a new group"""

group = client.create_group(
    GroupName='Developer'
)
print(group)

"""Task 05: Add user to group."""

adding_user_to_group = client.add_user_to_group(
    GroupName = 'Developer',
    UserName = 'SayeedZaman'   
)
print("User added to group successfully")

#Imp: removing user from group is a prerequisite to delete group or user

client.remove_user_from_group(
    GroupName='Developer',
    UserName='SayeedZaman'
)
print("user removed from group.")

"""Task 06: Delete user"""

client.delete_user(
    UserName='SayeedZaman'
)
print("user deleted successfully.")

"""Task 07: Delete group"""

client.delete_group(
    GroupName='Developer'
)
print("Group deleted successfully.")