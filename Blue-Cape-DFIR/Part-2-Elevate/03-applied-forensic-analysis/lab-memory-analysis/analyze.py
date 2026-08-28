import subprocess
import sys
import os

def extract_raw_strings(mem_file, output_txt):
    """
    Extracts raw strings from memory using the Linux utility.
    Required before running windows.strings.
    """
    print(f"[*] Extracting raw strings from {mem_file}...")
    try:
        with open(output_txt, "w") as f:
            subprocess.run(["strings", mem_file], check=True, stdout=f)
        print(f"[+] Raw strings saved to {output_txt}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("[!] Error: 'strings' utility failed. Is it installed?")
        return False

def run_volatility_plugin(plugin_name, cmd_args, output_file):
    """
    Runs any volatility plugin with dynamic arguments and saves output as CSV.
    """
    # Dynamic argument assembly: 'cmd_args' handles unique plugin flags
    cmd = ["vol", "-r", "csv"] + cmd_args + [plugin_name]

    print(f"[*] Running: {plugin_name}...")
    try:
        with open(output_file, "w") as f:
            result = subprocess.run(cmd, check=True, stdout=f, stderr=subprocess.PIPE)
        print(f"[+] Success: Output saved to {output_file}")
        return True
    except FileNotFoundError:
        print(f"[!] Error: Command not found. Is 'vol' in your PATH?")
        return False
    except subprocess.CalledProcessError as e:
        print(f"[!] Error running {plugin_name}: {e}")
        if e.stderr:
            print(f"    stderr: {e.stderr.decode()[:500]}")
        return False

def main():
    MEMORY_FILE = "memdump.mem"
    OUTPUT_DIR = "output/"
    RAW_STRINGS_TXT = os.path.join(OUTPUT_DIR, "raw_strings.txt")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    # 1. Define standard plugins that only need [-f MEMORY_FILE]
    standard_plugins = [
        ("windows.pslist", "pslist"),
        ("windows.pstree", "pstree"),
        ("windows.cmdline", "cmdline"),
        ("windows.filescan", "filescan"),
        ("windows.netscan", "netscan"),
        ("timeliner.Timeliner", "timeline")  
    ]
    
    print(f"--- Starting Bulk Analysis for: {MEMORY_FILE} ---\n")
    
    # Run the standard plugins
    for plugin, short_name in standard_plugins:
        out_file = os.path.join(OUTPUT_DIR, f"{plugin}.csv")
        base_args = ["-f", MEMORY_FILE]
        run_volatility_plugin(plugin, base_args, out_file)
    
    print("\n--- Starting Special Plugins ---")
    
    # 2. Handle the strings extraction and run windows.strings
    if extract_raw_strings(MEMORY_FILE, RAW_STRINGS_TXT):
        strings_out = os.path.join(OUTPUT_DIR, "windows.strings.csv")
        # Here we pass the dynamic, expanded arguments required by this specific plugin
        strings_args = ["-f", MEMORY_FILE, "--strings-file", RAW_STRINGS_TXT]
        run_volatility_plugin("windows.strings", strings_args, strings_out)
    
    print(f"\n--- Analysis Complete. Check '{OUTPUT_DIR}' folder. ---")

if __name__ == "__main__":
    try:
        import volatility3
    except ImportError:
        print("Error: volatility3 is not installed.")
        print("Please run: pip install volatility3")
        sys.exit(1)
        
    main()