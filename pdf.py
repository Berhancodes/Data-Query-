import os
import logging
from llama_index import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers import PDFReader

# Setup logging
logging.basicConfig(filename='pdf_processing_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def get_index(data, index_name, rebuild=False):
    index = None
    try:
        if rebuild or not os.path.exists(index_name):
            if rebuild:
                print(f"Rebuilding index for {index_name}")
            else:
                print(f"Building index for {index_name}")
            logging.info(f"Building index: {index_name}")
            index = VectorStoreIndex.from_documents(data, show_progress=True)
            index.storage_context.persist(persist_dir=index_name)
        else:
            print(f"Loading existing index for {index_name}")
            logging.info(f"Loading index from storage: {index_name}")
            index = load_index_from_storage(
                StorageContext.from_defaults(persist_dir=index_name)
            )
    except Exception as e:
        print(f"An error occurred while processing the index: {e}")
        logging.error(f"Error processing index {index_name}: {e}")
        exit(1)
    
    return index

def create_pdf_engine(pdf_path, index_name, rebuild=False):
    try:
        print(f"Loading PDF file: {pdf_path}")
        pdf_data = PDFReader().load_data(file=pdf_path)
        logging.info(f"Loaded PDF file: {pdf_path}")
    except FileNotFoundError:
        print(f"Error: PDF file not found at {pdf_path}")
        logging.error(f"PDF file not found: {pdf_path}")
        exit(1)
    except Exception as e:
        print(f"An error occurred while reading the PDF file: {e}")
        logging.error(f"Error reading PDF file {pdf_path}: {e}")
        exit(1)
    
    pdf_index = get_index(pdf_data, index_name, rebuild)
    return pdf_index.as_query_engine()
