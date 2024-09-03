import boto3

client = boto3.client('dynamodb')

"""Task01: Create a table."""

table_name = 'movies'
attributes = [
    {
        'AttributeName': 'Title',
        'AttributeType': 'S'
    },
    {
        'AttributeName': 'Rating',
        'AttributeType': 'N'
    }
]

key_schema = [
    {
        'AttributeName': 'Title',
        'KeyType': 'HASH'
    },
    {
        'AttributeName': 'Rating',
        'KeyType': 'RANGE'
    },
]

provisioned_throughput = {
    'ReadCapacityUnits': 10,
    'WriteCapacityUnits': 10
}

response = client.create_table(
    TableName=table_name,
    AttributeDefinitions=attributes,
    KeySchema=key_schema,
    ProvisionedThroughput=provisioned_throughput
)

"""Task02: Put value to the item. """

entry = {
    'Title':{'S':'Parasite'},
    'Director': {'S': 'Bong Joon-ho'},
    'Year':{'N': '2019'},
    'Rating': {'N': '5'}
}

value = client.put_item(
    TableName = table_name,
    Item = entry
)
#print(value)"""

"""Task03: Read the item"""

item_key = {'Title':{'S':'Parasite'},
            'Rating': {'N': '5'}
}
            
response = client.get_item(TableName = table_name, Key = item_key)
print(response['Item'])

"""Task04: Update Key"""

update = 'SET Director = :r'

updated_value = client.update_item(
    TableName = table_name,
    Key = item_key,
    UpdateExpression = update,
    ExpressionAttributeValues = {':r': {'S':'Updated value: Bong Joon-ho is the director.'}}
)

response = client.get_item(TableName = table_name, Key = item_key)
print(response['Item'])

"""Task05: Delete the item"""

client.delete_item(TableName = table_name, Key = item_key)

"""Task06: Delete the table."""

delete_table = client.delete_table(
    TableName = table_name
)
print("Table Deleted!!!")