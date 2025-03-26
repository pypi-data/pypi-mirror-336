![Test](https://github.com/pjaudiomv/kube-bench-report-converter/actions/workflows/test.yml/badge.svg)
![Build](https://github.com/pjaudiomv/kube-bench-report-converter/actions/workflows/release.yml/badge.svg)

# kube-bench-report-converter-2

Converts [kube-bench](https://github.com/aquasecurity/kube-bench) execution console output to a CSV report.

## Install

### PyPI

    pip3 install -U kube-bench-report-converter-2

### Source

    git clone git@github.com:pjaudiomv/kube-bench-report-converter-2.git
    cd kube-bench-report-converter-2/
    pip3 install .

## Use


    cat kube-bench.log | kube-bench-report-converter-2 > kube-bench-report.csv
    
or
    
    kube-bench-report-converter-2 --input_file_path 'kube-bench.log' --output_file_path 'kube-bench-report.csv'

To include WARNING level findings in the report:

    kube-bench-report-converter-2 --input_file_path 'kube-bench.log' --output_file_path 'kube-bench-report.csv' --include_warnings

## Arguments

| Name | Description | Default |
|---|---|---|
| input_file_path  | kube-bench execution console output. | Read from stdin. |
| output_file_path  | kube-bench CSV report file path. | Write to stdout. |
| include_warnings  | Include WARNING level findings in the report. | False |

## Running Tests

To run tests, you'll need to install the test dependencies:

    pip3 install pytest pytest-cov

Then run the tests with pytest:

    python3 -m pytest -v

For coverage reporting:

    python3 -m pytest -v --cov=kube_bench_report_converter_2 --cov-report=term --cov-report=html

## Example

### Input

    [INFO] 3 Worker Node Security Configuration
    [INFO] 3.1 Worker Node Configuration Files
    [PASS] 3.1.1 Ensure that the kubeconfig file permissions are set to 644 or more restrictive (Manual)
    [PASS] 3.1.2 Ensure that the kubelet kubeconfig file ownership is set to root:root (Manual)
    [PASS] 3.1.3 Ensure that the kubelet configuration file has permissions set to 644 or more restrictive (Manual)
    [PASS] 3.1.4 Ensure that the kubelet configuration file ownership is set to root:root (Manual)
    [INFO] 3.2 Kubelet
    [PASS] 3.2.1 Ensure that the --anonymous-auth argument is set to false (Automated)
    [PASS] 3.2.2 Ensure that the --authorization-mode argument is not set to AlwaysAllow (Automated)
    [PASS] 3.2.3 Ensure that the --client-ca-file argument is set as appropriate (Manual)
    [PASS] 3.2.4 Ensure that the --read-only-port argument is set to 0 (Manual)
    [PASS] 3.2.5 Ensure that the --streaming-connection-idle-timeout argument is not set to 0 (Manual)
    [PASS] 3.2.6 Ensure that the --protect-kernel-defaults argument is set to true (Automated)
    [PASS] 3.2.7 Ensure that the --make-iptables-util-chains argument is set to true (Automated)
    [PASS] 3.2.8 Ensure that the --hostname-override argument is not set (Manual)
    [PASS] 3.2.9 Ensure that the --eventRecordQPS argument is set to 0 or a level which ensures appropriate event capture (Automated)
    [PASS] 3.2.10 Ensure that the --rotate-certificates argument is not set to false (Manual)
    [PASS] 3.2.11 Ensure that the RotateKubeletServerCertificate argument is set to true (Manual)
    [INFO] 3.3 Container Optimized OS
    [WARN] 3.3.1 Prefer using Container-Optimized OS when possible (Manual)
     
    == Remediations node ==
    3.3.1 audit test did not run: No tests defined
     
    == Summary node ==
    15 checks PASS
    0 checks FAIL
    1 checks WARN
    0 checks INFO
     
    == Summary total ==
    15 checks PASS
    0 checks FAIL
    1 checks WARN
    0 checks INFO

### Output (without warnings)

    Id,Category,Subcategory,Rating,Description,Remediation
    "3.1.1","Worker Node Security Configuration","Worker Node Configuration Files","PASS","Ensure that the kubeconfig file permissions are set to 644 or more restrictive (Manual)",""
    "3.1.2","Worker Node Security Configuration","Worker Node Configuration Files","PASS","Ensure that the kubelet kubeconfig file ownership is set to root:root (Manual)",""
    "3.1.3","Worker Node Security Configuration","Worker Node Configuration Files","PASS","Ensure that the kubelet configuration file has permissions set to 644 or more restrictive (Manual)",""
    "3.1.4","Worker Node Security Configuration","Worker Node Configuration Files","PASS","Ensure that the kubelet configuration file ownership is set to root:root (Manual)",""
    "3.2.1","Worker Node Security Configuration","Kubelet","PASS","Ensure that the --anonymous-auth argument is set to false (Automated)",""
    "3.2.2","Worker Node Security Configuration","Kubelet","PASS","Ensure that the --authorization-mode argument is not set to AlwaysAllow (Automated)",""
    "3.2.3","Worker Node Security Configuration","Kubelet","PASS","Ensure that the --client-ca-file argument is set as appropriate (Manual)",""
    "3.2.4","Worker Node Security Configuration","Kubelet","PASS","Ensure that the --read-only-port argument is set to 0 (Manual)",""
    "3.2.5","Worker Node Security Configuration","Kubelet","PASS","Ensure that the --streaming-connection-idle-timeout argument is not set to 0 (Manual)",""
    "3.2.6","Worker Node Security Configuration","Kubelet","PASS","Ensure that the --protect-kernel-defaults argument is set to true (Automated)",""
    "3.2.7","Worker Node Security Configuration","Kubelet","PASS","Ensure that the --make-iptables-util-chains argument is set to true (Automated)",""
    "3.2.8","Worker Node Security Configuration","Kubelet","PASS","Ensure that the --hostname-override argument is not set (Manual)",""
    "3.2.9","Worker Node Security Configuration","Kubelet","PASS","Ensure that the --eventRecordQPS argument is set to 0 or a level which ensures appropriate event capture (Automated)",""
    "3.2.10","Worker Node Security Configuration","Kubelet","PASS","Ensure that the --rotate-certificates argument is not set to false (Manual)",""
    "3.2.11","Worker Node Security Configuration","Kubelet","PASS","Ensure that the RotateKubeletServerCertificate argument is set to true (Manual)",""

### Output (with warnings)

    Id,Category,Subcategory,Rating,Description,Remediation
    "3.1.1","Worker Node Security Configuration","Worker Node Configuration Files","PASS","Ensure that the kubeconfig file permissions are set to 644 or more restrictive (Manual)",""
    "3.1.2","Worker Node Security Configuration","Worker Node Configuration Files","PASS","Ensure that the kubelet kubeconfig file ownership is set to root:root (Manual)",""
    "3.1.3","Worker Node Security Configuration","Worker Node Configuration Files","PASS","Ensure that the kubelet configuration file has permissions set to 644 or more restrictive (Manual)",""
    "3.1.4","Worker Node Security Configuration","Worker Node Configuration Files","PASS","Ensure that the kubelet configuration file ownership is set to root:root (Manual)",""
    "3.2.1","Worker Node Security Configuration","Kubelet","PASS","Ensure that the --anonymous-auth argument is set to false (Automated)",""
    "3.2.2","Worker Node Security Configuration","Kubelet","PASS","Ensure that the --authorization-mode argument is not set to AlwaysAllow (Automated)",""
    "3.2.3","Worker Node Security Configuration","Kubelet","PASS","Ensure that the --client-ca-file argument is set as appropriate (Manual)",""
    "3.2.4","Worker Node Security Configuration","Kubelet","PASS","Ensure that the --read-only-port argument is set to 0 (Manual)",""
    "3.2.5","Worker Node Security Configuration","Kubelet","PASS","Ensure that the --streaming-connection-idle-timeout argument is not set to 0 (Manual)",""
    "3.2.6","Worker Node Security Configuration","Kubelet","PASS","Ensure that the --protect-kernel-defaults argument is set to true (Automated)",""
    "3.2.7","Worker Node Security Configuration","Kubelet","PASS","Ensure that the --make-iptables-util-chains argument is set to true (Automated)",""
    "3.2.8","Worker Node Security Configuration","Kubelet","PASS","Ensure that the --hostname-override argument is not set (Manual)",""
    "3.2.9","Worker Node Security Configuration","Kubelet","PASS","Ensure that the --eventRecordQPS argument is set to 0 or a level which ensures appropriate event capture (Automated)",""
    "3.2.10","Worker Node Security Configuration","Kubelet","PASS","Ensure that the --rotate-certificates argument is not set to false (Manual)",""
    "3.2.11","Worker Node Security Configuration","Kubelet","PASS","Ensure that the RotateKubeletServerCertificate argument is set to true (Manual)",""
    "3.3.1","Worker Node Security Configuration","Container Optimized OS","WARN","Prefer using Container-Optimized OS when possible (Manual)","audit test did not run: No tests defined"


## Attribution

This project is based on or originally forked from [kube-bench-report-converter](https://github.com/build-failure/kube-bench-report-converter/) by Michael Lewkowski.

Many thanks to the original author for the foundation of this work.
