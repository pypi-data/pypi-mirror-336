import argparse
import os

from kube_bench_report_converter_2 import parser as report_parser
from kube_bench_report_converter_2 import writer as report_writer


def main():
    parser = argparse.ArgumentParser(description='Converts kube-bench checks console output to CSV format.')
    parser.add_argument('--output_file_path', default=None, help='kube-bench CSV report file path.')
    parser.add_argument('--input_file_path', default=None, help='kube-bench execution console output.')
    parser.add_argument('--include_warnings', action='store_true', help='Include WARNING level findings in the output.')

    args = parser.parse_args()

    if args.input_file_path:
        findings = report_parser.parse_from_file(args.input_file_path, include_warnings=args.include_warnings)
    else:
        findings = report_parser.parse_from_stdin(include_warnings=args.include_warnings)

    if args.output_file_path:
        print(f"Writing to {args.output_file_path}")
        report_writer.write_to_file(findings, args.output_file_path)
        if os.path.exists(args.output_file_path):
            print(f"File created successfully, size: {os.path.getsize(args.output_file_path)} bytes")
        else:
            print(f"Failed to create the file {args.output_file_path}")
    else:
        report_writer.write_to_stdout(findings)
