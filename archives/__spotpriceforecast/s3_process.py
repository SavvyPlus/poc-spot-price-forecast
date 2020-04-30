import logging 

import boto3

s3 = boto3.client('s3')

def move_file(src_bucket, src_key, dst_bucket, dst_key):
    logging.info('Moving {} to {} from {} to {}'.format(src_key,
                                                       dst_key,
                                                       src_bucket,
                                                       dst_bucket))
    s3.copy({'Bucket': src_bucket, 'Key': src_key}, dst_bucket, dst_key)
    s3.delete_object(Bucket=src_bucket, Key=src_key)
    logging.debug('Moved {} to {} from {} to {}'.format(src_key,
                                                       dst_key,
                                                       src_bucket,
                                                       dst_bucket))


def copy_file(src_bucket, src_key, dst_bucket, dst_key):
    logging.info('Copying {} to {} from {} to {}'.format(src_key,
                                                        dst_key,
                                                        src_bucket,
                                                        dst_bucket))
    return s3.copy({'Bucket': src_bucket, 'Key': src_key}, dst_bucket, dst_key)
   


def put_file(bucket, key, body):
    logging.info('Put file {} to {}'.format(key, bucket))
    return s3.put_object(Bucket=bucket, Key=key, Body=body)
    

def get_object(bucket, key):
    return s3.get_object(Bucket=bucket, Key=key)


def get_object_or_404(bucket, key):
    try:
        return get_object_byte(bucket, key)
    except s3.exceptions.ClientError as e:
        print(e)
        return None


def get_object_byte(bucket, key):
    obj = s3.get_object(Bucket=bucket, Key=key)
    return obj['Body'].read()


def delete_object(bucket, key):
    logging.debug('Deleting file {} in {}'.format(key, bucket))
    return s3.delete_object(Bucket=bucket, Key=key)    