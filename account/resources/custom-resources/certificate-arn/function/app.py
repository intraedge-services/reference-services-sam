from __future__ import print_function
import boto3
import json
import cfnresponse

def lambda_handler(event, context):
    region = event["ResourceProperties"]["Region"]
    domain = event["ResourceProperties"]["Domain"]
    
    domain = str(domain).strip('[]').strip("'")
    
    print("Domain is ", domain)
    print("Region is ", region)
    
    acm_client = boto3.client('acm', region_name=region)
    acm_response = acm_client.list_certificates()

    # Creating JSON from JSONlike structure, prelacing single quotes with double
    acm_as_string = str(acm_response).replace("'", '"')

    # Now we can use it as JSON
    acm_as_json = json.loads(acm_as_string)
    
    certificate_arn = None

    # Find certificate matching the domain in the returened list
    for certificates in acm_as_json['CertificateSummaryList']:
        if certificates['DomainName'] == domain:
            certificate_arn=certificates['CertificateArn']
    
    responseData = {}
    
    if certificate_arn is None:
        reason = 'No certificate found for', domain
        print(reason)
        responseData['Error'] = reason
        cfnresponse.send(event, context, cfnresponse.FAILED, responseData, "NoResourcePhysicalId")
    else:
        print('CertificateArn:',certificate_arn)

        responseData['CertificateArnId'] = certificate_arn
        print(responseData)

        cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, "CustomResourcePhysicalId")
