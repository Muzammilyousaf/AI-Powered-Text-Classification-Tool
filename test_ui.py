#!/usr/bin/env python3
"""
Test script for the web UI API endpoints
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:5000"

def test_status():
    """Test the status endpoint"""
    print("Testing /api/status...")
    try:
        response = requests.get(f"{BASE_URL}/api/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data.get('status')}")
            print(f"   Labels: {', '.join(data.get('labels', []))}")
            return True
        else:
            print(f"❌ Status check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
        print("   Start the server with: python run_ui.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_classify_single():
    """Test single text classification"""
    print("\nTesting /api/classify (single text)...")
    test_text = "I'm very unhappy with the service I received yesterday. The staff was rude."
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/classify",
            json={"text": test_text},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Classification successful!")
            print(f"   Text: {test_text[:50]}...")
            print(f"   Label: {data.get('predicted_label')}")
            print(f"   Confidence: {data.get('confidence', 'N/A')}")
            if data.get('rationale'):
                print(f"   Rationale: {data.get('rationale')[:80]}...")
            return True
        else:
            print(f"❌ Classification failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_classify_batch():
    """Test batch text classification"""
    print("\nTesting /api/classify-batch...")
    test_texts = [
        "What are your business hours?",
        "I love your new product design!",
        "The delivery was late and damaged."
    ]
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/classify-batch",
            json={"texts": test_texts},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            print(f"✅ Batch classification successful!")
            print(f"   Processed: {data.get('count')} texts")
            for i, result in enumerate(results, 1):
                print(f"   {i}. {result.get('predicted_label')} - {result.get('text', '')[:40]}...")
            return True
        else:
            print(f"❌ Batch classification failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("Web UI API Test Suite")
    print("=" * 60)
    print()
    print("Make sure the server is running:")
    print("  python run_ui.py")
    print()
    print("Waiting 2 seconds for server check...")
    time.sleep(2)
    print()
    
    results = []
    
    # Test status
    results.append(("Status Check", test_status()))
    
    # Test single classification
    results.append(("Single Classification", test_classify_single()))
    
    # Test batch classification
    results.append(("Batch Classification", test_classify_batch()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The web UI is working correctly.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)

