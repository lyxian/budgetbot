#!/bin/bash

exportFunc() {
    ENV=`echo $1 | cut -d / -f2 | tr [a-z] [A-Z]`
    VALUE=`cat $1`
    APP=$2
    # export $ENV=$VALUE
    heroku config:set $ENV=$VALUE --app $APP
}

exportFunc .config/key yxian-budget-test
exportFunc .config/secret_telegram yxian-budget-test

exit

API=`python3 -c "import json; file = open('.config/heroku.json'); data=json.loads(file.read()); print(data['api_key']); file.close()"`

curlSettings="-H \"Accept: application/vnd.heroku+json; version=3\" -H \"Content-Type: application/json\""
curlSettings="$curlSettings -H \"Authorization: Bearer ${API}\""

NAME="yxian-budget-test"
# STACK="heroku/python"
STACK="heroku-20"

URL="https://api.heroku.com/apps"

payload="'{\"name\": \"${NAME}\", \"stack\": \"${STACK}\"}'"

# DEST=.scripts/response.json
# eval "curl $curlSettings -X POST -d $payload $URL" > $DEST

DEST=.scripts/response1.json
eval "curl $curlSettings -X PUT https://api.heroku.com/apps/$NAME/buildpack-installations \
  -d '{
  \"updates\": [
    {
      \"buildpack\": \"https://github.com/heroku/heroku-buildpack-python\"
    }
  ]
}'"  > $DEST


# curl -n -X POST  \
#   -d '{
#   "name": "example",
#   "region": "01234567-89ab-cdef-0123-456789abcdef",
#   "stack": "01234567-89ab-cdef-0123-456789abcdef"
# }' \