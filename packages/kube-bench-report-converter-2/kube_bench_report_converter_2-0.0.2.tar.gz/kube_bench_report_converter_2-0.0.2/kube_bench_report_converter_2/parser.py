import re
import sys

FINDING = '['
REMEDIATION_SECTION = '== Remediations'
SUMMARY_SECTION = '== Summary'
NEW_SECTION_PATTERN = re.compile('\\[INFO]\\s([0-9]+)\\s(.*)')
STATUS_PATTERN = re.compile('\\[([a-zA-Z]+)]\\s([0-9.]+)\\s(.*)')
ANCHOR_PATTERN = re.compile('[0-9]*\\.*([0-9]*)\\.*([0-9]*)')
REMEDIATION_PATTERN = re.compile('([0-9]+\\.[0-9]+\\.[0-9]+)\\s(.*)')


def parse_finding_details(value):
    match = STATUS_PATTERN.match(value)
    level = match.group(1)
    anchor = match.group(2)
    description = match.group(3)
    section = ANCHOR_PATTERN.match(anchor)
    subcategory = section.group(1) if len(section.groups()) > 0 else None
    finding = section.group(2) if len(section.groups()) > 1 else None

    return {
        'level': level,
        'anchor': anchor,
        'description': description,
        'is_category': not finding and not subcategory,
        'is_subcategory': subcategory and not finding
    }


def parse_remediation(value):
    match = REMEDIATION_PATTERN.match(value)
    anchor = match.group(1)
    description = match.group(2).rstrip()

    return {
        'anchor': anchor,
        'description': description
    }


def is_remediation_start(value):
    return REMEDIATION_PATTERN.match(value)


def is_summary_section(value):
    return value.startswith(SUMMARY_SECTION)


def is_remediation_section(value):
    return value.startswith(REMEDIATION_SECTION)


def is_finding(value):
    return value.startswith(FINDING)


def is_new_section(value):
    return NEW_SECTION_PATTERN.match(value)


def parse_line(line, context, findings, include_warnings=False):
    # If we hit a summary section, reset the remediation context but continue parsing
    if is_summary_section(line):
        context['remediation_section'] = False
        context['remediation_details'] = {}
        return True
    
    # If we find a new section, reset the context and continue
    if is_new_section(line):
        match = NEW_SECTION_PATTERN.match(line)
        context['category'] = match.group(2)
        context['subcategory'] = ''
        context['remediation_section'] = False
        context['remediation_details'] = {}
        return True

    if not context['remediation_section']:
        context['remediation_section'] = is_remediation_section(line)

    if context['remediation_section']:
        if is_remediation_start(line):
            context['remediation_details'] = parse_remediation(line)
            anchor = context['remediation_details']['anchor']
            if anchor in findings:
                findings[anchor]['remediation'] = context['remediation_details']
        elif line and context['remediation_details']:
            context['remediation_details']['description'] += ' ' + line.rstrip()

    if is_finding(line):
        try:
            finding_details = parse_finding_details(line)
            
            if finding_details['is_category']:
                context['category'] = finding_details['description']
            elif finding_details['is_subcategory']:
                context['subcategory'] = finding_details['description']
            else:
                # Skip WARN findings unless include_warnings is True
                if finding_details['level'] == 'WARN' and not include_warnings:
                    return True
                
                # Skip INFO findings
                if finding_details['level'] == 'INFO':
                    return True
                
                finding_details['category'] = context['category']
                finding_details['subcategory'] = context['subcategory']
                findings[finding_details['anchor']] = finding_details
        except Exception as e:
            # In case of parsing error, continue to next line
            print(f"Error parsing line: {line.strip()} - {str(e)}")

    return True


def parse_from_stdin(include_warnings=False):
    findings = {}
    context = {
        'remediation_section': False,
        'remediation_details': {},
        'category': '',
        'subcategory': ''
    }

    for line in sys.stdin:
        if not parse_line(line, context, findings, include_warnings):
            break

    return findings


def parse_from_file(input_file_path, include_warnings=False):
    findings = {}
    context = {
        'remediation_section': False,
        'remediation_details': {},
        'category': '',
        'subcategory': ''
    }

    with open(input_file_path) as input_file:
        for line in input_file:
            parse_line(line, context, findings, include_warnings)

    return findings
