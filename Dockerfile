FROM odoo:19.0

USER root

# Install dependencies for Excel parsing using system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-openpyxl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /opt/odoo

# Copy custom configuration
COPY ./odoo.conf /etc/odoo/

USER odoo