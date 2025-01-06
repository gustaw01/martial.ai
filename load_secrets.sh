#!/bin/bash

HCP_API_TOKEN=$(curl --location "https://auth.idp.hashicorp.com/oauth2/token" \
--header "Content-Type: application/x-www-form-urlencoded" \
--data-urlencode "client_id=$HCP_CLIENT_ID" \
--data-urlencode "client_secret=$HCP_CLIENT_SECRET" \
--data-urlencode "grant_type=client_credentials" \
--data-urlencode "audience=https://api.hashicorp.cloud" | jq -r .access_token)

SECRETS=$(curl \
--location "https://api.cloud.hashicorp.com/secrets/2023-11-28/organizations/ca33a12a-7a7e-4cb5-a9a6-2ec4feb47366/projects/959f0380-aeb2-45ce-8462-25d987c99782/apps/martial-ai/secrets:open" \
--request GET \
--header "Authorization: Bearer $HCP_API_TOKEN" | jq)

# Parsowanie odpowiedzi z Vaulta
echo "$SECRETS" | jq -r '.secrets[] | "export \(.name)=\(.static_version.value)"' > /tmp/vault_env.sh

# Załadowanie zmiennych środowiskowych do aktualnej sesji
source /tmp/vault_env.sh

echo "Załadowane zmienne środowiskowe:"
echo "$SECRETS" | jq -r '.secrets[] | .name'

# Usunięcie pliku tymczasowego
rm /tmp/vault_env.sh