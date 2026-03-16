import os
import sqlite3
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class PeruAnalystAgent:
    def __init__(self):
        # Handle API Key from environment or Streamlit Secrets
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            try:
                import streamlit as st
                api_key = st.secrets.get("OPENAI_API_KEY")
            except Exception:
                api_key = None
        
        if not api_key:
            raise ValueError("OpenAI API Key not found. Please set OPENAI_API_KEY in your .env file or Streamlit Secrets dashboard.")
            
        self.client = OpenAI(api_key=api_key)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        db_path = os.path.join(base_dir, "data", "github_peru.db")
        self.conn = sqlite3.connect(db_path)
        
    def get_db_schema(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        schema = ""
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table[0]})")
            cols = cursor.fetchall()
            schema += f"Table: {table[0]}\nColumns: {[c[1] for c in cols]}\n\n"
        return schema

    def execute_query(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return str(results[:10]) # Limit to 10 results
        except Exception as e:
            return f"Error: {e}"

    def ask(self, question):
        print(f"Agent Reasoning for: '{question}'")
        
        system_prompt = f"""You are an expert GitHub data analyst for the Peruvian ecosystem. 
You have access to a SQLite database.
SCHEMA:
{self.get_db_schema()}

Your goal is to answer questions by generating and executing SQL queries.
You must return your answer in TWO parts:
1. REASONING: Explain your thought process.
2. ANSWER: The final answer based on the query results.

Be precise. If the question is about 'top' or 'most popular', use stars accordingly.
"""
        
        # Step 1: Generate SQL
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Generate ONLY the SQL query to answer this: {question}"}
            ],
            temperature=0
        )
        sql_query = response.choices[0].message.content.strip().replace("```sql", "").replace("```", "")
        print(f"  > Executing SQL: {sql_query}")
        
        # Step 2: Execute
        query_results = self.execute_query(sql_query)
        
        # Step 3: Final Answer
        final_response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Question: {question}\nQuery executed: {sql_query}\nResults: {query_results}\n\nProvide the final reasoning and answer."}
            ],
            temperature=0.3
        )
        
        print(f"  > Done.")
        return final_response.choices[0].message.content

if __name__ == "__main__":
    agent = PeruAnalystAgent()
    print(agent.ask("Who is the most influential developer in Lima based on followers and what is their main language?"))
