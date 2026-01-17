#!/usr/bin/env python3
"""
Startup script for the AI-Based Rockfall Prediction System Dashboard
"""

import sys
import os
import time

def main():
    print("=" * 60)
    print("🏔️  AI-Based Rockfall Prediction System")
    print("🌐 Web Dashboard Starting...")
    print("=" * 60)
    
    # Test system components first
    print("\n📋 Running System Health Check...")
    
    try:
        from test_system import main as test_main
        if not test_main():
            print("❌ System health check failed. Please fix issues before starting.")
            return False
    except Exception as e:
        print(f"⚠️  Could not run health check: {e}")
        print("Proceeding anyway...")
    
    print("\n🚀 Starting Flask Web Server...")
    
    # Import and run the app
    try:
        from app import app
        
        print(f"🌍 Server will be available at: http://localhost:5000")
        print(f"📊 Dashboard URL: http://localhost:5000")
        print(f"🔗 API Status: http://localhost:5000/api/status")
        print("\n💡 Features Available:")
        print("   • Interactive map with 18 Indian mining sites")
        print("   • Real-time rockfall risk predictions")
        print("   • Multi-level alert system")
        print("   • Mine details and historical data")
        print("   • System health monitoring")
        
        print(f"\n⏹️  Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Run the app
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            use_reloader=False  # Disable reloader to avoid issues
        )
        
    except ImportError as e:
        print(f"❌ Failed to import Flask app: {e}")
        print("Make sure all dependencies are installed:")
        print("   pip install flask pandas numpy scikit-learn")
        return False
    except KeyboardInterrupt:
        print(f"\n\n👋 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Server error: {e}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n👋 Goodbye!")
        sys.exit(0)
