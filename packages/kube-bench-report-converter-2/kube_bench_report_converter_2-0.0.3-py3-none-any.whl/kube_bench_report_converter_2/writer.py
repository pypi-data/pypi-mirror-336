import csv
import sys

def write_to_file(findings, output_file_path):
    with open(output_file_path, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file, quoting=csv.QUOTE_ALL, dialect='excel')
        csv_writer.writerow(['Id', 'Category', 'Subcategory', 'Rating', 'Description', 'Remediation'])

        for anchor, finding in findings.items():
            remediation = finding['remediation']['description'] if finding.get('remediation') else ''
            csv_writer.writerow([
                anchor, 
                finding['category'], 
                finding['subcategory'],
                finding['level'], 
                finding['description'],
                remediation
            ])


def write_to_stdout(findings):
    csv_writer = csv.writer(sys.stdout, quoting=csv.QUOTE_ALL, dialect='excel')
    csv_writer.writerow(['Id', 'Category', 'Subcategory', 'Rating', 'Description', 'Remediation'])

    for anchor, finding in findings.items():
        remediation = finding['remediation']['description'] if finding.get('remediation') else ''
        csv_writer.writerow([
            anchor, 
            finding['category'], 
            finding['subcategory'],
            finding['level'], 
            finding['description'],
            remediation
        ])
