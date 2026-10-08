# SAST Security Analyzer

A modular, enterprise-grade Static Application Security Testing (SAST) utility engineered in Python to evaluate source codebases for security vulnerabilities, enforce secure coding standards, and automate compliance reporting.

## Features

- **Advanced Regex Rule Engine**: Extensible detection engine configured to identify critical security risks, including Hardcoded Secrets, Command Injection vectors, SQL Injection vulnerabilities, and Insecure Deserialization.
- **Rich Terminal User Interface (TUI)**: Delivers structured, color-coded CLI outputs and diagnostic tables leveraging `click` and `rich`.
- **Automated Security Reporting**: Generates comprehensive Markdown-formatted compliance audits automatically exported to the `reports/` directory.
- **Robust Verification Suite**: Fully tested using an automated test framework powered by `pytest`.
- **Containerized Deployment**: Includes a production-ready `Dockerfile` ensuring isolated, reproducible analysis environments.

## Installation & Setup

To clone and configure the environment locally, execute the following commands in your terminal:

```bash
git clone [https://github.com/rajeshgurindapalli15-crypto/sast-security-analyzer.git](https://github.com/rajeshgurindapalli15-crypto/sast-security-analyzer.git)
cd sast-security-analyzer
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt



