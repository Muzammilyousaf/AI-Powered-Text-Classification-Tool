#!/usr/bin/env python3
"""
Helper script to set up OpenAI API key
"""

import os
from pathlib import Path

def setup_api_key():
    """Interactive setup for OpenAI API key"""
    print("=" * 60)
    print("OpenAI API Key Setup")
    print("=" * 60)
    print()
    print("To get your API key:")
    print("1. Go to: https://platform.openai.com/api-keys")
    print("2. Sign in or create an account")
    print("3. Click 'Create new secret key'")
    print("4. Copy the key (it starts with 'sk-')")
    print()
    
    api_key = input("Paste your OpenAI API key here (or press Enter to skip): ").strip()
    
    if not api_key:
        print("\nNo API key provided. You can set it later:")
        print("1. Edit the .env file manually")
        print("2. Or set environment variable: $env:OPENAI_API_KEY='your-key'")
        return False
    
    if not api_key.startswith('sk-'):
        print("\n⚠️  Warning: API keys usually start with 'sk-'. Please verify your key.")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            return False
    
    # Write to .env file
    env_file = Path('.env')
    
    if env_file.exists():
        # Read existing content
        with open(env_file, 'r') as f:
            content = f.read()
        
        # Replace existing key or add new one
        if 'OPENAI_API_KEY=' in content:
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                if line.startswith('OPENAI_API_KEY='):
                    new_lines.append(f'OPENAI_API_KEY={api_key}')
                else:
                    new_lines.append(line)
            content = '\n'.join(new_lines)
        else:
            content += f'\nOPENAI_API_KEY={api_key}\n'
        
        with open(env_file, 'w') as f:
            f.write(content)
    else:
        # Create new .env file
        with open(env_file, 'w') as f:
            f.write(f"# OpenAI API Configuration\n")
            f.write(f"OPENAI_API_KEY={api_key}\n")
    
    print("\n✅ API key saved to .env file!")
    print("\n⚠️  Important: Never commit .env file to version control!")
    print("   The .gitignore file should already exclude it.")
    
    # Test if it works
    print("\nTesting API key...")
    os.environ['OPENAI_API_KEY'] = api_key
    try:
        from text_classifier import TextClassifier
        classifier = TextClassifier()
        print("✅ API key is valid and classifier initialized successfully!")
        return True
    except Exception as e:
        print(f"⚠️  Could not verify API key: {e}")
        print("   The key has been saved, but please verify it's correct.")
        return False

if __name__ == "__main__":
    setup_api_key()

