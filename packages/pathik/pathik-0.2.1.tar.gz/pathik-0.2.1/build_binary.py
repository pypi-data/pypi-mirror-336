#!/usr/bin/env python
"""
Script to build the Go binary for pathik
"""
import os
import subprocess
import sys
import platform
import argparse

def build_binary(target_os=None, target_arch=None):
    """Build the Go binary for the specified platform"""
    # Determine target platform
    if target_os is None:
        target_os = platform.system().lower()
        if target_os == "darwin":
            target_os = "darwin"
        elif target_os.startswith("win"):
            target_os = "windows"
        elif target_os.startswith("linux"):
            target_os = "linux"
    
    if target_arch is None:
        machine = platform.machine().lower()
        if machine in ("x86_64", "amd64"):
            target_arch = "amd64"
        elif machine in ("arm64", "aarch64"):
            target_arch = "arm64"
        elif machine in ("i386", "i686", "x86"):
            target_arch = "386"
        else:
            target_arch = machine
    
    # Determine the binary name based on platform
    binary_name = "pathik_bin"
    if target_os == "windows":
        binary_name += ".exe"
    
    # Setup output path
    if target_os != platform.system().lower() or target_arch != platform.machine().lower():
        # Cross-compilation
        output_path = f"pathik/bin/{target_os}_{target_arch}/{binary_name}"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
    else:
        # Native compilation
        os.makedirs("pathik", exist_ok=True)
        output_path = f"pathik/{binary_name}"
    
    # Setup environment
    env = os.environ.copy()
    env["GOOS"] = target_os
    env["GOARCH"] = target_arch
    
    # Build the Go binary
    cmd = ["go", "build", "-o", output_path, "./main.go"]
    print(f"Building for {target_os}/{target_arch}: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, env=env)
    
    if result.returncode != 0:
        print(f"Error building Go binary: {result.stderr.decode()}")
        return False
    
    print(f"Go binary built successfully: {output_path}")
    return True

def build_all():
    """Build binaries for all supported platforms"""
    platforms = [
        ("darwin", "amd64"),  # Intel Mac
        ("darwin", "arm64"),  # Apple Silicon Mac
        ("linux", "amd64"),   # Linux x86_64
        ("linux", "arm64"),   # Linux ARM64
        ("windows", "amd64"), # Windows x86_64
    ]
    
    success = True
    for target_os, target_arch in platforms:
        if not build_binary(target_os, target_arch):
            print(f"Failed to build for {target_os}/{target_arch}")
            success = False
    
    return success

def main():
    parser = argparse.ArgumentParser(description="Build pathik binaries")
    parser.add_argument("--all", action="store_true", help="Build for all supported platforms")
    parser.add_argument("--os", help="Target OS (darwin, linux, windows)")
    parser.add_argument("--arch", help="Target architecture (amd64, arm64, 386)")
    
    args = parser.parse_args()
    
    if args.all:
        print("Building for all supported platforms...")
        if build_all():
            print("All binaries built successfully.")
            print("You can now install the Python package with:")
            print("  pip install -e .")
        else:
            print("Some binaries failed to build.")
            sys.exit(1)
    else:
        if build_binary(args.os, args.arch):
            print("Binary built successfully.")
            print("You can now install the Python package with:")
            print("  pip install -e .")
        else:
            print("Failed to build binary.")
            sys.exit(1)

if __name__ == "__main__":
    main() 