with open('addons/icofr_demo/icofr_demo_data.xml', 'r') as f:
    content = f.read()

fixed_content = content.replace('\\"', '"')

with open('addons/icofr_demo/icofr_demo_data.xml', 'w') as f:
    f.write(fixed_content)
