#!/bin/bash

echo "======================================"
echo "1. HTTP -> HTTPS redirect"
echo "======================================"
curl -s -I http://movies.local/ | grep -E "HTTP/|Location:"

echo
echo "======================================"
echo "2. Load balancing between backends"
echo "======================================"
for i in {1..6}; do
    curl -k -s -D - -o /dev/null \
        https://movies.local/api/movies \
        | grep -i "X-Backend-Instance"
    sleep 1
done

echo
echo "======================================"
echo "3. Backend failover"
echo "======================================"

PID=$(lsof -ti :5001 | head -n 1)

if [ -n "$PID" ]; then
    echo "Stopping backend-1..."
    kill "$PID"
    sleep 2

    echo "Request with backend-1 stopped:"
    curl -k -s -D - -o /dev/null \
        https://movies.local/api/movies \
        | grep -E "HTTP/|X-Backend-Instance"

    echo "Starting backend-1 again..."
    INSTANCE_ID=backend-1 PORT=5001 python backend/app.py \
        > /tmp/backend1.log 2>&1 &

    sleep 3
fi

echo
echo "======================================"
echo "4. /admin without authentication"
echo "======================================"
curl -k -s -o /dev/null \
    -w "HTTP status: %{http_code}\n" \
    https://movies.local/admin/

echo
echo "======================================"
echo "5. Rate limit"
echo "======================================"

seq 1 20 | xargs -P 5 -I {} \
    curl -k -s -o /dev/null \
    -w "%{http_code}\n" \
    https://movies.local/api/movies

echo
echo "======================================"
echo "6. Virtual hosts"
echo "======================================"

echo "movies.local:"
curl -k -s https://movies.local/ \
    | grep -o "<title>[^<]*</title>"

echo "demo.local:"
curl -s http://demo.local/ \
    | grep -o "<title>[^<]*</title>"

echo
echo "======================================"
echo "7. Custom 404"
echo "======================================"

curl -k -s -o /dev/null \
    -w "HTTP status: %{http_code}\n" \
    https://movies.local/this-page-does-not-exist

echo
echo "======================================"
echo "CHECK FINISHED"
echo "======================================"
