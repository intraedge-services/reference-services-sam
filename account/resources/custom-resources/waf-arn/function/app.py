from __future__ import print_function
import boto3
import json
import cfnresponse

def lambda_handler(event, context):
    Region = event["ResourceProperties"]["Region"]
    WebACLName = event["ResourceProperties"]["WebACLName"]
    WAFScope = event["ResourceProperties"]["WAFScope"]
    
    WebACLName = str(WebACLName).strip('[]').strip("'")
    #WAFScope = str(WAFScope).strip('[]]').strip("'")
    
    print("WebACLName is ", WebACLName)
    
    client = boto3.client('wafv2', region_name=Region)

    waf_response = client.list_web_acls(
        Scope=WAFScope #'CLOUDFRONT'
    )

    # Creating JSON from JSONlike structure, prelacing single quotes with double
    waf_as_string = str(waf_response).replace("'", '"')

    # Now we can use it as JSON
    waf_as_json = json.loads(waf_as_string)
    
    webacl_arn = None

    # Find webacl matching the WebACLName in the returened list
    for webacls in waf_as_json['WebACLs']:
        if webacls['Name'] == WebACLName:
            webacl_arn=webacls['ARN']

    responseData = {}
    
    if webacl_arn is None:
        reason = 'No webacl found for', WebACLName
        print(reason)
        responseData['Error'] = reason
        cfnresponse.send(event, context, cfnresponse.FAILED, responseData, "NoResourcePhysicalId")
    else:
        print('webaclArn:',webacl_arn)

        responseData['WebACLArnId'] = webacl_arn
        print(responseData)

        cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, "CustomResourcePhysicalId")
