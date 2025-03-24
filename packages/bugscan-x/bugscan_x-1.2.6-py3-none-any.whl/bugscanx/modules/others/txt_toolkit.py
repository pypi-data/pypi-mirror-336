import os
import re
import socket
import ipaddress
from rich import print
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict
from bugscanx.utils.common import get_input, get_confirm

def read_file_lines(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines()]
    except Exception as e:
        print(f"[red] Error reading file {file_path}: {e}[/red]")
        return []

def write_file_lines(file_path, lines):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(f"{line}\n" for line in lines)
        return True
    except Exception as e:
        print(f"[red] Error writing to file {file_path}: {e}[/red]")
        return False

def get_file_input():
    return get_input("File path", "file")

def split_txt_file():
    file_path = get_file_input()
    parts = int(get_input("Number of parts", "number"))
    lines = read_file_lines(file_path)
    
    if not lines:
        return
    
    lines_per_file = len(lines) // parts
    file_base = os.path.splitext(file_path)[0]
    
    created_files = []
    
    for i in range(parts):
        start_idx = i * lines_per_file
        end_idx = None if i == parts - 1 else (i + 1) * lines_per_file
        part_lines = lines[start_idx:end_idx]
        part_file = f"{file_base}_part_{i + 1}.txt"
        
        if write_file_lines(part_file, part_lines):
            created_files.append((part_file, len(part_lines)))
    
    print(f"[green] Successfully split '{os.path.basename(file_path)}' ({len(lines)} lines) into {len(created_files)} parts:[/green]")
    for file_path, line_count in created_files:
        print(f"[green] - {os.path.basename(file_path)}: {line_count} lines[/green]")

def merge_txt_files():
    directory = get_input("Directory path", default=os.getcwd())
    
    if get_confirm(" Merge all txt files?"):
        files_to_merge = [f for f in os.listdir(directory) if f.endswith('.txt')]
    else:
        filenames = get_input("Files to merge (comma-separated)")
        files_to_merge = [f.strip() for f in filenames.split(',') if f.strip()]
    
    if not files_to_merge:
        print("[red] No files found to merge[/red]")
        return
    
    output_file = get_input("Output filename")
    output_path = os.path.join(directory, output_file)
    total_lines = 0
    
    try:
        with open(output_path, 'w', encoding="utf-8") as outfile:
            for filename in files_to_merge:
                file_path = os.path.join(directory, filename)
                lines = read_file_lines(file_path)
                outfile.write('\n'.join(lines) + "\n")
                total_lines += len(lines)
        print(f"[green] Successfully merged {len(files_to_merge)} files into '{output_file}'[/green]")
        print(f"[green] - Total lines: {total_lines}[/green]")
        print(f"[green] - Output location: {directory}[/green]")
    except Exception as e:
        print(f"[red] Error merging files: {e}[/red]")

def remove_duplicate_domains():
    file_path = get_file_input()
    lines = read_file_lines(file_path)
    
    if not lines:
        return
    
    unique_lines = sorted(set(lines))
    duplicates_removed = len(lines) - len(unique_lines)
    
    if write_file_lines(file_path, unique_lines):
        print(f"[green] Successfully removed duplicates from '{os.path.basename(file_path)}':[/green]")
        print(f"[green] - Original count: {len(lines)} lines[/green]")
        print(f"[green] - Unique count: {len(unique_lines)} lines[/green]")
        print(f"[green] - Duplicates removed: {duplicates_removed} lines[/green]")

def txt_cleaner():
    input_file = get_file_input()
    domain_output_file = get_input("Domain output file")
    ip_output_file = get_input("IP output file")
    
    content = read_file_lines(input_file)
    if not content:
        return
    
    domain_pattern = re.compile(r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}\b')
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    
    domains = set()
    ips = set()
    
    for line in content:
        domains.update(domain_pattern.findall(line))
        ips.update(ip_pattern.findall(line))
    
    domains_success = write_file_lines(domain_output_file, sorted(domains))
    ips_success = write_file_lines(ip_output_file, sorted(ips))
    
    if domains_success or ips_success:
        print(f"[green] TXT Cleaner results for '{os.path.basename(input_file)}':[/green]")
        if domains_success:
            print(f"[green] - Extracted {len(domains)} unique domains to '{os.path.basename(domain_output_file)}'[/green]")
        if ips_success:
            print(f"[green] - Extracted {len(ips)} unique IP addresses to '{os.path.basename(ip_output_file)}'[/green]")

def convert_subdomains_to_domains():
    file_path = get_file_input()
    output_file = get_input("Output file")
    
    subdomains = read_file_lines(file_path)
    if not subdomains:
        return

    root_domains = set()
    for subdomain in subdomains:
        parts = subdomain.split('.')
        if len(parts) >= 2:
            root_domains.add('.'.join(parts[-2:]))
    
    if write_file_lines(output_file, sorted(root_domains)):
        print(f"[green] Successfully converted subdomains to root domains:[/green]")
        print(f"[green] - Input subdomains: {len(subdomains)}[/green]")
        print(f"[green] - Unique root domains: {len(root_domains)}[/green]")
        print(f"[green] - Output file: '{os.path.basename(output_file)}'[/green]")

def separate_domains_by_extension():
    file_path = get_file_input()
    extensions_input = get_input("Extensions (comma-separated) or 'all'")
    
    domains = read_file_lines(file_path)
    if not domains:
        return
    
    extensions_dict = defaultdict(list)
    for domain in domains:
        ext = domain.split('.')[-1].lower()
        extensions_dict[ext].append(domain)
    
    base_name = os.path.splitext(file_path)[0]
    target_extensions = [ext.strip() for ext in extensions_input.lower().split(',')] if extensions_input.lower() != 'all' else list(extensions_dict.keys())
    
    success_count = 0
    print(f"[green] Separating domains by extension from '{os.path.basename(file_path)}':[/green]")
    
    for ext in target_extensions:
        if ext in extensions_dict:
            ext_file = f"{base_name}_{ext}.txt"
            if write_file_lines(ext_file, sorted(extensions_dict[ext])):
                success_count += 1
                print(f"[green] - Created '{os.path.basename(ext_file)}' with {len(extensions_dict[ext])} domains[/green]")
        else:
            print(f"[yellow] - No domains found with .{ext} extension[/yellow]")
    
    if success_count > 0:
        print(f"[green] Successfully created {success_count} files based on domain extensions[/green]")

def filter_by_keywords():
    file_path = get_file_input()
    keywords = [k.strip().lower() for k in get_input("Keywords (comma-separated)").split(',')]
    output_file = get_input("Output file")
    
    lines = read_file_lines(file_path)
    if not lines:
        return
    
    filtered_domains = [domain for domain in lines if any(keyword in domain.lower() for keyword in keywords)]
    
    if write_file_lines(output_file, filtered_domains):
        print(f"[green] Successfully filtered domains by keywords:[/green]")
        print(f"[green] - Input domains: {len(lines)}[/green]")
        print(f"[green] - Matched domains: {len(filtered_domains)}[/green]")
        print(f"[green] - Keywords used: {', '.join(keywords)}[/green]")
        print(f"[green] - Output file: '{os.path.basename(output_file)}'[/green]")

def cidr_to_ip():
    cidr_input = get_input("CIDR range")
    output_file = get_input("Output file")
    
    try:
        network = ipaddress.ip_network(cidr_input.strip(), strict=False)
        ip_addresses = [str(ip) for ip in network.hosts()]
        
        if write_file_lines(output_file, ip_addresses):
            print(f"[green] Successfully converted CIDR to IP addresses:[/green]")
            print(f"[green] - CIDR range: {cidr_input}[/green]")
            print(f"[green] - Total IPs: {len(ip_addresses)}[/green]")
            print(f"[green] - Output file: '{os.path.basename(output_file)}'[/green]")
    except ValueError as e:
        print(f"[red] Invalid CIDR range: {cidr_input} - {str(e)}[/red]")

def resolve_domain(domain):
    try:
        ip = socket.gethostbyname_ex(domain.strip())[2][0]
        return domain, ip
    except (socket.gaierror, socket.timeout):
        return domain, None

def domains_to_ip():
    file_path = get_file_input()
    output_file = get_input("Output file")
    
    domains = read_file_lines(file_path)
    if not domains:
        return
        
    ip_addresses = set()
    total_domains = len(domains)
    resolved_count = 0
    failed_count = 0

    socket.setdefaulttimeout(1)
    
    with Progress(
        SpinnerColumn(),
        *Progress.get_default_columns(),
        TimeElapsedColumn(),
        transient=True
    ) as progress:
        task = progress.add_task("[yellow]Resolving", total=total_domains)
        
        with ThreadPoolExecutor(max_workers=100) as executor:
            future_to_domain = {executor.submit(resolve_domain, domain): domain for domain in domains}
            for future in as_completed(future_to_domain):
                domain, ip = future.result()
                if ip:
                    ip_addresses.add(ip)
                    resolved_count += 1
                else:
                    failed_count += 1
                progress.update(task, advance=1)
    
    if ip_addresses and write_file_lines(output_file, sorted(ip_addresses)):
        print(f"[green] Successfully resolved domains to IP addresses:[/green]")
        print(f"[green] - Input domains: {total_domains}[/green]")
        print(f"[green] - Successfully resolved: {resolved_count}[/green]")
        print(f"[green] - Failed to resolve: {failed_count}[/green]")
        print(f"[green] - Unique IP addresses: {len(ip_addresses)}[/green]")
        print(f"[green] - Output file: '{os.path.basename(output_file)}'[/green]")
    else:
        print("[red] No domains could be resolved or there was an error writing to the output file[/red]")

def main():
    options = {
        "1": ("Split File", split_txt_file, "bold cyan"),
        "2": ("Merge Files", merge_txt_files, "bold blue"),
        "3": ("Remove Duplicate", remove_duplicate_domains, "bold yellow"),
        "4": ("Subdomains to Domains", convert_subdomains_to_domains, "bold magenta"),
        "5": ("Domains and IP Extractor", txt_cleaner, "bold cyan"),
        "6": ("Filter by Extension", separate_domains_by_extension, "bold magenta"),
        "7": ("Filter by Keywords", filter_by_keywords, "bold yellow"),
        "8": ("CIDR to IP", cidr_to_ip, "bold green"),
        "9": ("Domains to IP", domains_to_ip, "bold blue"),
        "0": ("Back", lambda: None, "bold red")
    }
    
    print("\n".join(f"[{color}] [{key}] {desc}" for key, (desc, _, color) in options.items()))
    choice = input("\n \033[36m[-]  Your Choice: \033[0m")
    
    if choice in options:
        options[choice][1]()
        if choice == '0':
            return
