import streamlit as st
import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyA4aTZ40rxQHzy7UoxRQOc5hFI5krz_U6o"

genai.configure(api_key=GOOGLE_API_KEY)
model=genai.GenerativeModel('gemini-pro')
def main():
    st.set_page_config(page_title="Text2SQL Generator", page_icon=":robot:")
    st.markdown(
        """
            <div style="text-align: center;">
                <h1> SQL Query Generator </h1>
                <h3> I can Generate SQL Queries for you!..</h3>
                <p> This Tool is a simple tool that allows you to generate SQL queries based in your prompts.</p>

            </div>
        """,

        unsafe_allow_html=True,
    )

    text_input=st.text_area("Enter your Query here in plain English: ")
    submit=st.button("Generate SQL Query")

    if submit:
        with st.spinner("Generating SQL Query..."):
            template="""
                Create a SQL query snippet using the below text:

                ```
                    {text_input}
                ```
                I just want a SQL Query.

                """
            formatted_template=template.format(text_input=text_input)

            response=model.generate_content(formatted_template)
            sql_query=response.text
            
            sql_query=sql_query.strip().lstrip("```sql").rstrip("```")

            expected_output="""
                what would be the expected response of this SQL query snippet:
                    ```
                    {sql_query}
                    ```
                provide sample tabular response with no explanation

                """
            expected_output_formatted=expected_output.format(sql_query=sql_query)
            expected_response=model.generate_content(expected_output_formatted)
            expected_response=expected_response.text

            query_explanation="""
                Explain this SQL query
                    ```
                    {sql_query}
                    ```
                Please provide the simplest of explanation

                """

            explanation_formatted=query_explanation.format(sql_query=sql_query)
            explanation_resposnse=model.generate_content(explanation_formatted)
            explanation_resposnse=explanation_resposnse.text

            with st.container():
                st.success("SQL Query Generated Successfully!.. Here is your Query Below: ")
                st.code(sql_query, language="sql")

                st.success("Expected Output of this SQL Query will be: ")
                st.markdown(expected_response)

                st.success("Explanation for the generated Query: ")
                st.markdown(explanation_resposnse)


main()