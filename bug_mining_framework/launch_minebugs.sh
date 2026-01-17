#!/bin/bash

# Define an array of GitHub repository URLs
REPOS=(
    "https://github.com/apilayer/restcountries"
  # "https://github.com/nopSolutions/nopCommerce"
  # "https://github.com/octokit/octokit.js"
  # "https://github.com/openblocks-dev/openblocks"
  # "https://github.com/OrchardCMS/OrchardCore"
  # "https://github.com/Jigsaw-Code/outline-server"s
  # "https://github.com/makeplane/plane"
  # "https://github.com/containers/podman"
  # "https://github.com/apache/pulsar"
  # "https://github.com/getredash/redash"
  # "https://github.com/jakartaee/rest"
  # "https://github.com/corona-warn-app/cwa-verification-server"
  # "https://github.com/restsharp/RestSharp"
  # "https://github.com/seaweedfs/seaweedfs"
  # "https://github.com/shopizer-ecommerce/shopizer"
  # "https://github.com/bbernhard/signal-cli-rest-api"
  # "https://github.com/silverapp/silver"
  # "https://github.com/ExpediaGroup/cyclotron"
  # "https://github.com/SAP/spartacus"
  # "https://github.com/openstf/stf"
  # "https://github.com/strapi/strapi"
  # "https://github.com/supabase/supabase"
  # "https://github.com/donnemartin/system-design-primer"
  # "https://github.com/bryanthowell-tableau/tableau_tools"
  # "https://github.com/traefik/traefik"
  # "https://github.com/louislam/uptime-kuma"
  # "https://github.com/vercel/vercel"
  # "https://github.com/WP-API/WP-API"
  # "https://github.com/jackyzha0/quartz"
  # "https://github.com/yt-dlp/yt-dlp"
  # "https://github.com/Netflix/zuul"
  # "https://github.com/treasure-data/digdag"
  # "https://github.com/enviroCar/enviroCar-server/"
  # "https://github.com/ContinuityControl/fdic"
  # "https://github.com/JavierMF/features-service"
  # "https://github.com/confluentinc/kafka-rest"
  # "https://github.com/lujakob/nestjs-realworld-example-app"
  # "https://github.com/fabioformosa/quartz-manager"
  # "https://github.com/RefugeRestrooms/refugerestrooms"
  # "https://github.com/r-spacex/SpaceX-API"
  # "https://github.com/spring-petclinic/spring-petclinic-rest"
  # "https://github.com/swagger-api/swagger-petstore"
  # "https://github.com/elastic/elasticsearch"
)


# Define your GitHub token
GITHUB_TOKEN="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"
ROOT_DIR="./new"

# Loop over each repository
for REPO in "${REPOS[@]}"; do
    REPO_NAME=$(echo "$REPO" | awk -F/ '{print $(NF-1) "-" $NF}')
    LOG_FILE="logs/${REPO_NAME}.log"

    sed -i "s/API_NAME/${REPO_NAME}/g" mine_bugs.sh
    bash mine_bugs.sh "$REPO" "$GITHUB_TOKEN" "$ROOT_DIR"
    sed -i "s/${REPO_NAME}/API_NAME/g" mine_bugs.sh
done

echo "All jobs launched. Check logs/ for progress."