import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import google.generativeai as palm
from llama_index.llms.palm import PaLM


def palmAPI(yourApiKey, prompt ):
    palm_api_key = yourApiKey
    palm.configure(api_key=palm_api_key)
    model = PaLM(api_key=palm_api_key)
    return model.complete(prompt).text





#Get your PalmAPI from the google 
def final_output(sqlQueries):
    outputQueries = []
    for i in range(len(sqlQueries)):
        outputQueries.append(palmAPI("", prompt = "Convert this SQL query " + sqlQueries[i] + " into pyspark"))

    return  outputQueries
    

st.title('Query Rating Visualization')

# Sample queries
queries = ["SELECT Orders.OrderID, Products.ProductName, OrderDetails.Quantity  FROM Orders INNER JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID INNER JOIN Products ON OrderDetails.ProductID = Products.ProductID;", "SELECT Customers.CustomerID, Customers.FirstName, Customers.LastName, SUM(Orders.TotalAmount) AS TotalSalesAmount FROM Customers INNER JOIN Orders ON Customers.CustomerID = Orders.CustomerID GROUP BY Customers.CustomerID, Customers.FirstName, Customers.LastName;", 
              "SELECT FirstName, LastName FROM Customers UNION SELECT FirstName, LastName FROM Customers INNER JOIN Orders ON Customers.CustomerID = Orders.CustomerID;"]


if 'current_query_index' not in st.session_state:
    st.session_state.current_query_index = 0
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'queries2' not in st.session_state:
    st.session_state.queries2 = final_output(queries)
    
if 'completed' not in st.session_state:
    st.session_state.completed = False
if 'show_chart' not in st.session_state:
    st.session_state.show_chart = False

def display_chart():
    response_count = {'Good': 0, 'Bad': 0, 'Somewhat': 0}
    for response in st.session_state.responses.values():
        response_count[response] += 1

    df = pd.DataFrame(list(response_count.items()), columns=['Response', 'Count'])
    sns.set_style("whitegrid")
    fig, ax = plt.subplots()
    bars = ax.bar(df['Response'], df['Count'], color=['green', 'red', 'blue'])
    ax.set_xlabel('Response Type', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.set_title('Response Counts', fontsize=14)

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), 
                verticalalignment='bottom', ha='center', fontsize=10)
    st.pyplot(fig)

max_length = min(len(queries), len(st.session_state.queries2))

# Reset button
if st.button("Reset"):
    st.session_state.current_query_index = 0
    st.session_state.responses = {}
    st.session_state.completed = False
    st.session_state.show_chart = False
    # Reset other states as needed

if not st.session_state.show_chart:
    
    if st.session_state.current_query_index < max_length:
        query1 = queries[st.session_state.current_query_index]
        query2 = st.session_state.queries2[st.session_state.current_query_index]

        st.write("### Original query:")
        st.text(query1)
        st.write("### Converted query:")
        st.text(query2)

        response_key = f"Query Pair {st.session_state.current_query_index}"
        response = st.radio("Is the SQL conversion correct?", ['Good', 'Bad', 'Somewhat'], key=response_key)

        if st.button("Next"):
            if response in ['Good', 'Bad', 'Somewhat']:
                st.session_state.responses[response_key] = response
                if st.session_state.current_query_index < max_length - 1:
                    st.session_state.current_query_index += 1
                else:
                    st.session_state.completed = True
                    st.session_state.show_chart = True
            else:
                st.warning('Please select an option before proceeding.')


if st.session_state.completed and st.session_state.show_chart:
    display_chart()
