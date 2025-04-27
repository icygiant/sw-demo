#!/bin/bash

# Load variables from .env
export $(grep -v '^#' .env | xargs)

# Connect using psql
psql "host=$PG_HOST port=$PG_PORT dbname=$PG_DB user=$PG_USER password=$PG_PASSWORD sslmode=require"
