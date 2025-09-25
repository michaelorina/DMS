import os
import extract_msg
import base64

def process_msg_file(filepath):
    """
    Wrapper for MSG file processing that captures output and returns structured data.
    """
    
    try:
        # Import and use the existing MSG processor
        import extract_msg
        
        # Load the .msg file
        msg = extract_msg.Message(filepath)
        
        # Extract message data
        result = {
            'file_type': 'msg',
            'subject': msg.subject,
            'date': str(msg.date) if msg.date else None,
            'sender': msg.sender,
            'to': msg.to,
            'body': msg.body,
            'attachments': []
        }
        
        # Process attachments
        for att in msg.attachments:
            attachment_info = {
                'filename': att.longFilename or att.shortFilename,
                'size': len(att.data) if att.data else 0
            }
            if att.data:
                attachment_info['data_base64'] = base64.b64encode(att.data).decode('utf-8')
                # attachment_info['data_bytes'] = att.data
            result['attachments'].append(attachment_info)
        
        msg.close()
        
        return result
        
    except Exception as e:
        raise Exception(f"Error processing MSG file: {str(e)}")

def process_msg_file_prev(msg_path, output_dir="attachments", save_attachments=False):
    """
    Process a .msg file and extract its contents.
    
    Args:
        msg_path (str): Path to the .msg file
        output_dir (str): Directory to save attachments (if save_attachments=True)
        save_attachments (bool): Whether to save attachments to disk
        
    Returns:
        dict: Extracted message data
    """
    # Load the .msg file
    msg = extract_msg.Message(msg_path)
    msg_subject = msg.subject
    msg_date = msg.date
    msg_sender = msg.sender
    msg_to = msg.to
    msg_body = msg.body

    # Print message details
    print("📌 Subject:", msg_subject)
    print("📅 Date:", msg_date)
    print("👤 From:", msg_sender)
    print("📩 To:", msg_to)
    print("📝 Body:\n", msg_body)

    # Prepare result data
    result = {
        'subject': msg_subject,
        'date': str(msg_date) if msg_date else None,
        'sender': msg_sender,
        'to': msg_to,
        'body': msg_body,
        'attachments': []
    }

    # Save attachments if requested
    if save_attachments and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for att in msg.attachments:
        attachment_name = att.longFilename or att.shortFilename
        attachment_info = {
            'filename': attachment_name,
            'size': len(att.data) if att.data else 0
        }
        result['attachments'].append(attachment_info)
        
        if save_attachments:
            filename = os.path.join(output_dir, attachment_name)
            with open(filename, "wb") as f:
                f.write(att.data)
            print(f"📎 Saved attachment: {filename}")

    msg.close()
    return result

if __name__ == "__main__":
    msg_file = "sample.msg"  # change to your .msg file path
    process_msg_file(msg_file)
