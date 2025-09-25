import os
import textract
from pathlib import Path

def extract_text_from_file(filepath):
    """
    Extract text from various document types using textract.
    
    Supported formats:
    - PDF files (.pdf)
    - Microsoft Word documents (.docx, .doc)
    - Images with text (.png, .jpg, .jpeg) - requires OCR
    
    Args:
        filepath (str): Path to the file to extract text from
        
    Returns:
        dict: Extracted text and metadata
    """
    
    try:
        # Get file info
        filename = os.path.basename(filepath)
        file_size = os.path.getsize(filepath)
        _, file_extension = os.path.splitext(filepath)
        file_extension = file_extension.lower()
        
        # Extract text using textract
        text = textract.process(filepath).decode('utf-8')
        
        # Clean up the extracted text
        text = text.strip()
        
        result = {
            'file_type': file_extension[1:] if file_extension else 'unknown',
            'filename': filename,
            'size': file_size,
            'extracted_text': text,
            'text_length': len(text),
            'word_count': len(text.split()) if text else 0,
            'extraction_method': 'textract',
            'status': 'success'
        }
        
        return result
        
    except Exception as e:
        # Return error information if extraction fails
        filename = os.path.basename(filepath) if os.path.exists(filepath) else 'unknown'
        _, file_extension = os.path.splitext(filepath)
        
        return {
            'file_type': file_extension[1:] if file_extension else 'unknown',
            'filename': filename,
            'size': os.path.getsize(filepath) if os.path.exists(filepath) else 0,
            'extracted_text': None,
            'text_length': 0,
            'word_count': 0,
            'extraction_method': 'textract',
            'status': 'error',
            'error_message': str(e)
        }


def extract_text_from_pdf(filepath):
    """
    Specialized PDF text extraction function.
    
    Args:
        filepath (str): Path to the PDF file
        
    Returns:
        dict: Extracted text and metadata
    """
    
    try:
        text = textract.process(filepath, method='pdftotext').decode('utf-8')
        
        return {
            'file_type': 'pdf',
            'filename': os.path.basename(filepath),
            'size': os.path.getsize(filepath),
            'extracted_text': text.strip(),
            'text_length': len(text.strip()),
            'word_count': len(text.split()) if text else 0,
            'extraction_method': 'pdftotext',
            'status': 'success'
        }
        
    except Exception as e:
        # Fallback to general textract method
        return extract_text_from_file(filepath)


def extract_text_from_docx(filepath):
    """
    Specialized DOCX text extraction function.
    
    Args:
        filepath (str): Path to the DOCX file
        
    Returns:
        dict: Extracted text and metadata
    """
    
    try:
        text = textract.process(filepath, method='docx2txt').decode('utf-8')
        
        return {
            'file_type': 'docx',
            'filename': os.path.basename(filepath),
            'size': os.path.getsize(filepath),
            'extracted_text': text.strip(),
            'text_length': len(text.strip()),
            'word_count': len(text.split()) if text else 0,
            'extraction_method': 'docx2txt',
            'status': 'success'
        }
        
    except Exception as e:
        # Fallback to general textract method
        return extract_text_from_file(filepath)


def extract_text_from_image(filepath):
    """
    Extract text from images using OCR via textract.
    
    Args:
        filepath (str): Path to the image file
        
    Returns:
        dict: Extracted text and metadata
    """
    
    try:
        # textract uses tesseract OCR for image text extraction
        text = textract.process(filepath, method='tesseract').decode('utf-8')
        
        return {
            'file_type': 'image',
            'filename': os.path.basename(filepath),
            'size': os.path.getsize(filepath),
            'extracted_text': text.strip(),
            'text_length': len(text.strip()),
            'word_count': len(text.split()) if text else 0,
            'extraction_method': 'tesseract_ocr',
            'status': 'success'
        }
        
    except Exception as e:
        return {
            'file_type': 'image',
            'filename': os.path.basename(filepath),
            'size': os.path.getsize(filepath) if os.path.exists(filepath) else 0,
            'extracted_text': None,
            'text_length': 0,
            'word_count': 0,
            'extraction_method': 'tesseract_ocr',
            'status': 'error',
            'error_message': f"OCR extraction failed: {str(e)}"
        }


def batch_extract_text(file_paths):
    """
    Extract text from multiple files.
    
    Args:
        file_paths (list): List of file paths to process
        
    Returns:
        list: List of extraction results
    """
    
    results = []
    
    for filepath in file_paths:
        try:
            result = extract_text_from_file(filepath)
            results.append(result)
        except Exception as e:
            results.append({
                'filename': os.path.basename(filepath),
                'status': 'error',
                'error_message': str(e)
            })
    
    return results


if __name__ == "__main__":
    # Test the extraction functions
    test_file = "sample.pdf"  # Change to your test file path
    result = extract_text_from_file(test_file)
    print(f"Extracted {result['word_count']} words from {result['filename']}")
    print(f"Text preview: {result['extracted_text'][:200]}...")