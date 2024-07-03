from llama_index import PromptTemplate

instruction_str = """\
    1. Transform the user's query into a precise Python expression using the Pandas library.
    2. The last line must be an executable Python expression that can be evaluated with the `eval()` function.
    3. Make sure the code addresses the user's query effectively.
    4. OUTPUT ONLY THE EXPRESSION, nothing more.
    5. Avoid quoting the expression to ensure it's executable."""


new_prompt = PromptTemplate(
    """\
    Greetings! You have a Pandas dataframe named `df` ready for analysis.
    Here's a quick look at the dataframe:
    {df_str}

    Follow these steps carefully:
    {instruction_str}

    User Query: {query_str}

    Generated Expression: """
)


context = """Hello! I'm your friendly data assistant, here to help you dive deep into your CSV and PDF data.
            Whether you need to uncover patterns, gather statistics, or find specific information, just ask away!
            I'm equipped to provide you with precise and insightful responses to make your data exploration effortless and enjoyable."""
