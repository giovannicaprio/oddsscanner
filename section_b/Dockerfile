FROM php:8.2-apache

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libxml2-dev \
    curl \
    zip \
    unzip \
    && docker-php-ext-install xml

# Enable Apache modules
RUN a2enmod rewrite

# Install Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Set working directory
WORKDIR /var/www/html

# Copy composer files first
COPY composer.json composer.lock ./

# Install dependencies
RUN composer install --no-scripts --no-autoloader

# Copy source code
COPY . .

# Generate autoloader
RUN composer dump-autoload --optimize

# Create necessary directories if they don't exist
RUN mkdir -p /var/www/html/views/layouts \
    && mkdir -p /var/www/html/views/home \
    && mkdir -p /var/www/html/controllers \
    && mkdir -p /var/www/html/core \
    && mkdir -p /var/www/html/config \
    && mkdir -p /var/www/html/models \
    && mkdir -p /var/www/html/storage/rates

# Configure Apache
RUN echo '<VirtualHost *:80>\n\
    DocumentRoot /var/www/html/src\n\
    <Directory /var/www/html/src>\n\
        Options Indexes FollowSymLinks\n\
        AllowOverride All\n\
        Require all granted\n\
    </Directory>\n\
</VirtualHost>' > /etc/apache2/sites-available/000-default.conf

# Set permissions
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html \
    && chmod -R 777 /var/www/html/storage

# Configure PHP
RUN echo "allow_url_fopen = On" >> /usr/local/etc/php/php.ini 