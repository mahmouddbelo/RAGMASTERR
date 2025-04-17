from flask import Blueprint, render_template, request, jsonify, current_app, session
from werkzeug.utils import secure_filename
import os
from app.models.rag_manager import RAGManager

bp = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        try:
            # Initialize RAG manager
            rag_manager = RAGManager(
                chunk_size=current_app.config['CHUNK_SIZE'],
                chunk_overlap=current_app.config['CHUNK_OVERLAP'],
                embedding_model=current_app.config['EMBEDDING_MODEL']
            )
            
            # Process the file
            rag_manager.load_document(file_path)
            rag_manager.process_text()
            rag_manager.build_vectorstore()
            
            # Save vectorstore
            vectorstore_path = os.path.join(current_app.config['VECTORSTORE_DIR'], 'current_vectorstore')
            rag_manager.save_vectorstore(vectorstore_path)
            
            return jsonify({'message': 'File processed successfully'}), 200
        except Exception as e:
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@bp.route('/process_url', methods=['POST'])
def process_url():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    try:
        # Initialize RAG manager
        rag_manager = RAGManager(
            chunk_size=current_app.config['CHUNK_SIZE'],
            chunk_overlap=current_app.config['CHUNK_OVERLAP'],
            embedding_model=current_app.config['EMBEDDING_MODEL']
        )
        
        # Process the URL
        rag_manager.load_document(url)
        rag_manager.process_text()
        rag_manager.build_vectorstore()
        
        # Save vectorstore
        vectorstore_path = os.path.join(current_app.config['VECTORSTORE_DIR'], 'current_vectorstore')
        rag_manager.save_vectorstore(vectorstore_path)
        
        return jsonify({'message': 'URL processed successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Error processing URL: {str(e)}'}), 500

@bp.route('/query', methods=['POST'])
def query():
    question = request.json.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        # Initialize RAG manager and load existing vectorstore
        rag_manager = RAGManager(
            chunk_size=current_app.config['CHUNK_SIZE'],
            chunk_overlap=current_app.config['CHUNK_OVERLAP'],
            embedding_model=current_app.config['EMBEDDING_MODEL']
        )
        
        vectorstore_path = os.path.join(current_app.config['VECTORSTORE_DIR'], 'current_vectorstore')
        rag_manager.load_vectorstore(vectorstore_path)
        
        # Get answer
        answer = rag_manager.query(question)
        
        return jsonify({'answer': answer}), 200
    except Exception as e:
        return jsonify({'error': f'Error getting answer: {str(e)}'}), 500 