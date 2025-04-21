server {
    listen ${LISTEN_PORT};

    server_name ${SER_NAME};

    location ^~ /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl;

    server_name ${SER_NAME};

    # ssl_certificate /etc/letsencrypt/live/${CRT_DNS}/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/${CRT_DNS}/privkey.pem;

    ssl_certificate /etc/letsencrypt/live/neotechwave.net/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/neotechwave.net/privkey.pem;

    location /static {
        alias /vol/static;
    }

    location /static/media {
        alias /vol/media;
    }

    location / {
        include              gunicorn_headers;
        proxy_redirect       off;
        proxy_pass           http://${APP_HOST}:${APP_PORT};
        client_max_body_size 10M;
    }
}
