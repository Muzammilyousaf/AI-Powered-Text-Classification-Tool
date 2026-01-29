#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script showing text classification output format
This demonstrates what the classifier would produce without making API calls
"""

import json
import sys
from datetime import datetime

# Fix encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def demo_classification():
    """Show example classification outputs"""
    
    demo_results = [
        {
            "text": "I'm very unhappy with the service I received yesterday. The staff was rude and unhelpful.",
            "predicted_label": "Complaint",
            "confidence": 0.98,
            "rationale": "The text clearly expresses dissatisfaction and negative experiences with service and staff."
        },
        {
            "text": "What are your business hours? Do you offer weekend service?",
            "predicted_label": "Inquiry",
            "confidence": 0.95,
            "rationale": "The text contains direct questions seeking information about business operations."
        },
        {
            "text": "I love your new product design! The user interface is much more intuitive now.",
            "predicted_label": "Feedback",
            "confidence": 0.92,
            "rationale": "The text provides positive feedback and constructive comments about product improvements."
        },
        {
            "text": "Can you tell me more about your pricing plans?",
            "predicted_label": "Inquiry",
            "confidence": 0.93,
            "rationale": "The text asks a question seeking information about pricing."
        },
        {
            "text": "The delivery was late and the package was damaged. This is unacceptable.",
            "predicted_label": "Complaint",
            "confidence": 0.97,
            "rationale": "The text expresses clear dissatisfaction with delivery service and product condition."
        },
        {
            "text": "I think you should consider adding more payment options. That would be helpful.",
            "predicted_label": "Feedback",
            "confidence": 0.88,
            "rationale": "The text provides a constructive suggestion for improvement."
        },
        {
            "text": "The weather is nice today.",
            "predicted_label": "Other",
            "confidence": 0.85,
            "rationale": "The text does not fit into complaint, inquiry, or feedback categories."
        },
        {
            "text": "How do I reset my password?",
            "predicted_label": "Inquiry",
            "confidence": 0.96,
            "rationale": "The text is a direct question seeking information or instructions."
        },
        {
            "text": "Your customer support team is excellent! Very responsive and helpful.",
            "predicted_label": "Feedback",
            "confidence": 0.94,
            "rationale": "The text provides positive feedback about customer support service."
        },
        {
            "text": "I want a refund immediately. This product doesn't work as advertised.",
            "predicted_label": "Complaint",
            "confidence": 0.99,
            "rationale": "The text expresses strong dissatisfaction and a demand for refund due to product issues."
        }
    ]
    
    print("=" * 80)
    print("Text Classification Tool - Demo Output")
    print("=" * 80)
    print()
    print("This is a DEMO showing the expected output format.")
    print("To run actual classifications, you need to set up your OpenAI API key.")
    print()
    print("=" * 80)
    print("Classification Results")
    print("=" * 80)
    print()
    
    correct = 0
    total = len(demo_results)
    
    # Expected labels for accuracy calculation
    expected_labels = {
        0: "Complaint",
        1: "Inquiry",
        2: "Feedback",
        3: "Inquiry",
        4: "Complaint",
        5: "Feedback",
        6: "Other",
        7: "Inquiry",
        8: "Feedback",
        9: "Complaint"
    }
    
    for i, result in enumerate(demo_results, 1):
        expected = expected_labels[i-1]
        predicted = result["predicted_label"]
        match = predicted == expected
        status = "[OK]" if match else "[X]"
        
        if match:
            correct += 1
        
        print(f"Test {i}/{total} {status}")
        print(f"Text: {result['text'][:70]}..." if len(result['text']) > 70 else f"Text: {result['text']}")
        print(f"Expected: {expected}")
        print(f"Predicted: {predicted}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Rationale: {result['rationale']}")
        print()
        print("-" * 80)
        print()
    
    # Summary
    print("=" * 80)
    print("Demo Summary")
    print("=" * 80)
    print(f"Total tests: {total}")
    print(f"Correct: {correct}")
    print(f"Accuracy: {correct/total*100:.1f}%")
    print()
    
    # JSON output
    print("JSON Output Format:")
    print("=" * 80)
    print(json.dumps(demo_results, indent=2, ensure_ascii=False))
    print()
    
    # Save to file
    output_file = "demo_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "demo": True,
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": total,
                "correct": correct,
                "accuracy": correct/total*100
            },
            "results": demo_results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Demo results saved to {output_file}")
    print()
    print("=" * 80)
    print("Next Steps:")
    print("=" * 80)
    print("1. Run: python setup_api_key.py")
    print("2. Or manually edit .env file with your OpenAI API key")
    print("3. Then run: python test_examples.py")
    print()

if __name__ == "__main__":
    demo_classification()

