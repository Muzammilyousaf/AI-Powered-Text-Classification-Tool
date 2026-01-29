#!/usr/bin/env python3
"""
Flask web application for Text Classification Tool
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from text_classifier import TextClassifier
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# Initialize classifier
classifier = None

def init_classifier():
    """Initialize the text classifier"""
    global classifier
    try:
        classifier = TextClassifier()
        return True, "Classifier initialized successfully"
    except Exception as e:
        return False, str(e)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/classify', methods=['POST'])
def classify_text():
    """Classify a single text"""
    global classifier
    
    if classifier is None:
        success, message = init_classifier()
        if not success:
            return jsonify({'error': f'Failed to initialize classifier: {message}'}), 500
    
    data = request.get_json()
    text = data.get('text', '').strip()
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        result = classifier.classify(text)
        
        response = {
            'text': result.text,
            'predicted_label': result.predicted_label,
            'confidence': result.confidence,
            'rationale': result.rationale
        }
        
        if result.error:
            response['error'] = result.error
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/classify-batch', methods=['POST'])
def classify_batch():
    """Classify multiple texts"""
    global classifier
    
    if classifier is None:
        success, message = init_classifier()
        if not success:
            return jsonify({'error': f'Failed to initialize classifier: {message}'}), 500
    
    data = request.get_json()
    texts = data.get('texts', [])
    
    if not texts or not isinstance(texts, list):
        return jsonify({'error': 'No texts provided or invalid format'}), 400
    
    if len(texts) > 100:  # Limit batch size
        return jsonify({'error': 'Maximum 100 texts per batch'}), 400
    
    try:
        results = classifier.classify_batch(texts)
        
        response = []
        for result in results:
            item = {
                'text': result.text,
                'predicted_label': result.predicted_label,
                'confidence': result.confidence,
                'rationale': result.rationale
            }
            if result.error:
                item['error'] = result.error
            response.append(item)
        
        return jsonify({'results': response, 'count': len(response)})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/classify-file', methods=['POST'])
def classify_file():
    """Classify texts from uploaded file"""
    global classifier
    
    if classifier is None:
        success, message = init_classifier()
        if not success:
            return jsonify({'error': f'Failed to initialize classifier: {message}'}), 500
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Read file content
        content = file.read().decode('utf-8')
        
        # Try to parse as JSON first
        try:
            data = json.loads(content)
            if isinstance(data, list):
                texts = [str(t) for t in data]
            else:
                texts = [content]
        except json.JSONDecodeError:
            # Treat as line-separated text
            texts = [line.strip() for line in content.split('\n') if line.strip()]
        
        if not texts:
            return jsonify({'error': 'No valid texts found in file'}), 400
        
        if len(texts) > 100:
            return jsonify({'error': 'Maximum 100 texts per file'}), 400
        
        # Classify
        results = classifier.classify_batch(texts)
        
        response = []
        for result in results:
            item = {
                'text': result.text,
                'predicted_label': result.predicted_label,
                'confidence': result.confidence,
                'rationale': result.rationale
            }
            if result.error:
                item['error'] = result.error
            response.append(item)
        
        return jsonify({'results': response, 'count': len(response)})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get classifier status"""
    global classifier
    
    if classifier is None:
        success, message = init_classifier()
        if not success:
            return jsonify({
                'status': 'error',
                'message': message,
                'labels': []
            })
    
    return jsonify({
        'status': 'ready',
        'labels': classifier.labels,
        'model': classifier.model
    })

@app.route('/api/download-results', methods=['POST'])
def download_results():
    """Download classification results as JSON"""
    data = request.get_json()
    results = data.get('results', [])
    
    if not results:
        return jsonify({'error': 'No results to download'}), 400
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    json.dump(results, temp_file, indent=2, ensure_ascii=False)
    temp_file.close()
    
    return send_file(
        temp_file.name,
        mimetype='application/json',
        as_attachment=True,
        download_name='classification_results.json'
    )

if __name__ == '__main__':
    # Initialize classifier on startup
    init_classifier()
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)

