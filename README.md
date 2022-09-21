# README #
This README documents all the steps necessary to get the services for IE Starter Kit deployed using AWS SAM.

## What is this repository for? ###
* This repository contains the SAM code for deploying services for IE Starter Kit.
* To use this repository the account repo has to be deployed into an AWS account first.
* The account resources are unique and do not have environments.

## How do I get set up? ###

### Requirements
- [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install-mac.html), follow step 5 to install AWS SAM CLI
- [aws2 cli](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- [cfn-python-lint](https://github.com/aws-cloudformation/cfn-python-lint#install)
- Node (14+) and NPM(6+)

### Setup
- Clone the repository
```sh
git clone git@bitbucket.org:intraedge/services-sam-aws.git
```

- Setup AWS Profile
```bash
aws configure sso  --profile=training
```
Use the URL: https://intraedge.awsapps.com/start#/

- Login with AWS Profile
AWS Session expires every 8 hours, and you might need to re-login using:
```bash
aws sso login --profile=training
```

## Deploy

One time requirement: Deploy the template.yaml in the accounts folder using the following command:
```sh
cd account
# uses the default samconfig.toml in the account directory. to use a different samconfig.toml file please use --config-file option.
sam deploy --profile training

```

>If using sam deploy --guided please refer to the following parameters. Additional data may be required. Refer to the samconfig.toml

### Parameters
- StackName:<br>
Not used in any of the Cloudformation templates. Used for sam deploy.<br>
Example: ie-starter-kit-services-feature1

- ProjectName:<br>
Use a project name.<br>
This is used for exports and imports across stacks.<br>

- Env:<br>
Deployment Environment, can be prod, dev, feature[n] or username. <br>
This is used for exports and imports across stacks.<br>
Examples: feature1, testsam

- DomainName:<br>
Web application domain name for use with Certificate and CloudFront Distribution. <br>
If FeatureDNSPrefix is used then the domain name will resolve with the prefix, e.g. feature.domainname.net<br>
Example: starterkit.intraedge.net
  
- HostedZoneId:<br>
Description: "Hosted Zone ID from Route53 for the above domain name."<br>
> Todo: Store HostedZoneId in a secret path.

- FeatureDNSPrefix:<br>
Feature DNS Prefix for feature branches. e.g: feature1,feature2 For staging, production and integration this will be empty.

### SAM Deployment
Run the following command from the root of the repository.
```sh
# feature1 is used as an example here. Replace with your env name
sam deploy --config-file "samconfigs/feature1.toml" --profile training

# additional options like --no-confirm-changeset and --no-fail-on-empty-changeset could be used depending on the deployment needs.
```
After the stack is deployed, copy your application files to the bucket created by the stack and wait for the CDN to effect.

To delete the stack:
Remove all data from S3 bucket
```sh
# ie-starter-kit-services-feature1 is used here for example. Replace with your stack-name
sam delete --stack-name ie-starter-kit-services-feature1 --region us-east-2 --profile training
```