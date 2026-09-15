#!/bin/bash
# Cria múltiplos bancos a partir da variável POSTGRES_MULTIPLE_DATABASES (lista separada por vírgula).
set -e

if [ -n "$POSTGRES_MULTIPLE_DATABASES" ]; then
  echo "Criando bancos: $POSTGRES_MULTIPLE_DATABASES"
  for db in $(echo "$POSTGRES_MULTIPLE_DATABASES" | tr ',' ' '); do
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
      CREATE DATABASE "$db";
EOSQL
  done
fi
