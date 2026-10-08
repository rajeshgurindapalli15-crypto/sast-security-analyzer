import click
import json
import os
from rich.console import Console
from rich.table import Table
from scanner.engine import SASTEngine
from scanner.database import save_vulnerabilities_to_db, get_scan_history

console = Console()

@click.group()
def cli():
    """Static Application Security Testing (SAST) Scanner CLI"""
    pass

@cli.command(name="scan")
@click.option('--target', '-t', required=True, help='File or directory to scan')
@click.option('--output', '-o', default='reports/scan_report.md', help='Output report file path')
def scan_command(target, output):
    """Run a security scan on a target file or directory"""
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

    # 💾 Save findings to SQLite database
    if findings:
        save_vulnerabilities_to_db(target, findings)
        console.print("[bold green]💾 Scan results successfully persisted to SQLite database (`sast_results.db`).[/bold green]")

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

@cli.command(name="history")
def history_command():
    """View historical scan results stored in the database"""
    rows = get_scan_history()
    
    if not rows:
        console.print("[yellow]⚠️ No historical scan records found in database.[/yellow]")
        return

    table = Table(title="Past SAST Scan History")
    table.add_column("Timestamp", style="dim")
    table.add_column("Target", style="yellow")
    table.add_column("Rule ID", style="cyan")
    table.add_column("Severity", style="bold red")
    table.add_column("Vulnerability", style="white")
    table.add_column("Line", style="magenta")

    for row in rows:
        timestamp, target_file, rule_id, severity, vulnerability, file_line = row
        table.add_row(timestamp, target_file, rule_id, severity, vulnerability, file_line)

    console.print(table)

if __name__ == '__main__':
    cli()