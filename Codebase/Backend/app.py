from flask import Flask, jsonify, request
import os
from werkzeug.utils import secure_filename
from dms.extractors.main import process_file

app = Flask(__name__)

# Configure file upload settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'msg', 'pdf', 'doc', 'docx', 'txt', 'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create upload directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/dms', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    if not files or all(file.filename == '' for file in files):
        return jsonify({'error': 'No files selected'}), 400
    
    results = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Save the uploaded file
            file.save(filepath)
            
            try:
                # Process the file through the extractor
                result = process_file(filepath)
                results.append({
                    'filename': filename,
                    'status': 'success',
                    'result': result
                })
            except Exception as e:
                results.append({
                    'filename': filename,
                    'status': 'error',
                    'error': str(e)
                })
                
            # Clean up the uploaded file after processing
            try:
                os.remove(filepath)
            except OSError:
                pass
        else:
            results.append({
                'filename': file.filename,
                'status': 'error',
                'error': 'File type not allowed'
            })
    
    return jsonify({'results': results})

@app.route('/api/dms', methods=['GET'])
def hello():
    return jsonify({"message": "DMS File Processing Service", "supported_formats": list(ALLOWED_EXTENSIONS)})

if __name__ == '__main__':
    app.run(debug=True)