import click
import json
import os
from rich.console import Console
from rich.table import Table
from scanner.engine import SASTEngine

console = Console()

@click.command()
@click.option('--target', '-t', required=True, help='File or directory to scan')
@click.option('--output', '-o', default='reports/scan_report.md', help='Output report file path')
def main(target, output):
    """Static Application Security Testing (SAST) Scanner CLI"""
    rules_path = os.path.join(os.path.dirname(__file__), 'rules.json')
    engine = SASTEngine(rules_path)

    console.print(f"\n[bold blue]🔍 Starting SAST Scan on:[/bold blue] [yellow]{target}[/yellow]\n")

    if os.path.isfile(target):
        findings = engine.scan_file(target)
    else:
        findings = engine.scan_directory(target)

    if not findings:
        console.print("[bold green]✅ No vulnerabilities detected![/bold green]\n")
        return

    table = Table(title="SAST Vulnerability Scan Results")
    table.add_column("Rule ID", style="cyan")
    table.add_column("Severity", style="bold red")
    table.add_column("Vulnerability", style="white")
    table.add_column("File:Line", style="yellow")

    for f in findings:
        table.add_row(f["rule_id"], f["severity"], f["name"], f"{f['file']}:{f['line']}")

    console.print(table)

    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, 'w', encoding='utf-8') as rep:
        rep.write("# 🛡️ SAST Security Scan Report\n\n")
        rep.write(f"**Target Analyzed:** `{target}`  \n")
        rep.write(f"**Total Vulnerabilities Found:** `{len(findings)}`  \n\n")
        rep.write("| Rule ID | Severity | Vulnerability | File & Line | Code Snippet |\n")
        rep.write("| :--- | :--- | :--- | :--- | :--- |\n")
        for f in findings:
            rep.write(f"| {f['rule_id']} | **{f['severity']}** | {f['name']} | `{f['file']}:{f['line']}` | `{f['code_snippet']}` |\n")

    console.print(f"\n[bold green]📄 Report generated successfully at:[/bold green] [underline]{output}[/underline]\n")

if __name__ == '__main__':
    main()