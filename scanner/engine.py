import os
import re
import json

class SASTEngine:
    def __init__(self, rules_path):
        with open(rules_path, 'r', encoding='utf-8') as f:
            self.rules = json.load(f)

    def scan_file(self, file_path):
        findings = []
        if not os.path.exists(file_path):
            return findings

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception:
            return findings

        for line_num, line_content in enumerate(lines, start=1):
            for rule in self.rules:
                if re.search(rule["pattern"], line_content):
                    findings.append({
                        "rule_id": rule["id"],
                        "name": rule["name"],
                        "severity": rule["severity"],
                        "file": file_path,
                        "line": line_num,
                        "code_snippet": line_content.strip(),
                        "description": rule["description"],
                        "remediation": rule["remediation"]
                    })
        return findings

    def scan_directory(self, target_dir):
        all_findings = []
        for root, _, files in os.walk(target_dir):
            for file in files:
                if file.endswith('.py') and not file.startswith('test_'):
                    full_path = os.path.join(root, file)
                    all_findings.extend(self.scan_file(full_path))
        return all_findings