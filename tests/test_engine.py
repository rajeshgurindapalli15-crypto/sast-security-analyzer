import os
import pytest
from scanner.engine import SASTEngine

def test_scan_vulnerabilities():
    rules_path = os.path.join('scanner', 'rules.json')
    engine = SASTEngine(rules_path)
    findings = engine.scan_file(os.path.join('tests', 'sample_vulnerable.py'))
    assert len(findings) > 0