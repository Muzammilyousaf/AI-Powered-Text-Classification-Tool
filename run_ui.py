#!/usr/bin/env python3
"""
Simple script to run the web UI
"""

from app import app, init_classifier

if __name__ == '__main__':
    print("=" * 60)
    print("AI-Powered Text Classification Tool - Web UI")
    print("=" * 60)
    print()
    
    # Initialize classifier
    from app import classifier
    success, message = init_classifier()
    if success:
        print("✅ Classifier initialized successfully")
        if classifier:
            print(f"   Labels: {', '.join(classifier.labels)}")
    else:
        print(f"⚠️  Warning: {message}")
        print("   Make sure OPENAI_API_KEY is set in .env file")
    
    print()
    print("🌐 Starting web server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print()
    print("=" * 60)
    print()
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)

