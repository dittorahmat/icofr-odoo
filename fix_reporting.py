
import re

with open('addons/icofr_demo/icofr_demo_data.xml', 'r') as f:
    content = f.read()

# Regular expression to find all <record ... model="icofr.finding"> ... </record> blocks
# and ensure they have the reporting fields.
finding_pattern = re.compile(r'(<record id="[^" ]+" model="icofr.finding">)(.*?)(</record>)', re.DOTALL)

def add_flags(match):
    header = match.group(1)
    body = match.group(2)
    footer = match.group(3)
    
    # Check if flags are already there
    if 'reported_to_ceo' not in body:
        body = '\n        <field name="reported_to_ceo" eval="True"/>' + body
    if 'reported_to_audit_committee' not in body:
        body = '\n        <field name="reported_to_audit_committee" eval="True"/>' + body
    if 'reported_to_board' not in body:
        body = '\n        <field name="reported_to_board" eval="True"/>' + body
    if 'reported_to_mgmt_assessment' not in body:
        body = '\n        <field name="reported_to_mgmt_assessment" eval="True"/>' + body
        
    return header + body + footer

fixed_content = finding_pattern.sub(add_flags, content)

with open('addons/icofr_demo/icofr_demo_data.xml', 'w') as f:
    f.write(fixed_content)

