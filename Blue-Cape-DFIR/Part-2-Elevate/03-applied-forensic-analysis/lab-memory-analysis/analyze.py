import subprocess
import sys
import os

def run_volatility_plugin(plugin_name, mem_file, output_dir):
    """
    Runs a volatility plugin and saves the output as a CSV.
    """
    cmd = ["vol",
            "-f",
            mem_file,
            "-r",
            "csv",
            plugin_name
        ]

    output_file = os.path.join(output_dir, f"{plugin_name}.csv")

    print(f"[*] Running: {plugin_name}...")
    try:
        with open(output_file, "w") as f:
            result = subprocess.run(cmd, check=True, stdout=f, stderr=subprocess.PIPE)
        print(f"[+] Success: Output saved to {output_file}")
        return True
    except FileNotFoundError:
        print(f"[!] Error: Command not found. Is 'vol' in your PATH?")
        print("    Try installing via: pip install volatility3")
        print("    Or check if 'vol' exists in your Python Scripts folder.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"[!] Error running {plugin_name}: {e}")
        if e.stderr:
            print(f"    stderr: {e.stderr.decode()[:500]}")
        return False

def main():
    MEMORY_FILE = "memdump.mem"
    OUTPUT_DIR = "output/"
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    plugins = [
        ("windows.pslist", "pslist"),
        ("windows.pstree", "pstree"),
        ("windows.cmdline", "cmdline"),
        ("windows.filescan", "filescan"),
        ("windows.netscan", "netscan"),
        ("windows.timeliner", "timeline"), # not working
        ("windows.strings", "strings") # Neither , check later 
    ]
    
    print(f"--- Starting Bulk Analysis for: {MEMORY_FILE} ---\n")
    
    for plugin, _ in plugins:
        run_volatility_plugin(plugin, MEMORY_FILE, OUTPUT_DIR)
    
    print(f"\n--- Analysis Complete. Check '{OUTPUT_DIR}' folder. ---")

if __name__ == "__main__":
    # Check if volatility3 is installed
    try:
        import volatility3
    except ImportError:
        print("Error: volatility3 is not installed.")
        print("Please run: pip install volatility3")
        sys.exit(1)
        
    main()