from dotenv import load_dotenv
import os
import pandas as pd
from llama_index.query_engine import PandasQueryEngine
from prompts import new_prompt, instruction_str, context
from note_engine import note_saver_tool, note_reader_tool
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.agent import ReActAgent
from llama_index.llms import OpenAI
from pdf import create_pdf_engine
import logging

# Setup logging
logging.basicConfig(filename='query_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Load environment variables
load_dotenv()

# Load CSV data
csv_path = os.path.join("data", os.getenv("CSV_FILE", "sample_data.csv"))
try:
    csv_df = pd.read_csv(csv_path)
    logging.info(f"Loaded CSV file: {csv_path}")
except FileNotFoundError:
    logging.error(f"CSV file not found: {csv_path}")
    print(f"Error: CSV file not found at {csv_path}")
    exit(1)

# Setup CSV query engine
csv_query_engine = PandasQueryEngine(
    df=csv_df, verbose=True, instruction_str=instruction_str
)
csv_query_engine.update_prompts({"pandas_prompt": new_prompt})

# Load PDF data
pdf_path = os.path.join("data", os.getenv("PDF_FILE", "sample_document.pdf"))
try:
    pdf_engine = create_pdf_engine(pdf_path, "document_index")
    logging.info(f"Loaded PDF file: {pdf_path}")
except FileNotFoundError:
    logging.error(f"PDF file not found: {pdf_path}")
    print(f"Error: PDF file not found at {pdf_path}")
    exit(1)
# Get OpenAI API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    logging.error("OpenAI API key not found in environment variables.")
    print("Error: OpenAI API key not found. Please set it in your .env file.")
    exit(1)

# Setup tools
tools = [
    note_saver_tool,
    note_reader_tool,
    QueryEngineTool(
        query_engine=csv_query_engine,
        metadata=ToolMetadata(
            name="csv_data",
            description="Provides information from the CSV data",
        ),
    ),
    QueryEngineTool(
        query_engine=pdf_engine,
        metadata=ToolMetadata(
            name="pdf_data",
            description="Provides information from the PDF document",
        ),
    ),
]

# Setup LLM and agent
llm = OpenAI(model="gpt-3.5-turbo-0613", api_key=openai_api_key)
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)

print("Welcome! You can ask questions about the data, save notes, or list notes. Type 'q' to quit.")

while (prompt := input("Enter a prompt: ")) != "q":
    try:
        result = agent.query(prompt)
        print("Response:", result)
        logging.info(f"Query: {prompt}")
        logging.info(f"Response: {result}")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"Error during query: {prompt} - {e}")

print("Thank you for using the data query tool!")
