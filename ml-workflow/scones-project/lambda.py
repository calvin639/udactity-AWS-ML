#1 Scones Image Serializer 
import json
import boto3
import base64


s3 = boto3.resource('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    print(event)
    # Get the s3 address from the Step Function event input
    key = event['s3_key']
    bucket = event['s3_bucket']
    print(bucket+key)
    # Download the data from s3 to /tmp/image.png
    s3.meta.client.download_file(bucket, key, '/tmp/image.png')
    print("Donwloaded Image")
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }


#2 Scones Projector Lambda
import json
import boto3 
import base64


# Fill this in with the name of your deployed model
ENDPOINT = 'scones-endpoint'
runtime= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):

    # Decode the image data
    event=event['body']
    image = base64.b64decode(event['image_data'])

    # Instantiate a Predictor
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT,
                                       ContentType='image/png',
                                       Body=image)

    # For this model the IdentitySerializer needs to be "image/png"
    #predictor.serializer = IdentitySerializer("image/png")
    
    
    # We return the data back to the Step Function    
    result = json.loads(response['Body'].read().decode())
    event["inferences"] = result
    print(event)
    return {
        'statusCode': 200,
        'body': event
    }


#3 Scones Threshold Lambda
import json
import csv 
import boto3

THRESHOLD = .8

def lambda_handler(event, context):
    # Grab the inferences from the event
    event = event['body']
    print(event)
    inferences = event["inferences"]
    d={inferences[0]:'motor-bike',inferences[1]:'bicycle'}
    # Check if any values in our inferences are above THRESHOLD
    print("checking threshold")
    meets_threshold = THRESHOLD < max(inferences)
    prob = max(inferences)
    guess = d[prob]
    real = event['s3_key'].split('/')[2].split('_')[0]
    res = real+","+guess+","+str(prob)
    print(res)
    
    #Add results to CSV
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(event['s3_bucket'])
    csvPath = 'scones-project/results/sconesResults.csv'
    # download s3 csv file to lambda tmp folder
    local_file_name = '/tmp/res.csv' #
    bucket.download_file(csvPath,local_file_name)
    # write the data into '/tmp' folder
    with open('/tmp/res.csv','a') as infile:
        infile.write(res)
            
    # upload file from tmp to s3 key
    bucket.upload_file('/tmp/res.csv', csvPath)

    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        print("Threshold passed, I am {}% sure that this is a {}".format(prob,guess))
        event['prediction']=d[max(inferences)]
        pass
    else:
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
