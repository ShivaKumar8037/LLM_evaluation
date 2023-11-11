# LLM_evaluation 
### Usecase: SQL to PySpark Query Converter


This Streamlit-based web application converts SQL queries into PySpark syntax using Google's PaLM API. It provides an easy-to-use interface for users to input SQL queries and view the converted PySpark code. Additionally, users can rate the accuracy of the conversions.

## Installation

To set up the application, you need to install the necessary Python libraries. Run the following command:

```bash
pip install streamlit pandas matplotlib seaborn google-generativeai llama_index
```

### Running the Application
To run the application, use the following command
```bash
streamlit run app.py
```

### Usage
In the web interface:

-  Input your SQL query.
-  View the converted PySpark query.
-  Rate the conversion (Good, Bad, Somewhat).

