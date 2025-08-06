#!/usr/bin/env python3
"""
HUVTSP System Verification Script
Verifies that all Final App components are properly integrated and functional
"""

import os
import json
import pandas as pd
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"🔍 {title}")
    print("=" * 60)

def check_file_exists(file_path, description):
    """Check if a file exists and print status"""
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        print(f"✅ {description}: {file_path} ({size:,} bytes)")
        return True
    else:
        print(f"❌ {description}: {file_path} - NOT FOUND")
        return False

def check_directory_exists(dir_path, description):
    """Check if a directory exists and print status"""
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        count = len(os.listdir(dir_path))
        print(f"✅ {description}: {dir_path} ({count} items)")
        return True
    else:
        print(f"❌ {description}: {dir_path} - NOT FOUND")
        return False

def verify_data_files():
    """Verify all required data files are present"""
    print_header("DATA FILES VERIFICATION")
    
    files_to_check = [
        ("weekly_summary.txt", "AI Summary Text"),
        ("predictions.csv", "ML Model Predictions"),
        ("alerts_today.csv", "Daily Alert Export"),
        ("anomaly_plot.png", "Anomaly Visualization"),
        ("ai_module.py", "Anomaly Detection Module"),
        ("alerts_20250807_summary.json", "Alert Export Metadata")
    ]
    
    all_present = True
    for file_path, description in files_to_check:
        if not check_file_exists(file_path, description):
            all_present = False
    
    return all_present

def verify_application_files():
    """Verify all application files are present"""
    print_header("APPLICATION FILES VERIFICATION")
    
    files_to_check = [
        ("app.py", "Flask Backend API"),
        ("run_system.py", "Unified System Launcher"),
        ("package.json", "Frontend Dependencies"),
        ("index.html", "HTML Entry Point"),
        ("README.md", "Documentation")
    ]
    
    all_present = True
    for file_path, description in files_to_check:
        if not check_file_exists(file_path, description):
            all_present = False
    
    return all_present

def verify_directories():
    """Verify all required directories are present"""
    print_header("DIRECTORY STRUCTURE VERIFICATION")
    
    directories_to_check = [
        ("src", "React Source Code"),
        ("src/components", "React Components"),
        ("public", "Static Assets"),
        ("node_modules", "Node.js Dependencies (if installed)")
    ]
    
    all_present = True
    for dir_path, description in directories_to_check:
        if dir_path == "node_modules":
            # Node modules is optional for verification
            check_directory_exists(dir_path, description)
        else:
            if not check_directory_exists(dir_path, description):
                all_present = False
    
    return all_present

def verify_data_integrity():
    """Verify that data files can be loaded and contain expected data"""
    print_header("DATA INTEGRITY VERIFICATION")
    
    try:
        # Check predictions.csv
        if os.path.exists("predictions.csv"):
            df = pd.read_csv("predictions.csv")
            print(f"✅ predictions.csv: {len(df)} records, columns: {list(df.columns)}")
        else:
            print("❌ predictions.csv: File not found")
        
        # Check alerts_today.csv
        if os.path.exists("alerts_today.csv"):
            df = pd.read_csv("alerts_today.csv")
            print(f"✅ alerts_today.csv: {len(df)} alerts, columns: {list(df.columns)}")
        else:
            print("❌ alerts_today.csv: File not found")
        
        # Check weekly_summary.txt
        if os.path.exists("weekly_summary.txt"):
            with open("weekly_summary.txt", "r") as f:
                content = f.read().strip()
                print(f"✅ weekly_summary.txt: {len(content)} characters")
        else:
            print("❌ weekly_summary.txt: File not found")
        
        # Check alert summary JSON
        if os.path.exists("alerts_20250807_summary.json"):
            with open("alerts_20250807_summary.json", "r") as f:
                data = json.load(f)
                print(f"✅ Alert summary JSON: {len(data)} fields, status: {data.get('status', 'Unknown')}")
        else:
            print("❌ Alert summary JSON: File not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Data integrity check failed: {e}")
        return False

def verify_no_duplicates():
    """Verify that there are no duplicate Final App folders"""
    print_header("DUPLICATE FOLDER VERIFICATION")
    
    # Check parent directory for duplicate Final App folders
    parent_dir = Path("..").resolve()
    final_app_dirs = []
    
    # Look for any "Final App" directories
    for item in parent_dir.rglob("*"):
        if item.is_dir() and "Final App" in item.name:
            final_app_dirs.append(str(item.relative_to(parent_dir)))
    
    if len(final_app_dirs) == 1:
        print(f"✅ Single Final App directory found: {final_app_dirs[0]}")
        return True
    elif len(final_app_dirs) > 1:
        print(f"⚠️  Multiple Final App directories found:")
        for dir_path in final_app_dirs:
            print(f"   - {dir_path}")
        print("🔧 Recommendation: Remove duplicate directories")
        return False
    else:
        print("❌ No Final App directory found")
        return False

def generate_system_report():
    """Generate a comprehensive system report"""
    print_header("SYSTEM INTEGRATION REPORT")
    
    current_dir = os.getcwd()
    print(f"📁 Current Directory: {current_dir}")
    print(f"📂 Directory Name: {os.path.basename(current_dir)}")
    
    # Count files and directories
    all_files = []
    all_dirs = []
    
    for root, dirs, files in os.walk("."):
        if "node_modules" not in root and ".git" not in root:
            all_dirs.extend([os.path.join(root, d) for d in dirs])
            all_files.extend([os.path.join(root, f) for f in files])
    
    print(f"📊 Total Files: {len(all_files)}")
    print(f"📊 Total Directories: {len(all_dirs)}")
    
    # Key components
    key_components = {
        "Frontend": ["src/", "public/", "package.json"],
        "Backend": ["app.py", "ai_module.py"],
        "Data": ["predictions.csv", "alerts_today.csv", "weekly_summary.txt"],
        "System": ["run_system.py", "README.md"]
    }
    
    print("\n🧩 Component Status:")
    for category, files in key_components.items():
        present = sum(1 for f in files if os.path.exists(f))
        total = len(files)
        status = "✅" if present == total else "⚠️" if present > 0 else "❌"
        print(f"   {status} {category}: {present}/{total} components present")

def main():
    """Main verification function"""
    print("🔍 HUVTSP Final App System Verification")
    print("=" * 60)
    print("Verifying that all components are properly consolidated...")
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Run all verification checks
    checks = [
        ("Data Files", verify_data_files),
        ("Application Files", verify_application_files),
        ("Directory Structure", verify_directories),
        ("Data Integrity", verify_data_integrity),
        ("No Duplicates", verify_no_duplicates)
    ]
    
    results = []
    for check_name, check_function in checks:
        try:
            result = check_function()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} check failed: {e}")
            results.append((check_name, False))
    
    # Generate final report
    generate_system_report()
    
    # Print summary
    print_header("VERIFICATION SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} {check_name}")
    
    print(f"\n📊 Overall Status: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 ALL CHECKS PASSED - System is properly consolidated!")
        print("🚀 Ready to run: python run_system.py")
    else:
        print("⚠️  Some checks failed - Please review the issues above")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main() 