FROM php:8.2-apache

RUN docker-php-ext-install pdo pdo_mysql && \
    apt-get update && apt-get install -y libcurl4-openssl-dev && \
    docker-php-ext-install curl && \
    rm -rf /var/lib/apt/lists/*

RUN a2enmod rewrite

WORKDIR /var/www/html

EXPOSE 80
