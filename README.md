# SAST Security Analyzer

A modular, terminal-based Static Application Security Testing (SAST) tool built in Python to scan codebases for security vulnerabilities.

## Features

- **Regex Rule Engine**: Scans code for Hardcoded Secrets, Command Injection, SQL Injection, and Insecure Deserialization.
- **Terminal UI**: Styled CLI table outputs built with `click` and `rich`.
- **Automated Reporting**: Generates Markdown security reports under `reports/`.
- **Tested**: Automated test suite powered by `pytest`.
- **Containerized**: Production-ready `Dockerfile` for isolated scanning environments.

## Installation & Setup

```bash
git clone [https://github.com/rajeshgurindapalli15-crypto/sast-security-analyzer.git](https://github.com/rajeshgurindapalli15-crypto/sast-security-analyzer.git)
cd sast-security-analyzer
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
