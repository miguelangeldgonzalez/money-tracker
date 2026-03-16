#!/bin/bash

# 1. Obtener el timestamp exacto del servidor de Binance
# Esto evita por completo el error de desincronización de tu reloj local
TIMESTAMP=$(curl -s "https://api.binance.com/api/v3/time" | grep -o '[0-9]\{13\}')

# 2. Definir los parámetros
# Agregamos recvWindow=60000 para dar un margen de 60 segundos
QUERY="recvWindow=60000&timestamp=$TIMESTAMP"

# 3. Generar la firma HMAC SHA256
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET_KEY" | sed 's/^.* //')

# 4. Ejecutar el curl
curl -H "X-MBX-APIKEY: $API_KEY" \
     -X GET "https://api.binance.com/sapi/v1/c2c/orderMatch/listUserOrderHistory?$QUERY&signature=$SIGNATURE"