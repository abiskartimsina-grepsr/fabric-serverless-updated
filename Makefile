PROFILE = null
ENV_VAR = env.json

# STG Deployments
REGION = us-east-1
BUCKET = fabric-api-stg-cloudformation
CF_STACK = fabric-amazon-domain-stack
DEPLOY_PROFILE = staging

.PHONY: run build start invoke deploy-stg validate-template

default: build

start:
	@sam local start-lambda --env-vars $(ENV_VAR)

build:
	@sam build

invoke:
	@sam local invoke $(FUNCTION_NAME) --env-vars $(ENV_VAR) --profile $(PROFILE)

validate-template:
	@sam validate --template-file template.yaml --profile $(PROFILE)
	@sam validate --template-file template.yaml --lint --profile $(PROFILE)

deploy-stg:
	$(MAKE) validate-template &&\
			sam deploy \
			--stack-name $(CF_STACK) \
			--s3-bucket $(BUCKET) \
			--region $(REGION) \
			--profile $(DEPLOY_PROFILE)
