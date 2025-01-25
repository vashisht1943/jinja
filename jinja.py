import os
import jinja2
import pdfkit
from datetime import datetime
from legend_accents.data import data as ts_data

cur_time = datetime.now()
data = ts_data
cur_dir = os.getcwd()

templateLoader = jinja2.FileSystemLoader(searchpath=cur_dir)
jinja_environment = jinja2.Environment(loader=templateLoader)
template = jinja_environment.get_template("legend_accents/template.html")
def replace_spaces_in_keys(data):
    if isinstance(data, dict):
        updated_data = {}
        for key, value in data.items():
            new_key = key.replace(" ", "_")
            new_key = key.replace("-", "_")
            updated_data[new_key] = replace_spaces_in_keys(value)
        return updated_data
    elif isinstance(data, list):
        return [replace_spaces_in_keys(item) for item in data]
    else:
        return data

output = template.render(data, all_jinja_data=data)

path_html = os.path.join(cur_dir, 'legend_accents/output.html')
with open(path_html, 'w', encoding='utf-8') as file:
    file.write(output)

path_pdf = os.path.join(cur_dir, 'legend_accents/output.pdf')
path_to_wkhtmltopdf = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

if "legend" in path_pdf.lower():

    tenant_address = data.get('tenant_address', '')
    header_template = jinja_environment.get_template("legend_accents/header.html")
    header_output = header_template.render(data)
    path_header = os.path.join(cur_dir, 'legend_accents/header_temp.html')
    with open(path_header, 'w', encoding='utf-8') as file:
        file.write(header_output)
    pdfkit.from_file(path_html, path_pdf, configuration=config, options={
            "header-html": path_header,
            "margin-left": "10mm",
            "margin-right": "10mm",
            "header-spacing": "5",
            "margin-bottom": "15mm",
            "page-width": "21.59cm",
            "page-height": "27.94cm",
        })
else:
    pdfkit.from_file(path_html, path_pdf, configuration=config, options={
        # "footer-font-name": "Open Sans",
        # "footer-font-size": "8",
        # "footer-right": "Page No.- [page]",
        # "footer-center": "sagebrookhome.com | elevarre.com",
        # "footer-spacing": "5",
        "margin-bottom": "15mm",
        "page-width": "21.59cm",          
        "page-height": "27.94cm",
    })

print(f"PDF generated and saved to {path_pdf}")
print("Time taken:", datetime.now() - cur_time)