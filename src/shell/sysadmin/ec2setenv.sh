# source ec2setenv.sh
export JAVA_HOME=/System/Library/Frameworks/JavaVM.framework/Home
export EC2_HOME=/usr/local/sdk/aws/latest
export PATH=$PATH:$EC2_HOME/bin
export EC2_PRIVATE_KEY=$HOME/.ssh/pk-${SECRET_ID}.pem
export EC2_CERT=$HOME/.ssh/cert-${SECRET_ID}.pem
export EC2_URL=http://ec2.ap-southeast-1.amazonaws.com

PS1=(ec2enabled)$PS1
