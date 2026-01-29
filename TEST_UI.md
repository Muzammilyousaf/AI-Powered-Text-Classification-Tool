# Testing the Web UI

## Quick Start

1. **Start the server:**
   ```bash
   python run_ui.py
   ```
   
   Or on Windows:
   ```bash
   START_SERVER.bat
   ```

2. **Open your browser:**
   - Go to: http://localhost:5000

3. **Test the UI:**
   - Try single text classification
   - Try batch text processing
   - Try file upload

## Automated Testing

Run the test script (requires server to be running):

```bash
# Terminal 1: Start server
python run_ui.py

# Terminal 2: Run tests
python test_ui.py
```

## Manual Testing Steps

### 1. Test Single Text Classification

1. Open http://localhost:5000
2. Make sure "Single Text" tab is selected
3. Enter: `"I'm very unhappy with the service"`
4. Click "Classify Text"
5. Should see: Label "Complaint" with confidence score

### 2. Test Batch Classification

1. Click "Batch Text" tab
2. Enter multiple texts (one per line):
   ```
   What are your business hours?
   I love your new product!
   The delivery was late.
   ```
3. Click "Classify All"
4. Should see results for all 3 texts

### 3. Test File Upload

1. Click "Upload File" tab
2. Create a test file `test.txt`:
   ```
   How do I reset my password?
   I want a refund immediately.
   Great service, thank you!
   ```
3. Upload the file
4. Should see classification results for all lines

### 4. Test Download Results

1. After getting results, click "Download Results (JSON)"
2. Should download a JSON file with all classifications

## Expected Results

- **Complaint**: "I'm very unhappy", "I want a refund"
- **Inquiry**: "What are your hours?", "How do I reset?"
- **Feedback**: "I love your product", "Great service"
- **Other**: "The weather is nice"

## Troubleshooting

### Server won't start
- Check if port 5000 is already in use
- Make sure OPENAI_API_KEY is set in .env file
- Check Python version (3.8+)

### API errors
- Verify API key is valid
- Check internet connection
- Ensure OpenAI API has credits

### UI not loading
- Check browser console for errors
- Verify server is running on port 5000
- Try clearing browser cache

