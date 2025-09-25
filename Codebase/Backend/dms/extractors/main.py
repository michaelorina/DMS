import os
from .msgToPdf import process_msg_file
from .textExtractor import extract_text_from_file
import base64

def process_file(filepath):
    """
    Main file processor that routes files to appropriate extractors based on file extension.
    
    Args:
        filepath (str): Path to the file to be processed
        
    Returns:
        dict: Processing result containing extracted data and metadata
    """
    
    # Get file extension
    _, file_extension = os.path.splitext(filepath)
    file_extension = file_extension.lower()
    
    try:
        if file_extension == '.msg':
            # Route .msg files to the msgToPdf processor
            ret  = process_msg_file(filepath)
            for att in ret["attachments"]:
                if att["filename"]:
                    att_name = att["filename"].lower()
                    if any(att_name.endswith(ext) for ext in ['.pdf', '.docx', '.doc', '.png', '.jpg', '.jpeg']):
                        try:
                            # Save attachment temporarily and extract text
                            temp_path = f"/tmp/{att['filename']}"
                            if 'data_base64' in att:
                                attachment_data =base64.b64decode(att["data_base64"])
                                with open(temp_path, 'wb') as f:
                                    f.write(attachment_data)
                            
                            # Extract text from attachment
                            att['extracted_text'] = extract_text_from_file(temp_path)
                            
                            # Clean up temp file
                            os.remove(temp_path)
                        except Exception as e:
                            att['extraction_error'] = str(e)
            
        
        elif file_extension in ['.pdf', '.docx', '.doc', '.png', '.jpg', '.jpeg']:
            # Route document files to text extractor
            return extract_text_from_file(filepath)
    
        else:
            # For other file types, return basic file info for now
            ret = process_generic_file(filepath)
            return ret
            
    except Exception as e:
        raise Exception(f"Error processing {file_extension} file: {str(e)}")


def process_generic_file(filepath):
    """
    Generic file processor for non-MSG files.
    """
    
    filename = os.path.basename(filepath)
    file_size = os.path.getsize(filepath)
    _, file_extension = os.path.splitext(filepath)
    
    return {
        'file_type': file_extension[1:] if file_extension else 'unknown',
        'filename': filename,
        'size': file_size,
        'message': f"File {filename} received and processed"
    }
