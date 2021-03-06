#Template with default values used to configure dev deployment of fabric8-analytics

#Openshift configuration
export OC_URI='dev.rdu2c.fabric8.io:8443'
export OC_USERNAME='Not set'
export OC_PASSWD='Not set'
export OC_PROJECT=$(whoami)'-greenfield-test'

#AWS credentials
export AWS_ACCESS_KEY_ID='Not set'
export AWS_SECRET_ACCESS_KEY='Not set'

#Github
export GITHUB_API_TOKENS='Not set'
export GITHUB_OAUTH_CONSUMER_KEY='Not set'
export GITHUB_OAUTH_CONSUMER_SECRET='Not set'


export FLASK_APP_SECRET_KEY='Not set'

#AWS RDS configuration variables are use to provision RDS instance
export RDS_ENDPOINT=''
export RDS_INSTANCE_NAME="$OC_USERNAME-bayesiandb"
export RDS_INSTANCE_CLASS='db.t2.micro'
export RDS_DBNAME='postgres'
export RDS_DBADMIN='coreapi'
export RDS_STORAGE=5
export RDS_PASSWORD="$(date +%s | sha256sum | base64 | head -c 32 ;)"
export RDS_SUBNET_GROUP_NAME='dv peering az'