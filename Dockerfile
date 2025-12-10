FROM odoo:19.0

# Set working directory
WORKDIR /opt/odoo

# Copy custom configuration
COPY ./odoo.conf /etc/odoo/