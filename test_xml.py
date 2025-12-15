import xml.etree.ElementTree as ET

try:
    tree = ET.parse(r'D:\development\icofr-odoo\addons\icofr_demo\icofr_demo_data.xml')
    print("XML is valid")
except ET.ParseError as e:
    print(f"XML Parse Error: {e}")
    # Try to find the problematic line
    with open(r'D:\development\icofr-odoo\addons\icofr_demo\icofr_demo_data.xml', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        line_number = e.position[0] if hasattr(e, 'position') else 0
        if line_number > 0:
            print(f"Problematic line {line_number}: {lines[line_number-1].strip()}")