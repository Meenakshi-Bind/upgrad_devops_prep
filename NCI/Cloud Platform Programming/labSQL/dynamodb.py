import logging
import boto3
from botocore.exceptions import ClientError

class DynamoDBDemo:
    
    
    def create_table(self, table_name, key_schema, attribute_definitions, provisioned_throughput, region):
        
        try:
            dynamodb_resource = boto3.resource("dynamodb", region_name=region)
            print("\ncreating the table {} ...".format(table_name))
            self.table = dynamodb_resource.create_table(TableName=table_name, KeySchema=key_schema, AttributeDefinitions=attribute_definitions,
                ProvisionedThroughput=provisioned_throughput)

            # Wait until the table exists.
            self.table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
            
        except ClientError as e:
            logging.error(e)
            return False
        return True

 
        

    def store_an_item(self, region, table_name, item):
        try:
            print("\nstoring the item {} in the table {} ...".format(item, table_name))
            dynamodb_resource = boto3.resource("dynamodb", region_name=region)
            table = dynamodb_resource.Table(table_name)
            table.put_item(Item=item)
        
        except ClientError as e:
            logging.error(e)
            return False
        return True
        
        
     
    def get_an_item(self, region, table_name, key):
        try:
            print("\nretrieving the item with the key {} from the table {} ...".format(key, table_name))
            dynamodb_resource = boto3.resource("dynamodb", region_name=region)
            table = dynamodb_resource.Table(table_name)
            response = table.get_item(Key=key)
            item = response['Item']
            print(item)
        
        except ClientError as e:
            logging.error(e)
            return False
        return True
            
 

def main():
    ''' Note that if you are running this demo using the AWS Academy Learner Lab,
        there is a restriction on the AWS Regions that can be used, namely
        all service access is limited to the us-east-1 and us-west-2 AWS Regions
        unless mentioned otherwise'''
        
    # TASK: Create a DynamoDB table
        
    region = 'us-east-1'
    d = DynamoDBDemo()
    
    table_name="music"
    
    key_schema=[
        {
            "AttributeName": "artist",
            "KeyType": "HASH"
        },
        {
            'AttributeName': 'song',
            'KeyType': 'RANGE'
        }
    ]
    
    attribute_definitions=[
        {
            "AttributeName": "artist",
            "AttributeType": "S"
        },
        {
            "AttributeName": "song",
            "AttributeType": "S"
        }
        
    ]
    
    provisioned_throughput={
        "ReadCapacityUnits": 1,
        "WriteCapacityUnits": 1
    }
    
    d.create_table(table_name, key_schema, attribute_definitions, provisioned_throughput, region)
   
    
    # TASK: Store data (items) into a DynamoDB table
    item = {
        "artist": "Pink Floyd",
        "song": "Us and Them",
        "album": "The Dark Side of the Moon",
        "year": 1973
    }
    
    d.store_an_item(region, table_name, item)
    
    item = {
        "artist": "Michael Jackson",
        "song": "Billie Jean",
        "album": "Thriller",
        "length_seconds": 294
    }
    
    d.store_an_item(region, table_name, item)
    
    # TASK: Retrieve the attributes of the item with the given primary key
    
    key_info={
        "artist": "Pink Floyd",
        "song": "Us and Them",
    }
    
    d.get_an_item(region, table_name, key_info)
    

    
if __name__ == '__main__':
    main()
