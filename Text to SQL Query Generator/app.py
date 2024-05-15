import streamlit as st
import google.generativeai as genai
import os
import sqlite3

from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model=genai.GenerativeModel('gemini-pro')

## Method main containing Text to SQL query generator
def main():
    ## Setting up the streamlit page with Heading
    st.set_page_config(page_title="Text2SQL Generator 🤖 ", page_icon=":robot:")
    st.markdown(
        """
            <div style="text-align: center;">
                <h1> SQL Query Generator 🤖 </h1>
                <h3> I can Generate SQL Queries for you!..</h3>
                <p> This is a simple tool that allows you to generate SQL queries based in your prompts.</p>

            </div>
        """,

        unsafe_allow_html=True,
    )

    ## User inputs will be read and submitted here
    text_input=st.text_area("Enter your Query here in plain English: ")
    database_name=st.text_input("Enter the DataBase Name: ", key="input")
    schema=st.text_area("Enter column names: ")
    submit=st.button("Generate SQL Query")

    ## Generating Query and DB output after user submission
    if submit:
        with st.spinner("Generating SQL Query..."):
            ## Generating SQL Query using the input
            template="""
                Create a SQL query snippet using the below text:\n
                You are an expert in converting English questions to SQL query!
                The SQL database has the name 
                
                    {database_name}
                
                 and has the following columns 
                
                    {schema}
                
                 Generate a SQL query 
                
                    {text_input}
                
                also the sql code should not have ``` in beginning or end and sql word in output. I just want a SQL Query.

                """
            formatted_template=template.format(text_input=text_input,database_name=database_name,schema=schema)
            response=model.generate_content(formatted_template)
            sql_query=response.text

            ## Getting the output from Table using the generated SQL Query
            query_output=read_sql_query(sql_query,database_name+".db")
            expected_output="""
                the expected response of this SQL query snippet:
                    
                    {sql_query}
                   
                is: 

                    {query_output}

                provide sample tabular response with no explanation

                """
            expected_output_formatted=expected_output.format(sql_query=sql_query,query_output=query_output)
            expected_response=model.generate_content(expected_output_formatted)
            expected_response=expected_response.text

            ## Providing simple explanation for Generated Query
            query_explanation="""
                Explain this SQL query
                    
                    {sql_query}
                    
                Please provide the simplest of explanation

                """

            explanation_formatted=query_explanation.format(sql_query=sql_query)
            explanation_resposnse=model.generate_content(explanation_formatted)
            explanation_resposnse=explanation_resposnse.text

            ## Displaying all above excution onto the Screen
            with st.container():
                st.success("SQL Query Generated Successfully!.. Here is your Query Below: ")
                st.code(sql_query, language="sql")

                st.success("Expected Output of this SQL Query will be: ")
                st.markdown(expected_response)

                st.success("Explanation for the generated Query: ")
                st.markdown(explanation_resposnse)


## Method to get the DB result from the SQL Query
def read_sql_query(sql,db):
    connection=sqlite3.connect(db)
    current_cursor=connection.cursor()
    current_cursor.execute(sql)
    query_result=current_cursor.fetchall()
    connection.commit()
    connection.close()
    for result in query_result:
        print(result)
    return query_result

## start of the program - calling main method
main()
