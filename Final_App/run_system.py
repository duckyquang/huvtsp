#!/usr/bin/env python3
"""
HUVTSP Unified System Runner
Coordinates all Final App components for seamless operation
"""

import os
import sys
import subprocess
import threading
import time
import webbrowser
from pathlib import Path

def print_banner():
    """Print system startup banner"""
    print("=" * 80)
    print("🚀 HUVTSP - Hydroelectric Utility Visualization & Technical Solutions Platform")
    print("=" * 80)
    print("📁 Final App - Production System Launcher")
    print("🎯 Week 4 Deliverable - Complete Interactive Dashboard")
    print("-" * 80)

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking system dependencies...")
    
    # Check Python dependencies
    required_packages = [
        ('flask', 'flask'),
        ('flask-cors', 'flask_cors'), 
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('scikit-learn', 'sklearn')
    ]
    
    missing_packages = []
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"  ✅ {package_name}")
        except ImportError:
            missing_packages.append(package_name)
            print(f"  ❌ {package_name} - Missing")
    
    if missing_packages:
        print(f"\n⚠️  Missing Python packages: {', '.join(missing_packages)}")
        print("📦 Install with: pip install " + " ".join(missing_packages))
        return False
    
    # Check Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✅ Node.js {result.stdout.strip()}")
        else:
            print("  ❌ Node.js - Not found")
            return False
    except FileNotFoundError:
        print("  ❌ Node.js - Not installed")
        return False
    
    # Check npm
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✅ npm {result.stdout.strip()}")
        else:
            print("  ❌ npm - Not found")
            return False
    except FileNotFoundError:
        print("  ❌ npm - Not installed")
        return False
    
    print("✅ All dependencies satisfied!")
    return True

def install_frontend_deps():
    """Install frontend dependencies if needed"""
    if not os.path.exists('node_modules'):
        print("📦 Installing frontend dependencies...")
        result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Frontend dependencies installed successfully!")
        else:
            print(f"❌ Failed to install frontend dependencies: {result.stderr}")
            return False
    else:
        print("✅ Frontend dependencies already installed")
    return True

def start_backend():
    """Start the Flask backend server"""
    print("🔧 Starting Flask backend server...")
    try:
        # Start Flask app
        process = subprocess.Popen(
            [sys.executable, 'app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a moment to check if it started successfully
        time.sleep(2)
        
        if process.poll() is None:
            print("✅ Flask backend started successfully on http://localhost:5000")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Flask backend failed to start: {stderr}")
            return None
    except Exception as e:
        print(f"❌ Error starting Flask backend: {e}")
        return None

def start_frontend():
    """Start the React frontend development server"""
    print("⚛️  Starting React frontend development server...")
    try:
        # Start React dev server
        process = subprocess.Popen(
            ['npm', 'run', 'dev'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for frontend to start
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ React frontend started successfully on http://localhost:8080")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ React frontend failed to start: {stderr}")
            return None
    except Exception as e:
        print(f"❌ Error starting React frontend: {e}")
        return None

def open_browser():
    """Open the application in the default browser"""
    time.sleep(3)  # Wait for servers to fully start
    print("🌐 Opening application in browser...")
    try:
        webbrowser.open('http://localhost:8080')
        print("✅ Browser opened successfully!")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print("📱 Manual access: http://localhost:8080")

def print_usage_info():
    """Print usage information"""
    print("\n" + "=" * 80)
    print("🎉 HUVTSP SYSTEM SUCCESSFULLY STARTED!")
    print("=" * 80)
    print("🌐 Frontend (React Dashboard): http://localhost:8080")
    print("🔧 Backend (Flask API): http://localhost:5000")
    print("\n📚 Quick Start Guide:")
    print("1. 📁 Upload CSV files using the drag-and-drop interface")
    print("2. 📊 View interactive charts with anomaly detection")
    print("3. 🤖 Review AI-generated summaries and insights")
    print("4. 🚨 Monitor alerts and export data as needed")
    print("\n🔗 API Endpoints:")
    print("  • GET  /api/health - System health check")
    print("  • POST /api/upload - File upload and analysis")
    print("  • GET  /api/alerts/export - Export alerts to CSV")
    print("\n⚙️  System Features:")
    print("  • Multi-algorithm anomaly detection")
    print("  • Real-time data visualization")
    print("  • AI-powered summary generation")
    print("  • Automated alert export for Zapier integration")
    print("\n💾 Data Files:")
    print("  • predictions.csv - ML model predictions")
    print("  • alerts_today.csv - Daily alert exports")
    print("  • weekly_summary.txt - AI summary text")
    print("  • anomaly_plot.png - Visualization artifacts")
    print("\n⌨️  Press Ctrl+C to stop all services")
    print("=" * 80)

def main():
    """Main system launcher"""
    print_banner()
    
    # Change to Final App directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependency check failed. Please install missing dependencies.")
        sys.exit(1)
    
    # Install frontend dependencies if needed
    if not install_frontend_deps():
        print("\n❌ Frontend setup failed.")
        sys.exit(1)
    
    print("\n🚀 Starting HUVTSP system components...")
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("\n❌ Failed to start backend. Exiting.")
        sys.exit(1)
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("\n❌ Failed to start frontend. Stopping backend.")
        backend_process.terminate()
        sys.exit(1)
    
    # Open browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Print usage information
    print_usage_info()
    
    try:
        # Keep the system running
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("\n⚠️  Backend process stopped unexpectedly")
                break
            
            if frontend_process.poll() is not None:
                print("\n⚠️  Frontend process stopped unexpectedly")
                break
    
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down HUVTSP system...")
        
        # Terminate processes gracefully
        if frontend_process and frontend_process.poll() is None:
            frontend_process.terminate()
            print("✅ Frontend server stopped")
        
        if backend_process and backend_process.poll() is None:
            backend_process.terminate()
            print("✅ Backend server stopped")
        
        print("👋 HUVTSP system shutdown complete. Thank you!")

if __name__ == "__main__":
    main() 