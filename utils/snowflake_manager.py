import snowflake.snowpark as snowpark
from snowflake.snowpark.functions import udf
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os

class SnowflakeManager:
    def __init__(self):
        self.session = snowpark.Session.builder.configs({
            "account": os.getenv("SNOWFLAKE_ACCOUNT"),
            "user": os.getenv("SNOWFLAKE_USER"),
            "password": os.getenv("SNOWFLAKE_PASSWORD"),
            "role": os.getenv("SNOWFLAKE_ROLE"),
            "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
            "database": os.getenv("SNOWFLAKE_DATABASE"),
            "schema": os.getenv("SNOWFLAKE_SCHEMA")
        }).create()
        
        self.mistral_client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    
    def query_documents(self, question):
        # Use Snowflake Cortex for vector search
        results = self.session.sql(f"""
            SELECT *,
                vector_similarity(
                    get_embedding('{question}'),
                    embedding
                ) as similarity
            FROM document_chunks
            ORDER BY similarity DESC
            LIMIT 5
        """).collect()
        
        # Format context for the LLM
        context = "\n\n".join([f"Document: {r['DOCUMENT_NAME']}\nContent: {r['TEXT']}" 
                              for r in results])
        
        # Generate answer using Mistral
        messages = [
            ChatMessage(role="system", content="You are a helpful assistant. Answer the question based on the provided context."),
            ChatMessage(role="user", content=f"Context:\n{context}\n\nQuestion: {question}")
        ]
        
        response = self.mistral_client.chat(
            model="mistral-large-2",
            messages=messages
        )
        
        # Return answer and contexts
        return (
            response.choices[0].message.content,
            [{'document_name': r['DOCUMENT_NAME'], 'text': r['TEXT']} for r in results]
        ) 