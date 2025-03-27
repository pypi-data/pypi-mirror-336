import os
import sys
import argparse
from PyPDF2 import PdfMerger

def combine_pdfs_in_folder(folder_path, output_filename='combined.pdf'):
    """
    Combine all PDF files in a specified folder into a single PDF.
    
    Args:
    folder_path (str): Path to the folder containing PDF files
    output_filename (str, optional): Name of the output combined PDF file. Defaults to 'combined.pdf'
    
    Returns:
    str: Path to the combined PDF file
    """
    # Create a PDF merger object
    merger = PdfMerger()
    
    # List to store PDF files
    pdf_files = []
    
    # Find all PDF files in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            pdf_files.append(filename)
    
    # Sort PDF files to ensure consistent order
    pdf_files.sort()
    
    # Check if any PDFs were found
    if not pdf_files:
        raise ValueError("No PDF files found in the specified folder.")
    
    # Merge PDF files
    try:
        for filename in pdf_files:
            filepath = os.path.join(folder_path, filename)
            merger.append(filepath)
        
        # Output combined PDF
        output_path = os.path.join(folder_path, output_filename)
        merger.write(output_path)
        merger.close()
        
        print(f"Successfully combined {len(pdf_files)} PDF files.")
        return output_path
    
    except Exception as e:
        print(f"An error occurred while combining PDFs: {e}")
        return None

def main():
    """
    Command-line interface for PDF combining tool
    """
    parser = argparse.ArgumentParser(description='Combine PDF files in a folder')
    parser.add_argument('folder', help='Path to the folder containing PDF files')
    parser.add_argument('-o', '--output', default='combined.pdf', 
                        help='Name of the output PDF file (default: combined.pdf)')
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        # Resolve to absolute path
        folder_path = os.path.abspath(args.folder)
        
        # Validate folder exists
        if not os.path.isdir(folder_path):
            print(f"Error: {folder_path} is not a valid directory.")
            sys.exit(1)
        
        # Combine PDFs
        combined_pdf_path = combine_pdfs_in_folder(folder_path, args.output)
        
        if combined_pdf_path:
            print(f"Combined PDF saved at: {combined_pdf_path}")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()