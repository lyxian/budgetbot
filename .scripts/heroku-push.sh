#!/bin/bash 

BRANCH=`git rev-parse --abbrev-ref HEAD`
MSG=$1

if [ $# -eq 1 ]; then

git checkout $BRANCH
git branch -M main 
git add .
git commit -m "$1"
git push -u heroku main
git branch -M $BRANCH

if [ $? -eq 0 ]; then
echo "=====Code pushed to Heroku successfully====="
else
echo "=====Code not push to Heroku====="
fi

else 
echo "Please enter Commit-Message as first argument..."
fi