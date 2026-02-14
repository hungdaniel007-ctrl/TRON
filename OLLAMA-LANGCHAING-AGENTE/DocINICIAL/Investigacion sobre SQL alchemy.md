Building a Conversational SQL Agent with LangChain and FastAPI
Silversky Technology
Silversky Technology

Follow
11 min read
·
Sep 10, 2025
132

Press enter or click to view image in full size

Ever wanted to build a chatbot that can answer specialized questions directly from your database? We had this exact requirement in one of our projects.

Initially, we used standard LangChain with custom tool calling — creating separate functions for each database table and manually crafting SQL queries. The result? High latency, an unmaintainable codebase that grew exponentially with our database, and memory management nightmares.

The Problems We Faced:
Codebase exploded as new tables were added
Manual SQL generation slowed everything down and introduced errors
Memory management broke under longer conversations
Supporting new queries required heavy dev effort
Adding new features on top of the chatbot became difficult
Implementing context management (bot memory) was tedious and error-prone
Then we discovered LangChain’s SQL agent, and how PostgreSQL and LangChain can take care of most of our needs readily. In this tutorial, we’ll show you how to build the solution that reduced our codebase complexity by 70% while dramatically improving performance.

What We’ll Build
A complete conversational SQL agent using LangChain, OpenAI, and FastAPI that can handle queries from a book database, like:

“Show me all books by Stephen King”
“Which authors have written more than 3 books?”
“What’s the average rating of science fiction books?”
The system maintains conversation context, so follow-up questions work naturally — all without the maintenance headaches of our previous approach.

You can find all the code for this guide on our GitHub page: LangChain SQL Agent Demo (GitHub)

Prerequisites
Python 3.9+
PostgreSQL database
OpenAI API key
Basic knowledge of SQL and Python
Setup
First, install the required packages:

pip install fastapi uvicorn langchain-openai langchain-community sqlalchemy psycopg2-binary langchain-postgres
For our example, let’s assume we have a simple bookstore database with two tables:

-- Authors table
CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birth_year INTEGER,
    nationality VARCHAR(100)
);

-- Books table  
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author_id INTEGER REFERENCES authors(id),
    genre VARCHAR(100),
    publication_year INTEGER,
    rating DECIMAL(3,2)
);
Authors: stores basic author information like name, year of birth, and nationality.
Books: stores book details such as title, genre, publication year, and rating, with a foreign key linking back to the author.
Once you create these tables and insert some sample data, it helps to also define a view called books_with_authors. This view joins both tables into one unified dataset so that queries can be simplified. Instead of writing complex SQL joins every time, the agent can query the view directly to get books along with their authors.

CREATE VIEW books_with_authors AS
SELECT 
    b.id AS book_id,
    b.title,
    b.genre,
    b.publication_year,
    b.rating,
    a.name AS author_name,
    a.birth_year,
    a.nationality
FROM books b
JOIN authors a ON b.author_id = a.id;
Step 1: Basic SQL Agent
Now that the database is ready, we’ll set up a SQL agent powered by LangChain and OpenAI.

import os
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent, SQLDatabaseToolkit
from sqlalchemy import create_engine

# Setup

os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
DB_URI = "postgresql+psycopg2://username:password@localhost:5432/bookstore"

# Create database connection

engine = create_engine(DB_URI)

# Define custom table info for better LLM context

custom_table_info = {
    "authors": (
        "A table of authors.\n"
        "- id (SERIAL PRIMARY KEY): Unique ID of author\n"
        "- name (VARCHAR): Name of the author\n"
        "- birth_year (INTEGER): Year of birth\n"
        "- nationality (VARCHAR): Nationality of the author\n"
    ),
    "books": (
        "A table of books.\n"
        "- id (SERIAL PRIMARY KEY): Unique ID of book\n"
        "- title (VARCHAR): Title of the book\n"
        "- author_id (INTEGER): References authors(id)\n"
        "- genre (VARCHAR): Genre of the book\n"
        "- publication_year (INTEGER): Year of publication\n"
        "- rating (DECIMAL): Book rating (0–5)\n"
    ),
    "books_with_authors": (
        "A view combining books and authors.\n"
        "- book_id (INTEGER): ID of the book\n"
        "- title (VARCHAR): Title of the book\n"
        "- genre (VARCHAR): Genre of the book\n"
        "- publication_year (INTEGER): Year of publication\n"
        "- rating (DECIMAL): Rating of the book\n"
        "- author_name (VARCHAR): Name of the author\n"
        "- birth_year (INTEGER): Birth year of the author\n"
        "- nationality (VARCHAR): Nationality of the author\n"
    ),
}

# Initialize SQLDatabase with view support and custom info

db = SQLDatabase(
    engine=engine,
    include_tables=list(custom_table_info.keys()),
    custom_table_info=custom_table_info,
    view_support=True
)

# Initialize LLM

llm = ChatOpenAI(model="gpt-4", temperature=0)

# Create toolkit and agent

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent = create_sql_agent(
    toolkit=toolkit,
    llm=llm,
    agent_type="tool-calling",
    verbose=True
)

# Test it out

response = agent.invoke({"input": "List all books with their authors and ratings"})
print(response["output"])
Here’s what happens under the hood:

Natural Language to SQL — The agent takes a plain English question like “List all books with their authors and ratings.”
SQL Generation — It automatically generates the appropriate SQL query (for example, selecting from the books_with_authors view).
Execution — The query is run against the PostgreSQL database.
Readable Output — The agent then returns the result in a human-friendly format.
We also enhance the agent’s reasoning by providing custom table information. This metadata describes each table and the view in natural language, so the model has context about what fields mean without repeatedly inspecting the schema. For example, we specify that rating is a decimal between 0–5, or that author_id references the authors table.

By enabling view support, we tell the agent that views (like books_with_authors) should be treated as first-class citizens. This allows it to prefer querying the view instead of re-creating the join logic each time, which makes the queries cleaner and more reliable.

Get Silversky Technology’s stories in your inbox
Join Medium for free to get updates from this writer.

Enter your email
Subscribe
Console Output:

Press enter or click to view image in full size

Reply from the Agent
Step 2: Adding Callbacks for Raw Results
Sometimes you need access to the raw SQL results for additional processing. Let’s add a callback handler to capture this information:

from langchain.callbacks.base import BaseCallbackHandler

class SQLResultHandler(BaseCallbackHandler):
    """Callback handler to capture raw SQL query results"""

    def __init__(self):
        self.latest_sql_result = None
        self.sql_run_ids = set()
    
    def on_tool_start(self, serialized, input_str, **kwargs):
        """Track SQL tool starts"""
        tool_name = serialized.get('name', 'unknown') if isinstance(serialized, dict) else str(serialized)
        if tool_name == "sql_db_query":
            run_id = kwargs.get('run_id')
            self.sql_run_ids.add(run_id)
    
    def on_tool_end(self, output, **kwargs):
        """Capture SQL tool output"""
        run_id = kwargs.get('run_id')
        parent_run_id = kwargs.get('parent_run_id')
    
        # Check if this is a SQL tool end
        if run_id in self.sql_run_ids or parent_run_id in self.sql_run_ids:
            self.latest_sql_result = output
    
            # Clean up run IDs
            self.sql_run_ids.discard(run_id)
            self.sql_run_ids.discard(parent_run_id)
    
    def on_tool_error(self, error, **kwargs):
        """Clean up on SQL tool errors"""
        run_id = kwargs.get('run_id')
        self.sql_run_ids.discard(run_id)
    
    def get_latest_result(self):
        """Get the most recent SQL result"""
        return self.latest_sql_result
    
    def reset(self):
        """Reset for next query"""
        self.latest_sql_result = None
        self.sql_run_ids = set()

# Usage with callback

sql_handler = SQLResultHandler()

response = agent.invoke(
    {"input": "Show me all science fiction books"},
    {"callbacks": [sql_handler]}
)

print("Agent Response:", response["output"])
print("Raw SQL Result:", sql_handler.get_latest_result())
The callback system in LangChain allows you to hook into different stages of the agent’s execution. Our SQLResultHandler specifically captures the output from SQL database queries, giving us access to both the agent's natural language response and the raw data.

Step 3: Adding Conversation Memory
Now let’s add memory so our agent can handle follow-up questions and maintain context:

from langchain_postgres import PostgresChatMessageHistory
from langchain.memory import ConversationBufferMemory
import psycopg

# Connection for chat history (separate from main DB)

CHAT_HISTORY_DB = "postgresql://username:password@localhost:5432/bookstore"
CHAT_HISTORY_TABLE = "chat_history" #the table that will store our hisory
CHAT_HISTORY_CONN = psycopg.connect(CHAT_HISTORY_DB)
We also have to tell LangChain to create the table that will store the chat history. This will be done only once, you can comment out or remove the snippet later.

# Run this only once

try:
    PostgresChatMessageHistory.create_tables(CHAT_HISTORY_CONN, CHAT_HISTORY_TABLE)
    print(f"Chat history table '{CHAT_HISTORY_TABLE}' created or already exists")
except Exception as e:
    print(f"Note: {e}")
After that we fetch the conversation history and convert it into a readable format for the agent to understand easily. The PostgresChatMessageHistory requires the session_id to be a UUID string.

async def get_session_history(session_id: str) -> PostgresChatMessageHistory:
    """Get chat history for a session"""
    async_conn = await psycopg.AsyncConnection.connect(CHAT_HISTORY_CONN)
    return PostgresChatMessageHistory(
        CHAT_HISTORY_TABLE,
        session_id,
        async_connection=async_conn
    )

async def get_memory(session_id: str) -> ConversationBufferMemory:
    """Create memory with PostgreSQL backing"""
    chat_history = await get_session_history(session_id)
    return ConversationBufferMemory(
        chat_memory=chat_history,
        memory_key="history", 
        return_messages=True
    )

async def format_history(chat_history, max_messages: int = 6):
    """Format recent chat history for context"""
    messages = await chat_history.aget_messages()
    recent_messages = messages[-max_messages:] if len(messages) > max_messages else messages

    formatted = []
    for msg in recent_messages:
        role = "User" if msg.type == "human" else "Assistant"
        formatted.append(f"{role}: {msg.content}")
    
    return "\n".join(formatted)

async def create_agent_with_memory(session_id: str):
    """Create agent with conversation memory"""
    memory = await get_memory(session_id)

    # Get formatted history for context
    readable_history = await format_history(memory.chat_memory, 6)
    
    # Custom prompt with history
    custom_prefix = f"""
    You are a helpful assistant that can answer questions about a bookstore database.
    You have access to information about books and authors.
    
    Previous conversation context:
    {readable_history}
    
    Be concise and helpful in your responses.
    """
    
    return create_sql_agent(
        toolkit=toolkit,
        llm=llm,
        agent_type="tool-calling",
        prefix=custom_prefix,
        agent_executor_kwargs={"memory": memory},
        verbose=True
    )

# Usage with memory

import asyncio

async def chat_example():
    agent = await create_agent_with_memory("3dc035ae-bc72-4d5a-8569-c87c10aab97f") # Must be a UUID

    # First question
    response1 = await agent.ainvoke({"input": "How many books by Jane Austen do we have?"})
    print("Response 1:", response1["output"])
    
    # Follow-up question (will remember context)
    response2 = await agent.ainvoke({"input": "What genres are they?"})
    print("Response 2:", response2["output"])

# Run the example

asyncio.run(chat_example())
The memory system stores conversation history in PostgreSQL, allowing the agent to:

Remember previous questions and answers
Handle follow-up questions naturally
Maintain context across multiple interactions
Scale to multiple users/sessions with session IDs
Step 4: FastAPI Web Service
Finally, let’s wrap everything in a FastAPI application for easy deployment:

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="SQL Chat Agent", version="1.0.0")

class ChatRequest(BaseModel):
    message: str
    user_id: str

class ChatResponse(BaseModel):
    reply: str
    raw_sql_result: Optional[str] = None

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Chat with the SQL agent"""

    # Create handler for raw results
    sql_handler = SQLResultHandler()
    
    # Create agent with memory for this user
    agent = await create_agent_with_memory(request.user_id)
    
    # Process the question
    response = await agent.ainvoke(
        {"input": request.message},
        {"callbacks": [sql_handler]}
    )
    
    return ChatResponse(
        reply=response["output"],
        raw_sql_result=sql_handler.get_latest_result()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
Running the Application
Save your code to main.py and run:

uvicorn main:app --reload
Your API will be available at http://localhost:8000. You can test it with:

curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How many authors do we have?",
    "user_id": "3dc035ae-bc72-4d5a-8569-c87c10aab97f"
  }'
Note: The user_id field must always be a valid UUID, otherwise LangChain will throw us an error.

Testing Your Agent
Try these example queries:

“Show me all books published after 2020”
“Which author has the highest average book rating?”
“List science fiction books with ratings above 4.0”
“Who wrote ‘The Shining’?” (followed by “What other books did they write?”)
Complete Working Example
Here’s the full code putting it all together:

import os
import asyncio
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent, SQLDatabaseToolkit
from langchain_postgres import PostgresChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.base import BaseCallbackHandler
import psycopg

# Configuration

os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
DB_URI = "postgresql+psycopg2://username:password@localhost:5432/bookstore"
CHAT_HISTORY_CONN = "postgresql://username:password@localhost:5432/bookstore"
CHAT_HISTORY_TABLE = "chat_history"

# Database setup

engine = create_engine(DB_URI)

# Define custom table info for better LLM context

custom_table_info = {
    "authors": (
        "A table of authors.\n"
        "- id (SERIAL PRIMARY KEY): Unique ID of author\n"
        "- name (VARCHAR): Name of the author\n"
        "- birth_year (INTEGER): Year of birth\n"
        "- nationality (VARCHAR): Nationality of the author\n"
    ),
    "books": (
        "A table of books.\n"
        "- id (SERIAL PRIMARY KEY): Unique ID of book\n"
        "- title (VARCHAR): Title of the book\n"
        "- author_id (INTEGER): References authors(id)\n"
        "- genre (VARCHAR): Genre of the book\n"
        "- publication_year (INTEGER): Year of publication\n"
        "- rating (DECIMAL): Book rating (0–10)\n"
    ),
    "books_with_authors": (
        "A view combining books and authors.\n"
        "- book_id (INTEGER): ID of the book\n"
        "- title (VARCHAR): Title of the book\n"
        "- genre (VARCHAR): Genre of the book\n"
        "- publication_year (INTEGER): Year of publication\n"
        "- rating (DECIMAL): Rating of the book\n"
        "- author_name (VARCHAR): Name of the author\n"
        "- birth_year (INTEGER): Birth year of the author\n"
        "- nationality (VARCHAR): Nationality of the author\n"
    ),
}

# Initialize SQLDatabase with view support and custom info

db = SQLDatabase(
    engine=engine,
    include_tables=list(custom_table_info.keys()),
    custom_table_info=custom_table_info,
    view_support=True
)
llm = ChatOpenAI(model="gpt-4", temperature=0)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Basic Callback Handler

class SQLResultHandler(BaseCallbackHandler):
    def __init__(self):
        self.latest_sql_result = None
        self.sql_run_ids = set()

    def on_tool_start(self, serialized, input_str, **kwargs):
        tool_name = serialized.get('name', 'unknown') if isinstance(serialized, dict) else str(serialized)
        if tool_name == "sql_db_query":
            self.sql_run_ids.add(kwargs.get('run_id'))
    
    def on_tool_end(self, output, **kwargs):
        run_id = kwargs.get('run_id')
        if run_id in self.sql_run_ids:
            self.latest_sql_result = output
            self.sql_run_ids.discard(run_id)
    
    def get_latest_result(self):
        return self.latest_sql_result

# Memory Handling

async def get_session_history(session_id: str):
    async_conn = await psycopg.AsyncConnection.connect(CHAT_HISTORY_CONN)
    return PostgresChatMessageHistory(CHAT_HISTORY_TABLE, session_id, async_connection=async_conn)
async def get_memory(session_id: str):
    chat_history = await get_session_history(session_id)
    return ConversationBufferMemory(chat_memory=chat_history, memory_key="history", return_messages=True)

# Agent Creation

async def create_agent_with_memory(session_id: str):
    memory = await get_memory(session_id)
    return create_sql_agent(
        toolkit=toolkit,
        llm=llm,
        agent_type="tool-calling",
        agent_executor_kwargs={"memory": memory},
        verbose=True
    )

# FastAPI app

app = FastAPI(title="SQL Chat Agent")

# Models

class ChatRequest(BaseModel):
    message: str
    user_id: str
class ChatResponse(BaseModel):
    reply: str
    raw_sql_result: Optional[str] = None

# API Endpoint

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    sql_handler = SQLResultHandler()
    agent = await create_agent_with_memory(request.user_id)

    response = await agent.ainvoke(
        {"input": request.message},
        {"callbacks": [sql_handler]}
    )
    
    return ChatResponse(
        reply=response["output"],
        raw_sql_result=sql_handler.get_latest_result()
    )

# Execution

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
Example Request:

{
    "message": "List all books with their authors and ratings",
    "user_id": "44b11b50-9417-4fa5-8e5d-ea968c6dc7d1"
}
Agent Reply:

{
    "reply": "Here are some books with their authors and ratings:\n\n1. 'One Hundred Years of Solitude' by Gabriel García Márquez - Rating: 4.90\n2. '1984' by George Orwell - Rating: 4.80\n3. 'Pride and Prejudice' by Jane Austen - Rating: 4.70\n4. 'Animal Farm' by George Orwell - Rating: 4.60\n5. 'Half of a Yellow Sun' by Chimamanda Ngozi Adichie - Rating: 4.60\n6. 'Kafka on the Shore' by Haruki Murakami - Rating: 4.50\n7. 'Emma' by Jane Austen - Rating: 4.50\n8. 'Americanah' by Chimamanda Ngozi Adichie - Rating: 4.40\n9. 'Adventures of Huckleberry Finn' by Mark Twain - Rating: 4.40\n10. 'Norwegian Wood' by Haruki Murakami - Rating: 4.30",
    "raw_sql_result": "[('One Hundred Years of Solitude', 'Gabriel García Márquez', Decimal('4.90')), ('1984', 'George Orwell', Decimal('4.80')), ('Pride and Prejudice', 'Jane Austen', Decimal('4.70')), ('Animal Farm', 'George Orwell', Decimal('4.60')), ('Half of a Yellow Sun', 'Chimamanda Ngozi Adichie', Decimal('4.60')), ('Kafka on the Shore', 'Haruki Murakami', Decimal('4.50')), ('Emma', 'Jane Austen', Decimal('4.50')), ('Americanah', 'Chimamanda Ngozi Adichie', Decimal('4.40')), ('Adventures of Huckleberry Finn', 'Mark Twain', Decimal('4.40')), ('Norwegian Wood', 'Haruki Murakami', Decimal('4.30'))]"
}
Key Benefits
This approach gives you:

Natural Language Interface: Users can ask questions in plain English
Conversation Memory: Maintains context across multiple questions
Raw Data Access: Callbacks provide access to underlying SQL results, or literally anything else you want to do after agent call.
REST API: Easy integration with web apps, mobile apps, or other services
Scalable: Supports multiple concurrent users with session management
Working Example from GitHub
The complete working example is available in the GitHub repository:
👉 LangChain SQL Agent Demo (GitHub)

To run it locally:

git clone https://github.com/Silversky-Technology/langchain-sql-agent-guide.git
cd langchain-sql-agent-guide
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn langchain-openai langchain-community sqlalchemy psycopg2-binary langchain-postgres asyncio
uvicorn main:app --reload
Remember to add in your own API key and database credentials.

Your API will be available to test at http://localhost:8000!

Conclusion
You now have a complete conversational SQL agent that can handle complex database queries through natural language. The modular design makes it easy to extend with additional features like:

Rate limiting and authentication
Query result caching
Support for multiple databases
Custom response formatting
The combination of LangChain’s SQL agent capabilities with FastAPI’s modern web framework creates a powerful foundation for building intelligent database interfaces.

Full working example is available here: LangChain SQL Agent Demo (GitHub)

Have you built a conversational SQL agent or similar natural language database interface? We’d love to hear about your approach, challenges, and lessons learned. Drop your thoughts and experiences in the comments below!

Brought to you by Debakshi from the Silversky Technology crew.
Curious what else we’re building? Explore more at silverskytechnology.com.

Langchain
Agentic Ai
OpenAI
Artificial Intelligence
Python
132

Silversky Technology
Written by Silversky Technology
119 followers
·
11 following
Transforming Visionary Ideas into Cutting-Edge Solutions

Follow
No responses yet





---

# AnalyticDB integrations

Copy page

Integrate with AnalyticDB using LangChain Python.

> [AnalyticDB for PostgreSQL](https://www.alibabacloud.com/help/en/analyticdb-for-postgresql/latest/product-introduction-overview) is a massively parallel processing (MPP) data warehousing service from [Alibaba Cloud](https://www.alibabacloud.com/) that is designed to analyze large volumes of data online.

> `AnalyticDB for PostgreSQL` is developed based on the open-source `Greenplum Database` project and is enhanced with in-depth extensions by `Alibaba Cloud`. AnalyticDB for PostgreSQL is compatible with the ANSI SQL 2003 syntax and the PostgreSQL and Oracle database ecosystems. AnalyticDB for PostgreSQL also supports row store and column store. AnalyticDB for PostgreSQL processes petabytes of data offline at a high performance level and supports highly concurrent.

This page covers how to use the AnalyticDB ecosystem within LangChain.

## 

[​

](https://docs.langchain.com/oss/python/integrations/providers/analyticdb#installation-and-setup)

Installation and setup

You need to install the `sqlalchemy` python package.

pip

uv

```
pip install sqlalchemy
```

## 

[​

](https://docs.langchain.com/oss/python/integrations/providers/analyticdb#vectorstore)

VectorStore

See a [usage example](https://docs.langchain.com/oss/python/integrations/vectorstores/analyticdb).

```
from langchain_community.vectorstores import AnalyticDB
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/providers/analyticdb.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](https://docs.langchain.com/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

Yes

---

# How to connect MS-SQL with LANG-CHAIN #9848

Not planned

Not planned

[How to connect MS-SQL with LANG-CHAIN](https://github.com/langchain-ai/langchain/issues/9848#top)#9848

[![@AnasKhan-25](https://avatars.githubusercontent.com/u/110221695?v=4&size=80)](https://github.com/AnasKhan-25)

## Description

[AnasKhan-25](https://github.com/AnasKhan-25)

opened [on Aug 28, 2023](https://github.com/langchain-ai/langchain/issues/9848#issue-1869572223)

### Issue you'd like to raise.

db = SQLDatabase.from_uri(  
"mysql+pyodbc://Driver={SQL Server};Server=DESKTOP-17L7UI1\SQLEXPRESS;Database=DociQDb;rusted_Connection=yes;",)

I am trying to connect to my microsoft sql server but this give me error  
sqlalchemy.exc.DBAPIError: (pyodbc.Error) ('IM010', '[IM010] [Microsoft][ODBC Driver Manager] Data source name too long (0) (SQLDriverConnect)')

### Suggestion:

*No response*

## Activity

[![](https://avatars.githubusercontent.com/in/324583?s=64&v=4)dosubot](https://github.com/apps/dosubot)

added 

[bugRelated to a bug, vulnerability, unexpected error with an existing feature](https://github.com/langchain-ai/langchain/issues?q=state%3Aopen%20label%3A%22bug%22)

 [on Aug 28, 2023](https://github.com/langchain-ai/langchain/issues/9848#event-10208104735)

[![dosubot](https://avatars.githubusercontent.com/in/324583?v=4&size=80)](https://github.com/apps/dosubot)

### dosubot commented on Aug 28, 2023

[dosubot](https://github.com/apps/dosubot)bot

[on Aug 28, 2023](https://github.com/langchain-ai/langchain/issues/9848#issuecomment-1695537911)

*🤖*

Hello,

From the error message you provided, it seems like the issue is with the connection string you're using to connect to your MS-SQL database. The error message `Data source name too long` typically indicates that the connection string is not formatted correctly.

In your connection string, you're using the MySQL driver (`mysql+pyodbc://`) to connect to an MS-SQL database, which could be causing the issue. You should use the MS-SQL driver instead.

Here's an example of how your connection string should look:

```python
db = SQLDatabase.from_uri(
"mssql+pyodbc://username:password@DESKTOP-17L7UI1\SQLEXPRESS/DociQDb?driver=SQL+Server",)
```

Please replace `username` and `password` with your actual username and password for the SQL server.

Also, make sure that the SQL Server driver is installed on your machine. If it's not, you can download it from the official Microsoft website.

If you're still having issues after trying these steps, please provide more details about your setup (e.g., Python version, LangChain version, operating system) so I can assist you further.

Best regards,  
Dosu

## Sources

- [libs/experimental/langchain_experimental/sql/base.py](https://github.com/langchain-ai/langchain/blob/-/libs/experimental/langchain_experimental/sql/base.py)
- [libs/langchain/langchain/utilities/sql_database.py](https://github.com/langchain-ai/langchain/blob/-/libs/langchain/langchain/utilities/sql_database.py)

---

This response is meant to be useful and save you time. It is **not meant to be a precise solution**, but rather a starting point for your own research.

Help me be more useful! Please leave a 👍 if this is helpful and 👎 if it is irrelevant.

If you want to continue the conversation, start your reply with [@dosu-bot](https://github.com/dosu-bot).

[![AnasKhan-25](https://avatars.githubusercontent.com/u/110221695?v=4&size=80)](https://github.com/AnasKhan-25)

### AnasKhan-25 commented on Aug 29, 2023

[AnasKhan-25](https://github.com/AnasKhan-25)

[on Aug 29, 2023](https://github.com/langchain-ai/langchain/issues/9848#issuecomment-1697144185)

Author

> *🤖*
> 
> Hello,
> 
> From the error message you provided, it seems like the issue is with the connection string you're using to connect to your MS-SQL database. The error message `Data source name too long` typically indicates that the connection string is not formatted correctly.
> 
> In your connection string, you're using the MySQL driver (`mysql+pyodbc://`) to connect to an MS-SQL database, which could be causing the issue. You should use the MS-SQL driver instead.
> 
> Here's an example of how your connection string should look:
> 
> ```python
> db = SQLDatabase.from_uri(
> "mssql+pyodbc://username:password@DESKTOP-17L7UI1\SQLEXPRESS/DociQDb?driver=SQL+Server",)
> ```
> 
> Please replace `username` and `password` with your actual username and password for the SQL server.
> 
> Also, make sure that the SQL Server driver is installed on your machine. If it's not, you can download it from the official Microsoft website.
> 
> If you're still having issues after trying these steps, please provide more details about your setup (e.g., Python version, LangChain version, operating system) so I can assist you further.
> 
> Best regards, Dosu
> 
> ## Sources
> 
> - [libs/experimental/langchain_experimental/sql/base.py](https://github.com/langchain-ai/langchain/blob/-/libs/experimental/langchain_experimental/sql/base.py)
> - [libs/langchain/langchain/utilities/sql_database.py](https://github.com/langchain-ai/langchain/blob/-/libs/langchain/langchain/utilities/sql_database.py)
> 
> This response is meant to be useful and save you time. It is **not meant to be a precise solution**, but rather a starting point for your own research.
> 
> Help me be more useful! Please leave a 👍 if this is helpful and 👎 if it is irrelevant.
> 
> If you want to continue the conversation, start your reply with [@dosu-bot](https://github.com/dosu-bot).

db = SQLDatabase.from_uri(  
"mssql+pyodbc://user1:Aksiq@312@DESKTOP-17L7UI1\SQLEXPRESS/DociQDb?driver=SQL+Server",)

I have change the connection_string to your desire pattern  
but it show error  
sqlalchemy.exc.OperationalError: (pyodbc.OperationalError) ('08001', '[08001] [Microsoft][ODBC SQL Server Driver][DBNETLIB]SQL Server does not exist or access denied. (17) (SQLDriverConnect); [08001] [Microsoft][ODBC SQL Server Driver][DBNETLIB]ConnectionOpen (Connect()). (53)')

[![dosubot](https://avatars.githubusercontent.com/in/324583?v=4&size=80)](https://github.com/apps/dosubot)

### dosubot commented on Aug 29, 2023

[dosubot](https://github.com/apps/dosubot)bot

[on Aug 29, 2023](https://github.com/langchain-ai/langchain/issues/9848#issuecomment-1697156149)

*🤖*

Hello,

Based on the error message you're receiving, it seems like there might be an issue with the connection string you're using to connect to your Microsoft SQL Server database. The error message `sqlalchemy.exc.DBAPIError: (pyodbc.Error) ('IM010', '[IM010] [Microsoft][ODBC Driver Manager] Data source name too long (0) (SQLDriverConnect)')` typically indicates that the Data Source Name (DSN) specified in the connection string is too long.

From the code you've shared, it appears that you're using the MySQL driver (`mysql+pyodbc`) in your connection string. However, you should be using the MS-SQL driver (`mssql+pyodbc`) instead, as you've been advised.

Here's how your connection string should look:

```python
db = SQLDatabase.from_uri(
"mssql+pyodbc://username:password@DESKTOP-17L7UI1\SQLEXPRESS/DociQDb?driver=SQL+Server",)
```

Please replace `username` and `password` with your actual username and password for the SQL server.

If you continue to encounter issues after trying these steps, please provide more details about your setup, such as your Python version, LangChain version, and operating system. This will help us better understand your issue and provide more targeted assistance.

As for your question, yes, the LangChain framework does support connections to Microsoft SQL Server databases. This is because LangChain uses SQLAlchemy as its database toolkit, which supports a variety of SQL databases, including Microsoft SQL Server. The `SQLDatabase` class in LangChain has a method `from_uri` which accepts a database URI and constructs a SQLAlchemy engine from it. This engine can be used to connect to any SQL database that SQLAlchemy supports, including Microsoft SQL Server.

I hope this helps! Let me know if you have any other questions.

## Sources

- [libs/langchain/langchain/utilities/sql_database.py](https://github.com/langchain-ai/langchain/blob/-/libs/langchain/langchain/utilities/sql_database.py)

---

This response is meant to be useful and save you time. It is **not meant to be a precise solution**, but rather a starting point for your own research.

Help me be more useful! Please leave a 👍 if this is helpful and 👎 if it is irrelevant.

If you want to continue the conversation, start your reply with [@dosu-bot](https://github.com/dosu-bot).

[![AnasKhan-25](https://avatars.githubusercontent.com/u/110221695?v=4&size=80)](https://github.com/AnasKhan-25)

### AnasKhan-25 commented on Aug 29, 2023

[AnasKhan-25](https://github.com/AnasKhan-25)

[on Aug 29, 2023](https://github.com/langchain-ai/langchain/issues/9848#issuecomment-1697161940)

Author

> *🤖*
> 
> Hello,
> 
> Based on the error message you're receiving, it seems like there might be an issue with the connection string you're using to connect to your Microsoft SQL Server database. The error message `sqlalchemy.exc.DBAPIError: (pyodbc.Error) ('IM010', '[IM010] [Microsoft][ODBC Driver Manager] Data source name too long (0) (SQLDriverConnect)')` typically indicates that the Data Source Name (DSN) specified in the connection string is too long.
> 
> From the code you've shared, it appears that you're using the MySQL driver (`mysql+pyodbc`) in your connection string. However, you should be using the MS-SQL driver (`mssql+pyodbc`) instead, as you've been advised.
> 
> Here's how your connection string should look:
> 
> ```python
> db = SQLDatabase.from_uri(
> "mssql+pyodbc://username:password@DESKTOP-17L7UI1\SQLEXPRESS/DociQDb?driver=SQL+Server",)
> ```
> 
> Please replace `username` and `password` with your actual username and password for the SQL server.
> 
> If you continue to encounter issues after trying these steps, please provide more details about your setup, such as your Python version, LangChain version, and operating system. This will help us better understand your issue and provide more targeted assistance.
> 
> As for your question, yes, the LangChain framework does support connections to Microsoft SQL Server databases. This is because LangChain uses SQLAlchemy as its database toolkit, which supports a variety of SQL databases, including Microsoft SQL Server. The `SQLDatabase` class in LangChain has a method `from_uri` which accepts a database URI and constructs a SQLAlchemy engine from it. This engine can be used to connect to any SQL database that SQLAlchemy supports, including Microsoft SQL Server.
> 
> I hope this helps! Let me know if you have any other questions.
> 
> ## Sources
> 
> - [libs/langchain/langchain/utilities/sql_database.py](https://github.com/langchain-ai/langchain/blob/-/libs/langchain/langchain/utilities/sql_database.py)
> 
> This response is meant to be useful and save you time. It is **not meant to be a precise solution**, but rather a starting point for your own research.
> 
> Help me be more useful! Please leave a 👍 if this is helpful and 👎 if it is irrelevant.
> 
> If you want to continue the conversation, start your reply with [@dosu-bot](https://github.com/dosu-bot).

[@dosu-bot](https://github.com/dosu-bot)  
db = SQLDatabase.from_uri(  
"mssql+pyodbc://user1:Aksiq@312@DESKTOP-17L7UI1\SQLEXPRESS/DociQDb?driver=SQL+Server",)

I have change the connection_string to your desire pattern  
but it show error  
sqlalchemy.exc.OperationalError: (pyodbc.OperationalError) ('08001', '[08001] [Microsoft][ODBC SQL Server Driver][DBNETLIB]SQL Server does not exist or access denied. (17) (SQLDriverConnect); [08001] [Microsoft][ODBC SQL Server Driver][DBNETLIB]ConnectionOpen (Connect()). (53)')

[![dosubot](https://avatars.githubusercontent.com/in/324583?v=4&size=80)](https://github.com/apps/dosubot)

### dosubot commented on Aug 29, 2023

[dosubot](https://github.com/apps/dosubot)bot

[on Aug 29, 2023](https://github.com/langchain-ai/langchain/issues/9848#issuecomment-1697173048)

*🤖*

Hello,

Thank you for reaching out and providing detailed information about your issue. The error you're encountering is indeed related to the connection string you're using to connect to your Microsoft SQL Server database.

The connection string you're currently using seems to be incorrectly formatted. You're using the MySQL driver (`mysql+pyodbc`) in your connection string, but you should be using the MS-SQL driver (`mssql+pyodbc`) as you've been advised.

Here's the corrected connection string:

```python
db = SQLDatabase.from_uri(
"mssql+pyodbc://username:password@DESKTOP-17L7UI1\SQLEXPRESS/DociQDb?driver=SQL+Server",)
```

Please replace `username` and `password` with your actual username and password for the SQL server.

If you continue to encounter issues after trying these steps, please provide more details about your setup, such as your Python version, LangChain version, and operating system.

As you correctly mentioned, the LangChain framework does support connections to Microsoft SQL Server databases because it uses SQLAlchemy as its database toolkit. The `SQLDatabase` class in LangChain has a method `from_uri` which accepts a database URI and constructs a SQLAlchemy engine from it. This engine can be used to connect to any SQL database that SQLAlchemy supports, including Microsoft SQL Server.

I hope this helps! If you have any other questions or need further clarification, please don't hesitate to ask.

Best,  
Dosu

## Sources

- [libs/langchain/langchain/utilities/sql_database.py](https://github.com/langchain-ai/langchain/blob/-/libs/langchain/langchain/utilities/sql_database.py)

---

This response is meant to be useful and save you time. It is **not meant to be a precise solution**, but rather a starting point for your own research.

Help me be more useful! Please leave a 👍 if this is helpful and 👎 if it is irrelevant.

If you want to continue the conversation, start your reply with [@dosu-bot](https://github.com/dosu-bot).

[![AnasKhan-25](https://avatars.githubusercontent.com/u/110221695?v=4&size=80)](https://github.com/AnasKhan-25)

### AnasKhan-25 commented on Aug 29, 2023

[AnasKhan-25](https://github.com/AnasKhan-25)

[on Aug 29, 2023](https://github.com/langchain-ai/langchain/issues/9848#issuecomment-1697259191)

Author

[@dosu-bot](https://github.com/dosu-bot)  
The above exception was the direct cause of the following exception:

Traceback (most recent call last):  
File "D:\OmniExtract\src\api\Cheque\chatTest.py", line 31, in  
db = SQLDatabase.from_uri(  
File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\langchain\utilities\sql_database.py", line 124, in from_uri  
return cls(create_engine(database_uri, **_engine_args), **kwargs)  
File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\langchain\utilities\sql_database.py", line 65, in **init**  
self._inspector.get_table_names(schema=schema)  
File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\engine\reflection.py", line 397, in get_table_names  
return self.dialect.get_table_names(  
File "", line 2, in get_table_names  
File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\engine\reflection.py", line 97, in cache  
ret = fn(self, con, *args, **kw)  
File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\dialects\mssql\base.py", line 2827, in wrap  
return _switch_db(  
File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\dialects\mssql\base.py", line 2869, in _switch_db  
return fn(*arg, **kw)  
File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\dialects\mssql\base.py", line 3306, in get_table_names  
table_names = [r[0] for r in connection.execute(s)]  
File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\engine\base.py", line 1414, in execute  
return meth(  
File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\sql\elements.py", line 486, in _execute_on_connection  
return connection._execute_clauseelement(  
File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\engine\base.py", line 1638, in _execute_clauseelement  
ret = self._execute_context(  
File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\engine\base.py", line 1842, in _execute_context  
return self._exec_single_context(  
File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\engine\base.py", line 1983, in _exec_single_context  
self._handle_dbapi_exception(  
File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\engine\base.py", line 2326, in _handle_dbapi_exception  
raise sqlalchemy_exception.with_traceback(exc_info[2]) from e  
File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\engine\base.py", line 1964, in _exec_single_context  
self.dialect.do_execute(  
File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\engine\default.py", line 748, in do_execute  
cursor.execute(statement, parameters)  
sqlalchemy.exc.DBAPIError: (pyodbc.Error) ('HY104', '[HY104] [Microsoft][ODBC SQL Server Driver]Invalid precision value (0) (SQLBindParameter)')  
[SQL: SELECT [INFORMATION_SCHEMA].[TABLES].[TABLE_NAME]  
FROM [INFORMATION_SCHEMA].[TABLES]  
WHERE [INFORMATION_SCHEMA].[TABLES].[TABLE_SCHEMA] = CAST(? AS NVARCHAR(max)) AND [INFORMATION_SCHEMA].[TABLES].[TABLE_TYPE] = CAST(? AS NVARCHAR(max)) ORDER BY [INFORMATION_SCHEMA].[TABLES].[TABLE_NAME]]  
[parameters: ('dbo', 'BASE TABLE')]

[![dosubot](https://avatars.githubusercontent.com/in/324583?v=4&size=80)](https://github.com/apps/dosubot)

### dosubot commented on Aug 29, 2023

[dosubot](https://github.com/apps/dosubot)bot

[on Aug 29, 2023](https://github.com/langchain-ai/langchain/issues/9848#issuecomment-1697270615)

*🤖*

Hello,

The error you're encountering is a common issue when using pyodbc with Microsoft SQL Server. It usually occurs when you're trying to insert or update a decimal value with a precision of 0 into the database.

LangChain uses SQLAlchemy to interact with databases, and SQLAlchemy, in turn, uses DBAPI (Database API), such as pyodbc, to connect to various databases including Microsoft SQL Server.

To fix this issue, you need to ensure that the decimal values you're trying to insert or update in the database have a precision greater than 0. If you're using a model to interact with your database, make sure the precision of the decimal column is set properly.

Unfortunately, without more specific information about your database schema or the data you're trying to insert or update, I can't provide a more detailed solution. Please check your data and your database schema to ensure they're compatible.

As for your second question, I wasn't able to find any specific requirements or limitations within the LangChain framework when connecting to a Microsoft SQL Server database in the repository. However, LangChain uses SQLAlchemy for database interactions, so any limitations or requirements would likely be the same as those for SQLAlchemy.

If you continue to encounter issues, please provide more information about your database schema and the data you're trying to insert or update, and I'll do my best to assist you further.

Best,  
Dosu

## Sources

- [libs/langchain/langchain/utilities/sql_database.py](https://github.com/langchain-ai/langchain/blob/-/libs/langchain/langchain/utilities/sql_database.py)

---

This response is meant to be useful and save you time. It is **not meant to be a precise solution**, but rather a starting point for your own research.

Help me be more useful! Please leave a 👍 if this is helpful and 👎 if it is irrelevant.

If you want to continue the conversation, start your reply with [@dosu-bot](https://github.com/dosu-bot).

[![dosubot](https://avatars.githubusercontent.com/in/324583?v=4&size=80)](https://github.com/apps/dosubot)

### dosubot commented on Nov 28, 2023

[dosubot](https://github.com/apps/dosubot)bot

[on Nov 28, 2023](https://github.com/langchain-ai/langchain/issues/9848#issuecomment-1830158487) – with [DosuBot](https://dosu.dev/)

Hi, [@AnasKhan-25](https://github.com/AnasKhan-25)! I'm Dosu, and I'm here to help the LangChain team manage our backlog. I wanted to let you know that we are marking this issue as stale.

Based on the information provided, it seems that you were experiencing an issue when trying to connect MS-SQL with LANG-CHAIN. Initially, you were getting an error message "Data source name too long". In response, I suggested that the issue might be with the connection string and advised you to use the MS-SQL driver instead of the MySQL driver. You mentioned that you tried the suggested solution but encountered a new error message. I then suggested that the new error might be related to the precision of decimal values being inserted or updated in the database and advised you to check your data and database schema.

Before we proceed, we would like to confirm if this issue is still relevant to the latest version of the LangChain repository. If it is, please let us know by commenting on this issue. Otherwise, feel free to close the issue yourself, or the issue will be automatically closed in 7 days.

Thank you for your understanding, and we look forward to hearing from you soon!

Best regards,  
[Dosu](https://dosu.dev/)

[![](https://avatars.githubusercontent.com/in/324583?s=64&v=4)dosubot](https://github.com/apps/dosubot)

added 

[stale](https://github.com/langchain-ai/langchain/issues?q=state%3Aopen%20label%3A%22stale%22)

 [on Nov 28, 2023](https://github.com/langchain-ai/langchain/issues/9848#event-11085676043)

[![](https://avatars.githubusercontent.com/in/324583?s=64&v=4)dosubot](https://github.com/apps/dosubot)

closed this as [not planned](https://github.com/langchain-ai/langchain/issues?q=is%3Aissue%20state%3Aclosed%20archived%3Afalse%20reason%3Anot-planned)[on Dec 6, 2023](https://github.com/langchain-ai/langchain/issues/9848#event-11171699380)

[![](https://avatars.githubusercontent.com/in/324583?s=64&v=4)dosubot](https://github.com/apps/dosubot)

removed 

[stale](https://github.com/langchain-ai/langchain/issues?q=state%3Aopen%20label%3A%22stale%22)

 [on Dec 6, 2023](https://github.com/langchain-ai/langchain/issues/9848#event-11171699472)

[![imsunnykr](https://avatars.githubusercontent.com/u/54575021?u=db8bf5e0ac636e62ab9e36ec1ee3de0d8aef0c05&v=4&size=80)](https://github.com/imsunnykr)

### imsunnykr commented on Jan 18, 2024

[imsunnykr](https://github.com/imsunnykr)

[on Jan 18, 2024](https://github.com/langchain-ai/langchain/issues/9848#issuecomment-1898510917)

> [@dosu-bot](https://github.com/dosu-bot) The above exception was the direct cause of the following exception:
> 
> Traceback (most recent call last): File "D:\OmniExtract\src\api\Cheque\chatTest.py", line 31, in db = SQLDatabase.from_uri( File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\langchain\utilities\sql_database.py", line 124, in from_uri return cls(create_engine(database_uri, **_engine_args), **kwargs) File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\langchain\utilities\sql_database.py", line 65, in **init** self._inspector.get_table_names(schema=schema) File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\engine\reflection.py", line 397, in get_table_names return self.dialect.get_table_names( File "", line 2, in get_table_names File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\engine\reflection.py", line 97, in cache ret = fn(self, con, *args, **kw) File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\dialects\mssql\base.py", line 2827, in wrap return _switch_db( File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\dialects\mssql\base.py", line 2869, in _switch_db return fn(*arg, **kw) File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\dialects\mssql\base.py", line 3306, in get_table_names table_names = [r[0] for r in connection.execute(s)] File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\engine\base.py", line 1414, in execute return meth( File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\sql\elements.py", line 486, in _execute_on_connection return connection._execute_clauseelement( File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\engine\base.py", line 1638, in _execute_clauseelement ret = self._execute_context( File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\engine\base.py", line 1842, in _execute_context return self._exec_single_context( File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\engine\base.py", line 1983, in _exec_single_context self._handle_dbapi_exception( File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\engine\base.py", line 2326, in _handle_dbapi_exception raise sqlalchemy_exception.with_traceback(exc_info[2]) from e File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\engine\base.py", line 1964, in _exec_single_context self.dialect.do_execute( File "C:\Users\dell\PycharmProjects\TravelIQ-Backend-test_environment\TravelIQ_update\OmniExtract\lib\site-packages\sqlalchemy\engine\default.py", line 748, in do_execute cursor.execute(statement, parameters) sqlalchemy.exc.DBAPIError: (pyodbc.Error) ('HY104', '[HY104] [Microsoft][ODBC SQL Server Driver]Invalid precision value (0) (SQLBindParameter)') [SQL: SELECT [INFORMATION_SCHEMA].[TABLES].[TABLE_NAME] FROM [INFORMATION_SCHEMA].[TABLES] WHERE [INFORMATION_SCHEMA].[TABLES].[TABLE_SCHEMA] = CAST(? AS NVARCHAR(max)) AND [INFORMATION_SCHEMA].[TABLES].[TABLE_TYPE] = CAST(? AS NVARCHAR(max)) ORDER BY [INFORMATION_SCHEMA].[TABLES].[TABLE_NAME]] [parameters: ('dbo', 'BASE TABLE')]

You can change the drive name with ODBC+Driver+17+for+SQL+Server in place of SQL+Server , this may solve your issue

Example below

db = SQLDatabase.from_uri(  
"mssql+pyodbc://username:password@DESKTOP-17L7UI1\SQLEXPRESS/DociQDb?driver=ODBC+Driver+17+for+SQL+Server")

[![satish-goml](https://avatars.githubusercontent.com/u/137066809?v=4&size=80)](https://github.com/satish-goml)

### satish-goml commented on Feb 9, 2024

[satish-goml](https://github.com/satish-goml)

[on Feb 9, 2024](https://github.com/langchain-ai/langchain/issues/9848#issuecomment-1935352460)

> Hi, [@AnasKhan-25](https://github.com/AnasKhan-25)! I'm Dosu, and I'm here to help the LangChain team manage our backlog. I wanted to let you know that we are marking this issue as stale.
> 
> Based on the information provided, it seems that you were experiencing an issue when trying to connect MS-SQL with LANG-CHAIN. Initially, you were getting an error message "Data source name too long". In response, I suggested that the issue might be with the connection string and advised you to use the MS-SQL driver instead of the MySQL driver. You mentioned that you tried the suggested solution but encountered a new error message. I then suggested that the new error might be related to the precision of decimal values being inserted or updated in the database and advised you to check your data and database schema.
> 
> Before we proceed, we would like to confirm if this issue is still relevant to the latest version of the LangChain repository. If it is, please let us know by commenting on this issue. Otherwise, feel free to close the issue yourself, or the issue will be automatically closed in 7 days.
> 
> Thank you for your understanding, and we look forward to hearing from you soon!
> 
> Best regards, [Dosu](https://dosu.dev/)

db = SQLDatabase.from_uri(f'mssql+pyodbc://username:[password@mis-db.crg4umutboef.ap-south-1.rds.amazonaws.com](mailto:password@mis-db.crg4umutboef.ap-south-1.rds.amazonaws.com)/EssTee?driver=ODBC+Driver+17+for+SQL+Server')  
the code is keep on running it is not connection

[![shivamsh314](https://avatars.githubusercontent.com/u/149043223?v=4&size=80)](https://github.com/shivamsh314)

### shivamsh314 commented on Mar 31, 2024

[shivamsh314](https://github.com/shivamsh314)

[on Mar 31, 2024](https://github.com/langchain-ai/langchain/issues/9848#issuecomment-2028848607)

was anyone able to resolve this issue?

[![gobielum](https://avatars.githubusercontent.com/u/158308301?v=4&size=80)](https://github.com/gobielum)

### gobielum commented on Aug 23, 2024

[gobielum](https://github.com/gobielum)

[on Aug 23, 2024](https://github.com/langchain-ai/langchain/issues/9848#issuecomment-2306560929)

[@AnasKhan-25](https://github.com/AnasKhan-25), in reply to your first question. I did this to resolve the issue:

import langchain  
import pyodbc  
from langchain.agents import create_sql_agent  
from langchain.agents.agent_toolkits import SQLDatabaseToolkit  
from langchain.agents.agent_types import AgentType  
from langchain.chains.sql_database.query import create_sql_query_chain  
from langchain.chat_models import ChatOpenAI  
from langchain.llms.openai import OpenAI  
from langchain.sql_database import SQLDatabase  
from langchain.utilities import SQLDatabase  
from sqlalchemy import create_engine  
from sqlalchemy.engine import URL

server= 'xxxxxxx'  
database='xxxxxxxx'  
user='xxxxxx'  
password='xxxxxxx'  
my_odbc_driver = "ODBC Driver 17 for SQL Server" #check your odbc driver for the correct version

connection_url = URL.create(  
"mssql+pyodbc",  
username=user,  
password=password,  
host=server,  
database=database,  
query={"driver": my_odbc_driver},  
)

connection_string= (connection_url)  
engine_args = {"echo": False} # Optional engine arguments  
db = SQLDatabase.from_uri(connection_string, engine_args)

---

# How do you use LangChain to build a Text-to-SQL solution? What are the challenges? How to solve it?

In this post, using LangChain as an example of how you could use it to implement text-to-SQL, encounter challenges and how you can solve…

![How do you use LangChain to build a Text-to-SQL solution? What are the challenges? How to solve it?](https://capable-butterfly-84cab64826.media.strapiapp.com/blog_post_How_do_you_use_Lang_Chain_to_build_a_Text_to_SQL_solution_31434fc0e4.png)

Retrieval-augmented generation (RAG) has opened up a new opportunity for LLMs to leverage their capability to comprehend users’ intentions to search internal database knowledge for SQL generation.

LLM frameworks such as [LangChain](https://python.langchain.com/docs/use_cases/sql/quickstart/) and [LlamaIndex](https://docs.llamaindex.ai/en/stable/examples/index_structs/struct_indices/SQLIndexDemo/) provide tutorials to help developers implement text-to-SQL on their data sources. However, when these frameworks are deployed in production, users quickly find it challenging to implement the necessary features.

In this post, I’ll give a brief walkthrough using LangChain as an example of how you could use it to implement text-to-SQL. We will break down the challenges you will encounter and provide a solution to solve them.

# How to do Text-to-SQL in LangChain?

*This is based on the tutorial from* [*LangChain's official documentation*](https://python.langchain.com/docs/use_cases/sql/quickstart/)![0_ZEXns-otbKH3wS8B.webp](https://capable-butterfly-84cab64826.media.strapiapp.com/0_ZE_Xns_otb_KH_3w_S8_B_150742f451.webp)

Image from [LangChain Tutorial](https://python.langchain.com/docs/use_cases/sql/quickstart/)

Here’s a high-level concept of building a text-to-SQL solution in LangChain; check [the full tutorial here](https://python.langchain.com/docs/use_cases/sql/quickstart/).

Here’s how it works

*First, when users ask a business question, LLM will comprehend the question and generate SQL based on DDL that comes along with the prompt with the business question; usually, if you want to enhance the semantics understanding, you will also attach semantics with the prompt.*

First, install LangChain-related libraries

PYTHONCopy

`%pip install --upgrade --quiet langchain langchain-community langchain-openai`

Next import `SQLDatabase` from `langchain-community` , `SQLDatabase` is an `SQLAlchemy` wrapper around a database, which provides a SQL Toolkit on top of databases.

PYTHONCopy

`from langchain_community.utilities import SQLDatabase from langchain.chains import create_sql_query_chain from langchain_openai import ChatOpenAI db = SQLDatabase.from_uri("sqlite:///Chinook.db") llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)`

Use `create_sql_query_chain` to generate different dialects of SQL languages.

PYTHONCopy

`chain = create_sql_query_chain(llm, db) response = chain.invoke({"question": "How many employees are there"})`

Here’s an example of how the [prompt looks like](https://api.python.langchain.com/en/latest/chains/langchain.chains.sql_database.query.create_sql_query_chain.html):

PYTHONCopy

`from langchain_core.prompts import PromptTemplate template = '''Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer. Use the following format: Question: "Question here" SQLQuery: "SQL Query to run" SQLResult: "Result of the SQLQuery" Answer: "Final answer here" Only use the following tables: {table_info}. Question: {input}''' prompt = PromptTemplate.from_template(template)`

Here, we see we are asking LLMs to generate SQL based on a string template `{dialect}` ; the underlying mechanism is to insert the current dialect into the prompt and rely on LLMs to generate SQL dialects.

For `{table_info}` , you will need to insert all the table DDLs you want LLM to understand. What if you have many tables? We can’t dump the full information about our database in every prompt. LangChain's official tutorial suggests the following.

Simplify our model’s job by grouping the tables together.

PYTHONCopy

`system = """Return the names of the SQL tables that are relevant to the user question. \ The tables are: Music Business""" category_chain = create_extraction_chain_pydantic(Table, llm, system_message=system) category_chain.invoke({"input": "What are all the genres of Alanis Morisette songs"})`

You can group tables by categories:

PYTHONCopy

`from typing import List def get_tables(categories: List[Table]) -> List[str]: tables = [] for category in categories: if category.name == "Music": tables.extend( [ "Album", "Artist", "Genre", "MediaType", "Playlist", "PlaylistTrack", "Track", ] ) elif category.name == "Business": tables.extend(["Customer", "Employee", "Invoice", "InvoiceLine"]) return tables table_chain = category_chain | get_tables # noqa table_chain.invoke({"input": "What are all the genres of Alanis Morisette songs"})`

Another common way is to store table schema in a vector database and perform a semantic search to retrieve relevant DDLs from certain business inquiries. However, many challenges remain when moving to production.

# Challenges for LangChain building Text-to-SQL

Building a text-to-SQL tool using LangChain appears simple, but there are common challenges that arise when integrating it with production use cases. As listed below.

## How do storing and defining business semantics in text-to-SQL retrieval work?

The problem with using text-to-SQL solely based on data schema is that when users ask business questions through the chat interface, they usually speak in business languages, not data structure definitions such as table names, column names, etc.

![1_Onfgzu0Y5dh1jtQYIMC6Bg.webp](https://capable-butterfly-84cab64826.media.strapiapp.com/1_Onfgzu0_Y5dh1jt_QYIMC_6_Bg_5c5bdb878b.webp)

Image from [cube.dev blog](https://cube.dev/blog/semantic-layer-the-backbone-of-ai-powered-data-experiences)

When asking through AI, you might use your business terminologies and definitions, as well as relationships that are defined within your company, so you need to consider not only data structure but also semantics.

## How do we optimize table schema and semantics stored in a vector database?

In the tutorial in [LangChain](https://python.langchain.com/docs/use_cases/sql/large_db/), demonstrate putting all your table schema into the prompt. When you connect to production databases, the tables easily scale to thousands and tens of thousands of tables in a database.

You can’t fit all the tables into a prompt, so you need to embed the table and metadata from the metadata store into a vector database. When users ask a question, you can use semantic search in a vector database to retrieve the most relevant vectors from the vector database.

The process described above mostly operates offline, doing vector index creation. Pinterest has shared how they deal with the problem in their recent post about how they [internally build text-to-SQL](https://medium.com/pinterest-engineering/how-we-built-text-to-sql-at-pinterest-30bad30dabff).

![0_zu30nEo84noJWHGm.webp](https://capable-butterfly-84cab64826.media.strapiapp.com/0_zu30n_Eo84no_JWH_Gm_f0f1dc4f76.webp)

Image from “[**How we build text-to-sql at Pinterest**](https://medium.com/pinterest-engineering/how-we-built-text-to-sql-at-pinterest-30bad30dabff)**”**

## Inconsistent data retrieval performance

Different databases need to speak in different dialects; LangChain’s Text-to-SQL tutorial relies on a popular Python library called `SQLAlchemy` , under the hood `SQLAlchemy` provides a standard toolkit and ORM for users to talk to different databases, but LLMs still need to generate certain dialects for different databases.

At first glance, using this pattern sounds reasonable and could easily provide LLM capability to many databases through `SQLAlchemy`.

When moving to production, using the same SQL syntax with predefined aggregations and calculations is important for better and consistent retrieval performance across data sources.

# How can we solve it? Wren AI comes to the rescue!

I list above some obvious challenges to building a production-ready text-to-SQL solution. This is why our team builds [Wren AI, the open-source AI data assistant for your databases](https://github.com/Canner/WrenAI). You can set up an AI agent internally for your text-to-SQL tasks within a few minutes.

## Automation across metadata and semantics

Using [Wren AI](https://github.com/Canner/WrenAI), we automate all the metadata and semantics and help LLMs learn how semantics work in their businesses without you writing any code. with your user-friendly interface, you can model your data schema and add business semantics to the modeling layer. We will automatically complete all the offline Vector Index creation for you.

![1_mMCHgSTpfOF9ojagyQvbaQ.webp](https://capable-butterfly-84cab64826.media.strapiapp.com/1_m_MC_Hg_S_Tpf_OF_9ojagy_Qvba_Q_99111a45a1.webp)

Automation across UI, AI service, and semantic engine

## Optimize semantic search and prompt engineering.

Mapping table schema with semantics and ensuring you can get the right information through prompt and semantics requires a lot of fine-tuning; with Wren AI, we handle all the optimization and ensure it can search for the most relevant result when users ask business questions.

![1_vanTS8ITKJ7IZgiHljibkg.webp](https://capable-butterfly-84cab64826.media.strapiapp.com/1_van_TS_8_ITKJ_7_I_Zgi_Hljibkg_2d90dff55a.webp)

Wren AI optimizes retrieval and prompts out-of-the-box

## Consistent SQL syntax across multiple sources

Underlying [Wren AI](https://github.com/Canner/WrenAI), we developed a semantic engine called [Wren Engine](https://github.com/Canner/wren-engine), which is also [open-sourced](https://github.com/Canner/wren-engine). The engine can transpile from Standard ANSI SQL into different SQL dialects and provides the semantic encapsulate ability to define aggregations and calculations in the semantic modeling layer.![1_fZZHuzudk4vDBGZukeAkzw.webp](https://capable-butterfly-84cab64826.media.strapiapp.com/1_f_ZZ_Huzudk4v_DBG_Zuke_Akzw_c4ff29b3e0.webp)

Wren Engine Architecture

## Feedback loop design

The feedback loop is one of the most important designs for AI agents. We want our agent to learn from our history and also teach the agent to perform better in future tasks; this is where the feedback loop comes in.

We built in a Wren AI feedback loop in the user interface, so when you ask a question and get the answer from Wren AI, you can **provide adjustments** to the agent, will learn from your inputs, regenerate the result, and store the learning in the semantic modeling definition, so it will generate the right outcome when users ask the next time.

![1_uOD4O3nuX5uCGZ7HLtoZjQ.webp](https://capable-butterfly-84cab64826.media.strapiapp.com/1_u_OD_4_O3nu_X5u_CGZ_7_H_Lto_Zj_Q_4df84252bd.webp)Built-in self-learning feedback loop

Wren AI is a fully open-source project! It’s on GitHub; check it out now!

🚀 GitHub: https://github.com/canner/wrenai

🙌 Website: https://www.getwren.ai/

Don’t forget to give ⭐ Wren AI a star on Github ⭐ if you’ve enjoyed this article, and as always, thank you for reading.



# CrateDB integrations

Copy page

Integrate with CrateDB using LangChain Python.

> [CrateDB](https://cratedb.com/database) is a distributed and scalable SQL database for storing and analyzing massive amounts of data in near real-time, even with complex queries. It is PostgreSQL-compatible, based on Lucene, and inheriting from Elasticsearch.

## 

[​

](https://docs.langchain.com/oss/python/integrations/providers/cratedb#installation-and-setup)

Installation and setup

### 

[​

](https://docs.langchain.com/oss/python/integrations/providers/cratedb#setup-cratedb)

Setup CrateDB

There are two ways to get started with CrateDB quickly. Alternatively, choose other [CrateDB installation options](https://cratedb.com/docs/guide/install/).

#### 

[​

](https://docs.langchain.com/oss/python/integrations/providers/cratedb#start-cratedb-on-your-local-machine)

Start CrateDB on your local machine

Example: Run a single-node CrateDB instance with security disabled, using Docker or Podman. This is not recommended for production use.

```
docker run --name=cratedb --rm \
  --publish=4200:4200 --publish=5432:5432 --env=CRATE_HEAP_SIZE=2g \
  crate:latest -Cdiscovery.type=single-node
```

#### 

[​

](https://docs.langchain.com/oss/python/integrations/providers/cratedb#deploy-cluster-on-cratedb-cloud)

Deploy cluster on CrateDB cloud

[CrateDB Cloud](https://cratedb.com/database/cloud) is a managed CrateDB service. Sign up for a [free trial](https://console.cratedb.cloud/?utm_source=langchain&utm_content=documentation).

### 

[​

](https://docs.langchain.com/oss/python/integrations/providers/cratedb#install-client)

Install client

Install the most recent version of the [langchain-cratedb](https://pypi.org/project/langchain-cratedb/) package and a few others that are needed for this tutorial.

pip

uv

```
pip install -U langchain-cratedb langchain-openai unstructured
```

## 

[​

](https://docs.langchain.com/oss/python/integrations/providers/cratedb#documentation)

Documentation

For a more detailed walkthrough of the CrateDB wrapper, see [using LangChain with CrateDB](https://cratedb.com/docs/guide/integrate/langchain/). See also [all features of CrateDB](https://cratedb.com/docs/guide/feature/) to learn about other functionality provided by CrateDB.

## 

[​

](https://docs.langchain.com/oss/python/integrations/providers/cratedb#features)

Features

The CrateDB adapter for LangChain provides APIs to use CrateDB as vector store, document loader, and storage for chat messages.

### 

[​

](https://docs.langchain.com/oss/python/integrations/providers/cratedb#vector-store)

Vector store

Use the CrateDB vector store functionality around `FLOAT_VECTOR` and `KNN_MATCH` for similarity search and other purposes. See also [CrateDBVectorStore Tutorial](https://github.com/crate/cratedb-examples/blob/main/topic/machine-learning/llm-langchain/vector_search.ipynb).Make sure you’ve configured a valid OpenAI API key.

```
export OPENAI_API_KEY=sk-XJZ...
```

```
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_cratedb import CrateDBVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter

loader = UnstructuredURLLoader(urls=["https://github.com/langchain-ai/langchain/raw/refs/tags/langchain-core==0.3.28/docs/docs/how_to/state_of_the_union.txt"])
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

# Connect to a self-managed CrateDB instance on localhost.
CONNECTION_STRING = "crate://?schema=testdrive"

store = CrateDBVectorStore.from_documents(
    documents=docs,
    embedding=embeddings,
    collection_name="state_of_the_union",
    connection=CONNECTION_STRING,
)

query = "What did the president say about Ketanji Brown Jackson"
docs_with_score = store.similarity_search_with_score(query)
```

### 

[​

](https://docs.langchain.com/oss/python/integrations/providers/cratedb#document-loader)

Document loader

Load load documents from a CrateDB database table, using the document loader `CrateDBLoader`, which is based on SQLAlchemy. See also [CrateDBLoader Tutorial](https://github.com/crate/cratedb-examples/blob/main/topic/machine-learning/llm-langchain/document_loader.ipynb).To use the document loader in your applications:

```
import sqlalchemy as sa
from langchain_community.utilities import SQLDatabase
from langchain_cratedb import CrateDBLoader

# Connect to a self-managed CrateDB instance on localhost.
CONNECTION_STRING = "crate://?schema=testdrive"

db = SQLDatabase(engine=sa.create_engine(CONNECTION_STRING))

loader = CrateDBLoader(
    'SELECT * FROM sys.summits LIMIT 42',
    db=db,
)
documents = loader.load()
```

### 

[​

](https://docs.langchain.com/oss/python/integrations/providers/cratedb#chat-message-history)

Chat message history

Use CrateDB as the storage for your chat messages. See also [CrateDBChatMessageHistory Tutorial](https://github.com/crate/cratedb-examples/blob/main/topic/machine-learning/llm-langchain/conversational_memory.ipynb).To use the chat message history in your applications:

```
from langchain_cratedb import CrateDBChatMessageHistory

# Connect to a self-managed CrateDB instance on localhost.
CONNECTION_STRING = "crate://?schema=testdrive"

message_history = CrateDBChatMessageHistory(
    session_id="test-session",
    connection=CONNECTION_STRING,
)

message_history.add_user_message("hi!")
```

### 

[​

](https://docs.langchain.com/oss/python/integrations/providers/cratedb#full-cache)

Full cache

The standard / full cache avoids invoking the LLM when the supplied prompt is exactly the same as one encountered already. See also [CrateDBCache Example](https://github.com/crate/langchain-cratedb/blob/main/examples/basic/cache.py).To use the full cache in your applications:

```
import sqlalchemy as sa
from langchain.globals import set_llm_cache
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_cratedb import CrateDBCache

# Configure cache.
engine = sa.create_engine("crate://crate@localhost:4200/?schema=testdrive")
set_llm_cache(CrateDBCache(engine))

# Invoke LLM conversation.
llm = ChatOpenAI(
    model_name="gpt-4.1",
    temperature=0.7,
)
print()
print("Asking with full cache:")
answer = llm.invoke("What is the answer to everything?")
print(answer.content)
```

### 

[​

](https://docs.langchain.com/oss/python/integrations/providers/cratedb#semantic-cache)

Semantic cache

The semantic cache allows users to retrieve cached prompts based on semantic similarity between the user input and previously cached inputs. It also avoids invoking the LLM when not needed. See also [CrateDBSemanticCache Example](https://github.com/crate/langchain-cratedb/blob/main/examples/basic/cache.py).To use the semantic cache in your applications:

```
import sqlalchemy as sa
from langchain.globals import set_llm_cache
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_cratedb import CrateDBSemanticCache

# Configure embeddings.
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Configure cache.
engine = sa.create_engine("crate://crate@localhost:4200/?schema=testdrive")
set_llm_cache(
    CrateDBSemanticCache(
        embedding=embeddings,
        connection=engine,
        search_threshold=1.0,
    )
)

# Invoke LLM conversation.
llm = ChatOpenAI(model_name="gpt-4.1")
print()
print("Asking with semantic cache:")
answer = llm.invoke("What is the answer to everything?")
print(answer.content)
```

---

# Prompt Engineering: Chain of thought and ReAct — SQL Agent

## Implement Langchain agents to accomplish traditional transaction processing using LLM, to demonstrate ReAct Prompt Engineering technique

[

![A B Vijay Kumar](https://miro.medium.com/v2/resize:fill:32:32/1*BQhW1q1CuV0QGx0lRlEeSg.jpeg)

](https://abvijaykumar.medium.com/?source=post_page---byline--85fa42575c06---------------------------------------)

[A B Vijay Kumar](https://abvijaykumar.medium.com/?source=post_page---byline--85fa42575c06---------------------------------------)

Follow

7 min read

·

Feb 10, 2024

98

4

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F85fa42575c06&operation=register&redirect=https%3A%2F%2Fabvijaykumar.medium.com%2Fprompt-engineering-chain-of-thought-and-react-sql-agent-85fa42575c06&source=---header_actions--85fa42575c06---------------------bookmark_footer------------------)

[

](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D85fa42575c06&operation=register&redirect=https%3A%2F%2Fabvijaykumar.medium.com%2Fprompt-engineering-chain-of-thought-and-react-sql-agent-85fa42575c06&source=---header_actions--85fa42575c06---------------------post_audio_button------------------)

*This blog will go through the Chain of Thought and ReAct Prompt Engineering techniques to guide the LLM to think with reasoning and act. We will also build an agent in Langchain to perform traditional transactions using SQL.*

## Prompt Engineering

Prompt engineering involves crafting carefully tailored input to language models to elicit desired responses. It’s a nuanced process that requires a deep understanding of the model’s capabilities and limitations. By refining prompts, engineers can guide models to produce more accurate, relevant, and creative outputs. Effective prompt engineering goes beyond mere manipulation of keywords. It involves providing context, setting the tone, and specifying the desired outcome.

While zero-short prompting is excellent for basic tasks, few-shot prompting allows the model to leverage pre-trained knowledge for more accurate responses. However, few-shot prompting falls short in tasks involving arithmetic, common sense, and symbolic reasoning.

To address the limitations of few-shot prompting, we use techniques such as “Chain of Thought” prompting. This method guides the language model through a step-by-step reasoning process by providing a few examples outlining the logic. This approach significantly improves the model’s performance on complex tasks, encouraging it to explain its reasoning along with the response.

### Chain of Thought

The Chain of Thought is one of the most effective prompt engineering techniques, that takes prompt engineering to a new level by leveraging the natural progression of ideas. Instead of providing a static prompt, this method involves crafting a series of prompts that build upon each other. The idea is to guide the model through a chain of related thoughts, encouraging it to explore and expand on concepts coherently.

Chain of thought prompting helps in providing reasoning capabilities as you go through step by step process of observing the response, and building on top of it. Chain of Thought prompting involves guiding the model through sequential reasoning, much like a human thought process.

Despite the effectiveness of Chain of Thought prompting, there’s an issue with naive greedy decoding, where the model generates responses one sentence at a time without considering the overall coherence.

**Self-consistency** prompting is a technique that calls the language model multiple times on the same prompt, selecting the most consistent answer. This helps overcome issues related to arithmetic and common sense reasoning. This enhancement generates multiple reasoning paths for a problem, aggregating them to find the most consistent answer.

LangChain handles the complexity of different prompt modifiers, making the process entirely unsupervised. Self-consistency boosts response accuracy without requiring additional human input or models.

You can read more about the chain of thought prompting [*here*](https://www.promptingguide.ai/techniques/cot).

### Reasoning and Action Prompting Technique

ReAct. Short for “synergizing reasoning and acting,” ReAct builds on the concepts of Chain of Thought prompting techniques and is an even more powerful tool that aids Foundation models in tackling user-requested tasks.

ReAct is a reasoning technique designed to structure problems and guide Foundation models through a sequence of steps to arrive at a solution. The process involves three key elements: Thought, Action, and Observation.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*XBh0aKnnFvI5wvpi5LAv4A.png)

1. **Thought**: The reasoning step, or thought, serves as a guide to the Foundation model, demonstrating how to approach a problem. It involves formulating a sequence of questions that lead the model to the desired solution.
2. **Action**: Once the thought is established, the next step is to define an action for the Foundation model to take. This action typically involves invoking an API from a predefined set, allowing the model to interact with external resources.
3. **Observation**: Following the action, the model observes and analyzes the results. The observations become crucial input for further reasoning and decision-making.

To illustrate the practical application of React. The following is an example of how React works on chatGPT.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*lB2NwFbn7vgMoR1h50IB4g.png)

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*sbCsRX6D5PI9wbF8r8K3-w.png)

> This may not be the perfect prompts :-D Please feel free to correct me if I am not using the right prompt.
> 
> But I think, you get the idea, of how ReAct technique
> 
> 1. Considers overall coherence to prevent illogical responses.
> 
> 2. Encourages diverse reasoning paths, ensuring alternative perspectives are thoroughly explored
> 
> 3. Implements self-consistency prompting, calling the model multiple times on the same prompt for a consistent answer.

You can read more about [ReAct here](https://www.promptingguide.ai/techniques/react)

## Get A B Vijay Kumar’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Langchain allows us to integrate our tools, to build agents. These tools could be fetching more information, that might be useful to enhance the context.

### Implementing a Langchain Agent to see ReAct in action

Let now implement this using Langchain, and implement an SQL agent, to demonstrate how reasoning is used to act and find the right response for the query. This is another implementation of Text2SQL. ([*you can read my blog on how we implement RAG based approach*](https://medium.com/@abvijaykumar/retrieval-augmented-generation-rag-with-llamaindex-on-a-database-text2sql-f4276943b256)).

Let's get started…Let's first configure our local Postgres database

I have installed Postgres on my MacBook and created 2 tables.

- `product_master`: Where I store the product_id and the name of the product.
- `inventor`: where I use the product_id and store the inventory of that product.

The following screenshots show the schema and the data that I inserted

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*jJnnXnubz6HEAhTy.png)

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/0*E1scQxSZ9DADeBCl.png)

Let's now create a `requirements.txt` with all the dependent libraries that we need for this project.

langchain  
openai  
streamlit  
python-dotenv  
psycopg2  
langchain_openai

The key libraries here other than `llama-index` are `sqlalchemy`, which is the Python SQL toolkit, and `psycopg2`, which is the adapter we will be using to connect to Postgres.

Let’s set the environment variables in `.env` file. In the env file, we provide the OPENAI_API_KEY and the database variables, as shown below

OPENAI_API_KEY=<<YourOPENAI key>>  
DB_USER=orderadmin  
DB_PASSWORD=orderadmin  
DB_HOST=localhost  
DB_NAME=postgres

Lets now walk through the application code

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*5hoMmwg4vtfXtp6rEDiWqg.png)

We are importing the standard libraries. I just want to call you `create_sql_agent`. This is used to create the SQL Agent that will perform the ReAct. You can read more about that [*here*](https://python.langchain.com/docs/integrations/toolkits/sql_database). [*AgentExecutor*](https://api.python.langchain.com/en/latest/agents/langchain.agents.agent.AgentExecutor.html) is another important class, which provides the runtime for the agents. Please go through Agents and concepts [*here*](https://python.langchain.com/docs/modules/agents/).

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*TliABthLy8eKTtpbd0mZug.png)

In the code above, we initiate the connection to the database and set up the necessary database parameters. Subsequently, we pass this information to the SQL agent, along with the Language Model (LLM). The agent utilizes these details to conduct reasoning, interacting with the database as required. The functionality is demonstrated in the accompanying video attached below.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*c6hh5ZOgjLTFLMrskehNbw.png)

In the provided code snippet, a method is being defined to invoke the agent using a specified prompt. Subsequently, in the subsequent code, we are developing a Streamlit chatbot application. This application utilizes the `callAgent()` method to handle all the prompts supplied by the user.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*bAHOjZFc4eYo1cSm8rOLbQ.png)

In the above code, We are creating a streamlit application, with a chat kind of interface. We will be storing the message in the `st.session_state` , and this will be printed in the main window as a chat. We are capturing the prompt that is given in the `st.chat_input()` and calling the `chat_engine()` that we created. LlamaIndex provides a convenient function to create a chat engine with the index that is created. This takes care of all the complexity of doing the RAG, and calling the appropriate LLM to get the response.

The following video shows the output.

There you go… you can see in the video and the screenshots how the agent can observe the results, apply reasoning, and act accordingly. This is a very powerful technique that agents use, to act as intelligent bots to get the job done. I will be going deeper into Agents and Agent orchestration in future blogs…

### Conclusion

React proves to be a valuable technique for prompting the Foundation models for more domain-specific tasks. By guiding the model through structured problems, React empowers it to reason and act effectively and is more extensible with the help of integration with other external sources.

I hope this blog was useful, and please leave your feedback and comments. Take care and see you soon with more blogs sharing my experiences...

You can find the code on my [*GitHub here*](https://github.com/abvijaykumar/react-agent)

[

Langchain

](https://medium.com/tag/langchain?source=post_page-----85fa42575c06---------------------------------------)

[

Generative Ai Tools

](https://medium.com/tag/generative-ai-tools?source=post_page-----85fa42575c06---------------------------------------)

[

OpenAI

](https://medium.com/tag/openai?source=post_page-----85fa42575c06---------------------------------------)

[  
](https://medium.com/tag/prompt?source=post_page-----85fa42575c06---------------------------------------)

---

# sqlalchemy.exc.InvalidRequestError: Table 'langchain_pg_collection' is already defined for this MetaData instance.  #14699

Closed

[#14726](https://github.com/langchain-ai/langchain/pull/14726)

Closed

[sqlalchemy.exc.InvalidRequestError: Table 'langchain_pg_collection' is already defined for this MetaData instance.](https://github.com/langchain-ai/langchain/issues/14699#top)#14699

[#14726](https://github.com/langchain-ai/langchain/pull/14726)

[![@arezazadeh](https://avatars.githubusercontent.com/u/35385652?u=e2e357efb1ba43156019290d1f1a3288898bf2ea&v=4&size=80)](https://github.com/arezazadeh)

## Description

[arezazadeh](https://github.com/arezazadeh)

opened [on Dec 14, 2023](https://github.com/langchain-ai/langchain/issues/14699#issue-2041031199)

### Issue you'd like to raise.

what is this issue, and how can i resolve it:

```python
    os.environ["AZURE_OPENAI_API_KEY"] = AZURE_OPENAI_API_KEY
    os.environ["AZURE_OPENAI_ENDPOINT"] = AZURE_OPENAI_ENDPOINT
    os.environ["OPENAI_API_TYPE"] = "azure"
    os.environ["OPENAI_API_VERSION"] = "2023-05-15"
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

    embedding = OpenAIEmbeddings()    COLLECTION_NAME = "network_team_documents"
    CONNECTION_STRING = PGVector.connection_string_from_db_params(        driver=os.environ.get(DB_DRIVER, DB_DRIVER),        host=os.environ.get(DB_HOST, DB_HOST),        port=int(os.environ.get(DB_PORT, DB_PORT)),        database=os.environ.get(DB_DB, DB_DB),        user=os.environ.get(DB_USER, DB_USER),        password=os.environ.get(DB_PASS, DB_PASS),    )    store = PGVector(        collection_name=COLLECTION_NAME,        connection_string=CONNECTION_STRING,        embedding_function=embedding,        extend_existing=True,    )    gpt4 = AzureChatOpenAI(        azure_deployment="GPT4",        openai_api_version="2023-05-15",    )    retriever = store.as_retriever(search_type="similarity", search_kwargs={"k": 10})    qa_chain = RetrievalQA.from_chain_type(llm=gpt4,                                           chain_type="stuff",                                           retriever=retriever,                                           return_source_documents=True)    return qa_chain
```

```python
Traceback (most recent call last):  File "/opt/network_tool/chatbot/views.py", line 21, in chat
    chat_object = create_session()  File "/opt/network_tool/chatbot/chatbot_functions.py", line 95, in create_session
    store = PGVector(  File "/opt/klevernet_venv/lib/python3.10/site-packages/langchain_community/vectorstores/pgvector.py", line 199, in __init__
    self.__post_init__()  File "/opt/klevernet_venv/lib/python3.10/site-packages/langchain_community/vectorstores/pgvector.py", line 207, in __post_init__
    EmbeddingStore, CollectionStore = _get_embedding_collection_store()  File "/opt/klevernet_venv/lib/python3.10/site-packages/langchain_community/vectorstores/pgvector.py", line 66, in _get_embedding_collection_store
    class CollectionStore(BaseModel):  File "/opt/klevernet_venv/lib/python3.10/site-packages/sqlalchemy/orm/decl_api.py", line 195, in __init__
    _as_declarative(reg, cls, dict_)  File "/opt/klevernet_venv/lib/python3.10/site-packages/sqlalchemy/orm/decl_base.py", line 247, in _as_declarative
    return _MapperConfig.setup_mapping(registry, cls, dict_, None, {})  File "/opt/klevernet_venv/lib/python3.10/site-packages/sqlalchemy/orm/decl_base.py", line 328, in setup_mapping
    return _ClassScanMapperConfig(  File "/opt/klevernet_venv/lib/python3.10/site-packages/sqlalchemy/orm/decl_base.py", line 578, in __init__
    self._setup_table(table)  File "/opt/klevernet_venv/lib/python3.10/site-packages/sqlalchemy/orm/decl_base.py", line 1729, in _setup_table
    table_cls(  File "", line 2, in __new__
  File "/opt/klevernet_venv/lib/python3.10/site-packages/sqlalchemy/util/deprecations.py", line 281, in warned
    return fn(*args, **kwargs)  # type: ignore[no-any-return]
  File "/opt/klevernet_venv/lib/python3.10/site-packages/sqlalchemy/sql/schema.py", line 436, in __new__
    return cls._new(*args, **kw)  File "/opt/klevernet_venv/lib/python3.10/site-packages/sqlalchemy/sql/schema.py", line 468, in _new
    raise exc.InvalidRequestError(
sqlalchemy.exc.InvalidRequestError: Table 'langchain_pg_collection' is already defined for this MetaData instance.  Specify 'extend_existing=True' to redefine options and columns on an existing Table object.
```

### Suggestion:

*No response*

## Activity

[![dosubot](https://avatars.githubusercontent.com/in/324583?v=4&size=80)](https://github.com/apps/dosubot)

### dosubot commented on Dec 14, 2023

[dosubot](https://github.com/apps/dosubot)bot

[on Dec 14, 2023](https://github.com/langchain-ai/langchain/issues/14699#issuecomment-1855247146) – with [DosuBot](https://dosu.dev/) · edited by [dosubot](https://github.com/apps/dosubot)

*🤖*

Hi [@arezazadeh](https://github.com/arezazadeh), nice to meet you! I'm [Dosu](https://dosu.dev/), a friendly bot here to assist you with bugs, answer questions, and guide you in contributing to our repository. Feel free to ask me anything you'd like about our code. I'm here to make your life easier while we wait for a human maintainer to pop in. Looking forward to helping you with your issue!

The error you're encountering, "sqlalchemy.exc.InvalidRequestError: Table 'langchain_pg_collection' is already defined for this MetaData instance", is caused by SQLAlchemy trying to define a table that has already been defined in the same MetaData instance. This can occur if the code that defines the table is executed more than once in the same process.

In your code, the table 'langchain_pg_collection' is defined in the class 'CollectionStore'. If this class is instantiated more than once in the same process, it will cause the error.

To resolve this issue, you can modify the code to ensure that the table definition is only executed once. One way to do this is to check if the table already exists before defining it. You can use the `has_table` method of the `MetaData` class in SQLAlchemy to check if a table already exists.

Here is an example of how you can modify the 'CollectionStore' class to check if the table already exists:

```python
from sqlalchemy import MetaData

class CollectionStore(BaseModel):    """Collection store."""

    metadata = MetaData()    if not metadata.tables.get('langchain_pg_collection'):        __tablename__ = "langchain_pg_collection"

        name = sqlalchemy.Column(sqlalchemy.String)        cmetadata = sqlalchemy.Column(JSON)        embeddings = relationship(            "EmbeddingStore",            back_populates="collection",            passive_deletes=True,        )
```

In this modified code, the `metadata.tables.get('langchain_pg_collection')` method is used to check if the 'langchain_pg_collection' table already exists. If it does not exist, the table is defined. If it does exist, the table definition is skipped. This ensures that the table is only defined once, preventing the "Table 'langchain_pg_collection' is already defined for this MetaData instance" error.

For more information, you can refer to the [LangChain codebase](https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain/vectorstores/pgvector.py) and the [SQLAlchemy documentation](https://docs.sqlalchemy.org/en/14/core/metadata.html).

Please let me know if this resolves your issue or if you need further assistance.

## Sources

- [libs/langchain/langchain/vectorstores/pgvector.py](https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain/vectorstores/pgvector.py)

---

This response is meant to be useful and save you time. It is **not meant to be a precise solution**, but rather a starting point for your own research.

Help me be more useful! Please leave a 👍 if this is helpful and 👎 if it is irrelevant.

If you want to continue the conversation, start your reply with [@dosu-bot](https://github.com/dosu-bot).

[![](https://avatars.githubusercontent.com/in/324583?s=64&v=4)dosubot](https://github.com/apps/dosubot)

added 

[area: vector store](https://github.com/langchain-ai/langchain/issues?q=state%3Aopen%20label%3A%22area%3A%20vector%20store%22)

 

[bugRelated to a bug, vulnerability, unexpected error with an existing feature](https://github.com/langchain-ai/langchain/issues?q=state%3Aopen%20label%3A%22bug%22)

 [on Dec 14, 2023](https://github.com/langchain-ai/langchain/issues/14699#event-11244122169)

[![johnmai-dev](https://avatars.githubusercontent.com/u/1825679?u=bc5db0325ef2a546c67e1e2ae1f7a0af7afe6803&v=4&size=80)](https://github.com/johnmai-dev)

### johnmai-dev commented on Dec 14, 2023

[johnmai-dev](https://github.com/johnmai-dev)

[on Dec 14, 2023](https://github.com/langchain-ai/langchain/issues/14699#issuecomment-1855326519)

Contributor

langchain==0.0.348 is ok，the bug appears to have been caused by version 0.0.350 & 0.0.349.

[#14463](https://github.com/langchain-ai/langchain/pull/14463) [#14414](https://github.com/langchain-ai/langchain/pull/14414) [@baskaryan](https://github.com/baskaryan) [@efriis](https://github.com/efriis)

[langchain/libs/langchain/langchain/vectorstores/pgvector.py](https://github.com/langchain-ai/langchain/blob/6ceb8e2ad43856a23b07dcc5b2f780504e28d614/libs/langchain/langchain/vectorstores/pgvector.py#L104)

Line 104 in [6ceb8e2](https://github.com/langchain-ai/langchain/commit/6ceb8e2ad43856a23b07dcc5b2f780504e28d614)

def _get_embedding_store() -> Any:

[langchain/libs/community/langchain_community/vectorstores/pgvector.py](https://github.com/langchain-ai/langchain/blob/dec277a637b7aeb645a0074431a2029fde5058f0/libs/community/langchain_community/vectorstores/pgvector.py#L63)

Line 63 in [dec277a](https://github.com/langchain-ai/langchain/commit/dec277a637b7aeb645a0074431a2029fde5058f0)

def _get_embedding_collection_store() -> Any:

[![arezazadeh](https://avatars.githubusercontent.com/u/35385652?u=e2e357efb1ba43156019290d1f1a3288898bf2ea&v=4&size=80)](https://github.com/arezazadeh)

### arezazadeh commented on Dec 14, 2023

[arezazadeh](https://github.com/arezazadeh)

[on Dec 14, 2023](https://github.com/langchain-ai/langchain/issues/14699#issuecomment-1855329470)

Author

i had the issue on both 348 and 349, I was able to fix it by adding `__table_args__ = {'extend_existing': True}` to the LangChainTable and also downgraded my 349 to 348 and did the same thing and fixed the issue.

[![ElReyZero](https://avatars.githubusercontent.com/u/31524106?u=598fa39d4e22f0a9fc4f3f0d51c013afe8347f25&v=4&size=80)](https://github.com/ElReyZero)

### ElReyZero commented on Dec 14, 2023

[ElReyZero](https://github.com/ElReyZero)

[on Dec 14, 2023](https://github.com/langchain-ai/langchain/issues/14699#issuecomment-1856298253) · edited by [ElReyZero](https://github.com/ElReyZero)

Contributor

Downgrading to 0.0.348 worked for me without adding the extend_existing argument!

[![efriis](https://avatars.githubusercontent.com/u/9557659?u=44391f1f5f5e3a72acc9772ca30f28bfdcc25fac&v=4&size=80)](https://github.com/efriis)

### efriis commented on Dec 14, 2023

[efriis](https://github.com/efriis)

[on Dec 14, 2023](https://github.com/langchain-ai/langchain/issues/14699#issuecomment-1856308298)

Contributor

Thanks for the report folks! I'll look into this today

[![](https://avatars.githubusercontent.com/u/9557659?s=64&u=44391f1f5f5e3a72acc9772ca30f28bfdcc25fac&v=4)efriis](https://github.com/efriis)

mentioned this [on Dec 14, 2023](https://github.com/langchain-ai/langchain/issues/14699#event-1340301521)

- [community[patch]: fix pgvector sqlalchemy #14726](https://github.com/langchain-ai/langchain/pull/14726)

[![](https://avatars.githubusercontent.com/u/9557659?s=64&u=44391f1f5f5e3a72acc9772ca30f28bfdcc25fac&v=4)efriis](https://github.com/efriis)

closed this as [completed](https://github.com/langchain-ai/langchain/issues?q=is%3Aissue%20state%3Aclosed%20archived%3Afalse%20reason%3Acompleted)in [#14726](https://github.com/langchain-ai/langchain/pull/14726)[on Dec 14, 2023](https://github.com/langchain-ai/langchain/issues/14699#event-11253084402)

[![](https://avatars.githubusercontent.com/u/9557659?s=64&u=44391f1f5f5e3a72acc9772ca30f28bfdcc25fac&v=4)efriis](https://github.com/efriis)

added a commit that references this issue [on Dec 14, 2023](https://github.com/langchain-ai/langchain/issues/14699#event-11253084677)

[](https://github.com/langchain-ai/langchain/commit/9fb26a2a718bc18a5ce48f04cf6b66bc4751b734)

[](https://github.com/langchain-ai/langchain/commit/9fb26a2a718bc18a5ce48f04cf6b66bc4751b734)

[community[patch]: fix pgvector sqlalchemy (](https://github.com/langchain-ai/langchain/commit/9fb26a2a718bc18a5ce48f04cf6b66bc4751b734)[#14726](https://github.com/langchain-ai/langchain/pull/14726))

[](https://docs.github.com/articles/closing-issues-via-commit-messages)Verified[9fb26a2](https://github.com/langchain-ai/langchain/commit/9fb26a2a718bc18a5ce48f04cf6b66bc4751b734)

[![efriis](https://avatars.githubusercontent.com/u/9557659?u=44391f1f5f5e3a72acc9772ca30f28bfdcc25fac&v=4&size=80)](https://github.com/efriis)

### efriis commented on Dec 14, 2023

[efriis](https://github.com/efriis)

[on Dec 14, 2023](https://github.com/langchain-ai/langchain/issues/14699#issuecomment-1856647149)

Contributor

This should be fixed in the next release! Also, the others are correct that you shouldn't have the `extend_existing` param in your init

[![nannarane](https://avatars.githubusercontent.com/u/50683718?v=4&size=80)](https://github.com/nannarane)

### nannarane commented on Dec 15, 2023

[nannarane](https://github.com/nannarane)

[on Dec 15, 2023](https://github.com/langchain-ai/langchain/issues/14699#issuecomment-1857393076)

> i had the issue on both 348 and 349, I was able to fix it by adding `__table_args__ = {'extend_existing': True}` to the LangChainTable and also downgraded my 349 to 348 and did the same thing and fixed the issue.

hello. I also had the same problem,  
**table_args** = {'extend_existing': True}

Can you tell me which part of the code you directly inserted?  
Can you tell me how you handled it without putting it directly in that pip package?

[![](https://avatars.githubusercontent.com/in/324583?s=64&v=4)dosubot](https://github.com/apps/dosubot)

mentioned this [on Dec 15, 2023](https://github.com/langchain-ai/langchain/issues/14699#event-1340524165)

- [Table 'langchain_pg_collection' is already defined for this MetaData instance. Specify 'extend_existing=True' #14760](https://github.com/langchain-ai/langchain/issues/14760)

[![efriis](https://avatars.githubusercontent.com/u/9557659?u=44391f1f5f5e3a72acc9772ca30f28bfdcc25fac&v=4&size=80)](https://github.com/efriis)

### efriis commented on Dec 15, 2023

[efriis](https://github.com/efriis)

[on Dec 15, 2023](https://github.com/langchain-ai/langchain/issues/14699#issuecomment-1858306741)

Contributor

[#14726](https://github.com/langchain-ai/langchain/pull/14726)

[![arezazadeh](https://avatars.githubusercontent.com/u/35385652?u=e2e357efb1ba43156019290d1f1a3288898bf2ea&v=4&size=80)](https://github.com/arezazadeh)

### arezazadeh commented on Dec 15, 2023

[arezazadeh](https://github.com/arezazadeh)

[on Dec 15, 2023](https://github.com/langchain-ai/langchain/issues/14699#issuecomment-1858412929)

Author

I added it in this file:  
`/lib/python3.10/site-packages/langchain/vectorstores/_pgvector_data_models.py`

```
class CollectionStore(BaseModel):
    """Collection store."""

    __tablename__ = "langchain_pg_collection"
    __table_args__ = {'extend_existing': True}
```

[![reneric](https://avatars.githubusercontent.com/u/4227607?v=4&size=80)](https://github.com/reneric)

### reneric commented on Dec 16, 2023

[reneric](https://github.com/reneric)

[on Dec 16, 2023](https://github.com/langchain-ai/langchain/issues/14699#issuecomment-1858927304)

Why is `langchain_pg_collection` being used exactly? Is that something happening under the hood when attempting to initialize another collection?

[![johnmai-dev](https://avatars.githubusercontent.com/u/1825679?u=bc5db0325ef2a546c67e1e2ae1f7a0af7afe6803&v=4&size=80)](https://github.com/johnmai-dev)

### johnmai-dev commented on Dec 18, 2023

[johnmai-dev](https://github.com/johnmai-dev)

[on Dec 18, 2023](https://github.com/langchain-ai/langchain/issues/14699#issuecomment-1862019863) · edited by [johnmai-dev](https://github.com/johnmai-dev)

Contributor

0.0.351

Instantiating multiple PGVectors with multiple collection_names may result in a software bug.

raise exc.InvalidRequestError(  
sqlalchemy.exc.InvalidRequestError: Multiple classes found for path "EmbeddingStore" in the registry of this declarative base. Please use a fully module-qualified path.

[![johnmai-dev](https://avatars.githubusercontent.com/u/1825679?u=bc5db0325ef2a546c67e1e2ae1f7a0af7afe6803&v=4&size=80)](https://github.com/johnmai-dev)

### johnmai-dev commented on Dec 18, 2023

[johnmai-dev](https://github.com/johnmai-dev)

[on Dec 18, 2023](https://github.com/langchain-ai/langchain/issues/14699#issuecomment-1862021515) · edited by [johnmai-dev](https://github.com/johnmai-dev)

Contributor

> 0.0.351
> 
> Instantiating multiple PGVectors with multiple collection_names may result in a software bug.
> 
> raise exc.InvalidRequestError( sqlalchemy.exc.InvalidRequestError: Multiple classes found for path "EmbeddingStore" in the registry of this declarative base. Please use a fully module-qualified path.

Why utilize the _get_embedding_collection_store method instead of following the approach used in version 0.0.348?  
[@efriis](https://github.com/efriis) [@baskaryan](https://github.com/baskaryan)

[![](https://avatars.githubusercontent.com/u/13333726?s=64&u=82ebf1e0eb0663ebd49ba66f67a43f51bbf11442&v=4)hinthornw](https://github.com/hinthornw)

added a commit that references this issue [on Dec 18, 2023](https://github.com/langchain-ai/langchain/issues/14699#event-11284042541)

[](https://github.com/langchain-ai/langchain/commit/c81d0f9290c73b95cdae27eb386f562285e24c9c)

[](https://github.com/langchain-ai/langchain/commit/c81d0f9290c73b95cdae27eb386f562285e24c9c)

[community[patch]: fix pgvector sqlalchemy (](https://github.com/langchain-ai/langchain/commit/c81d0f9290c73b95cdae27eb386f562285e24c9c)[#14726](https://github.com/langchain-ai/langchain/pull/14726))

[](https://docs.github.com/articles/closing-issues-via-commit-messages)[c81d0f9](https://github.com/langchain-ai/langchain/commit/c81d0f9290c73b95cdae27eb386f562285e24c9c)

[![nannarane](https://avatars.githubusercontent.com/u/50683718?v=4&size=80)](https://github.com/nannarane)

### nannarane commented on Dec 21, 2023

[nannarane](https://github.com/nannarane)

[on Dec 21, 2023](https://github.com/langchain-ai/langchain/issues/14699#issuecomment-1867119851)

For inquiries about [#14699 (comment)](https://github.com/langchain-ai/langchain/issues/14699#issuecomment-1857393076), we registered this issue because it was installed through pip when building the docker image to run on Kubernetes.

I solved it by lowering the version to 0.0.311. It seems that [c81d0f9](https://github.com/langchain-ai/langchain/commit/c81d0f9290c73b95cdae27eb386f562285e24c9c) has been treated as second-rate now.

[![johnmai-dev](https://avatars.githubusercontent.com/u/1825679?u=bc5db0325ef2a546c67e1e2ae1f7a0af7afe6803&v=4&size=80)](https://github.com/johnmai-dev)

### johnmai-dev commented on Dec 22, 2023

[johnmai-dev](https://github.com/johnmai-dev)

[on Dec 22, 2023](https://github.com/langchain-ai/langchain/issues/14699#issuecomment-1867353074)

Contributor

langchain-community >= 0.0.5 is ok!

[![](https://avatars.githubusercontent.com/u/48178546?s=64&v=4)AyoTheDev](https://github.com/AyoTheDev)

mentioned this in 2 issues [on Dec 23, 2023](https://github.com/langchain-ai/langchain/issues/14699#event-1342423958)

- [Foreign key associated with column 'langchain_pg_embedding.collection_id' could not find table #15096](https://github.com/langchain-ai/langchain/issues/15096)

- [Foreign key associated with column 'langchain_pg_embedding.collection_id' could not find table pgvector/pgvector#390](https://github.com/pgvector/pgvector/issues/390)

[![vigneshsrinivasan9](https://avatars.githubusercontent.com/u/12109720?v=4&size=80)](https://github.com/vigneshsrinivasan9)

### vigneshsrinivasan9 commented on Dec 27, 2023

[vigneshsrinivasan9](https://github.com/vigneshsrinivasan9)

[on Dec 27, 2023](https://github.com/langchain-ai/langchain/issues/14699#issuecomment-1870561695) · edited by [vigneshsrinivasan9](https://github.com/vigneshsrinivasan9)

> `/lib/python3.10/site-packages/langchain/vectorstores/_pgvector_data_models.py`

Is this issue fixed in the latest release? what's the workaround for this? I am using langchain 0.0.352

**sqlalchemy.exc.InvalidRequestError: Multiple classes found for path "EmbeddingStore" in the registry of this declarative base. Please use a fully module-qualified path.**

[![](https://avatars.githubusercontent.com/u/103998125?s=64&u=1b852354696d1846c13f4974d24257da6cc11a3d&v=4)arunraja1](https://github.com/arunraja1)

added a commit that references this issue [on Feb 15, 2024](https://github.com/langchain-ai/langchain/issues/14699#event-11811887899)

[](https://github.com/skypointcloud/skypoint-langchain/commit/87edf891fc5c03b97a2b96699d11ed9a7ae1cba9)

[](https://github.com/skypointcloud/skypoint-langchain/commit/87edf891fc5c03b97a2b96699d11ed9a7ae1cba9)

[Langchain version upgrade (](https://github.com/skypointcloud/skypoint-langchain/commit/87edf891fc5c03b97a2b96699d11ed9a7ae1cba9)[#8](https://github.com/skypointcloud/skypoint-langchain/pull/8))

[](https://docs.github.com/articles/closing-issues-via-commit-messages)Partially verified[87edf89](https://github.com/skypointcloud/skypoint-langchain/commit/87edf891fc5c03b97a2b96699d11ed9a7ae1cba9)

[![](https://avatars.githubusercontent.com/u/42812152?s=64&v=4)CJ-Lab7](https://github.com/CJ-Lab7)

mentioned this [on Mar 12, 2025](https://github.com/langchain-ai/langchain/issues/14699#event-2163247487)

- [Store initialization race condition - Table 'langchain_pg_collection' is already defined for this MetaData instance langchain-postgres#165](https://github.com/langchain-ai/langchain-postgres/issues/165)

---

## [Generative AI for SAP Part III. LLMs with Database Queries using Natural Language (NLQ)](https://community.sap.com/t5/artificial-intelligence-blogs-posts/generative-ai-for-sap-part-iii-llms-with-database-queries-using-natural/ba-p/13575460)

![MarioDeFelipe](https://avatars.profile.sap.com/d/5/idd54a66537cf10dee8ff1d1db09cfb0088e9ae1b985efdfc003fb1217b9d6b46a_small.jpeg "MarioDeFelipe")

[MarioDeFelipe](https://community.sap.com/t5/user/viewprofilepage/user-id/13491)

Active Contributor

‎2023 Sep 03 8:36 AM

[](https://community.sap.com/t5/kudos/messagepage/board-id/aiblog-board/message-id/356/tab/all-users "Click here to see who liked this post")

 

5,454

- SAP Managed Tags
- [Artificial Intelligence](https://community.sap.com/t5/c-khhcw49343/Artificial%2520Intelligence/pd-p/c3c3a408-33ea-4c2a-ae6f-05461e76982d)

Thank you for coming to this blog series. In my [first blog](https://blogs.sap.com/2023/08/13/generative-ai-for-sap-using-aws.-private-domains-and-foundation-models/), I introduced the idea of Foundation Models for SAP and how to deploy them on our private account, private vs. public access topics, which will evolve.  

In my [second blog](https://blogs.sap.com/?p=1827322), I introduced the concept of Model Customizing, meaning that for an existing Foundation Model, how to infuse it with a new dataset without the need to pre-train it; this is important if you like a conversational AI in particular, but we want to feed it with our Enterprise data, and providing a way to do it called RAG aka Retrieval Augmented Generation, a relatively new methodology for Models to retrieve facts from an external knowledge base on most accurate, up-to-date information.  

   

In this third blog, I am not leaving the same concept, leveraging existing LLMs and (for the moment) avoiding the pre-training topic. I firmly believe that enterprises will have their own LLMs using one of the existing models as a base. That's out of discussion, but the evolution of the LLMs is so intense that it will probably take some time to get to that point. Pre-training models is not an easy thing and is not cheap either. In this series of blogs, I am introducing a way to interact with existing LLMs with techniques that do not require pre-training the models on our own datasets. Then, in this blog, I present what I believe is an exciting topic: While building an end-to-end solution, where a conversation will end by accessing live data from another application.  

   

This is possible with Natural Language Queries (NLQ) and LangChain Agents.  

Natural language querying allows users to interact with databases; leveraging the power of LangChain, [**SQL** **Agents**](https://api.python.langchain.com/en/latest/chains/langchain.chains.sql_database.query.create_sql_query_chain.html), and Large Language Models (LLMs), we can create applications that enable users to query databases using natural language.

![](https://community.sap.com/legacyfs/online/storage/blog_attachments/2023/09/Captura-de-Pantalla-2023-09-02-a-las-21.36.53.png)

![](https://community.sap.com/legacyfs/online/storage/blog_attachments/2016/02/sapnwabline_885687.png)

## LangChain

LangChain is a framework designed for building applications powered by language models. It provides a standard chain interface, integrates with various tools, and offers end-to-end application chains. The two main features of LangChain are data-awareness and agentic behavior.

Data awareness enables the language model to connect to other data sources, while agentic behavior allows it to interact with its environment. Using **agents**, LangChain can dynamically decide which tools to call based on user input. This makes agents extremely powerful when used correctly.

LangChain provides two main methods to interact with SQL Databases: using Chains for Query creation and execution. On top of the Chain, another technique is to optionally interact with SQL databases using Agents for more flexible querying. LangChain SQL Agent provides a more flexible way of interacting with SQL Databases than the `SQLDatabaseChain`.  

![](https://community.sap.com/legacyfs/online/storage/blog_attachments/2023/09/Captura-de-Pantalla-2023-09-03-a-las-9.22.13.png)

What does all this mean?  

🧑🏻‍💻 We ask a question without a query, "How many sales did we have this week for this company code?"  

❓ LLM doesn't know about queries, goes to LangChain SQL Agent / Chain, it translates customer question into an SQL Query  

🛢 DB is queried using the SQLAlchemy library (or others)  

🤖 LLM now has all the information it needs and can provide an answer to the user  

   

**Why use Agents on top of Chains**  
*The main advantages of using the SQL Agent are:*  

- *1️⃣ It can answer questions based on the databases' schema as well as on the databases' content (like describing a specific table)*

- *2️⃣ It can recover from errors by running a generated query, catching the traceback, and regenerating it correctly*

This blog uses Langchain to connect the application with LLM and External Data Sources, such as an Oracle DB for querying.

## How *Agents* work

The **SQL Database Agent** from LangChain is designed to interact with any database, allowing users to ask questions in natural language and receive answers.

```python
from langchain import Cohere, SQLDatabase, SQLDatabaseChain
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.agents import create_sql_agent

import cx_Oracle
import os
import cohere
import os

COHERE_API_KEY="Your Cohere API Key"
os.environ["COHERE_API_KEY"] = COHERE_API_KEY

from sqlalchemy import create_engine
engine=create_engine(url, echo=True)
db = SQLDatabase(engine)

lib_dir = os.path.join(os.environ.get("HOME"), "Development", "instantclient_19_8")
cx_Oracle.init_oracle_client(lib_dir=lib_dir)

hostname='localhost'
port='...'
service_name='...'
username='<...>'
password='<...>'

# cx_Oracle.init_oracle_client(lib_dir=lib_dir)
oracle_connection_string_fmt = (
  'oracle+cx_oracle://{username}:{password}@' +
  cx_Oracle.makedsn('{hostname}', '{port}', service_name='{service_name}')
)
url = oracle_connection_string_fmt.format(
  username=username, password=password, 
  hostname=hostname, port=port, 
  service_name=service_name,
)

agent_executor = create_sql_agent(
    llm=Cohere(temperature=0),
    toolkit=SQLDatabaseToolkit(db=db, llm=Cohere(temperature=0)),
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)
```

   

The way that Langchain works is that you can configure it as a library inside of your application and connect it to different endpoints.  

In our example, we connected to a database and an API endpoint. Still, we've also got a large language model, which gives us our natural language capability to query the database using natural language.  

We might ask the LLM, "How many Materials did we create yesterday?"  

The application receives the prompt "How many Materials did we create yesterday?" and sends that through LangChain.  

LLMs can't execute SQL Queries; LLMs are text encoders or decoders, not SQL executors. Here is where we interact with LangChain Agents. Agents will receive the SQL query generated and will execute the SQL query against the database to get the information.  

The whole thing is about prompt engineering; we did in-context learning. I just introduced how it would work with an SQL query, but this can be applied to many other topics; we can use Agents to execute Matemathic calculations (LLMs don't do mathematics; they are text encoders and decoders), they can book a flight for us if they can connect to any SAP API from any other application, which I will describe in other blogs.  

![](https://community.sap.com/legacyfs/online/storage/blog_attachments/2016/02/sapnwabline_885687.png)  

# ![LlamaIndexを完全に理解するチュートリアル その１：処理の概念や流れを理解する基礎編（v0.6.8対応） | DevelopersIO](https://d1tlzifd8jdoy4.cloudfront.net/wp-content/uploads/2023/03/eyecatch-llamdaindex.png)LlamaIndex alternative

While Langchain is a framework for Generative AI application development and orchestration, LlamaIndex (formerly GPT Index) is a data framework for LLM applications to ingest, structure, and access private or domain-specific data.  

With LlamaIndex, thanks to its data connectors, you can effortlessly incorporate data from diverse sources such as APIs, databases, and PDFs. This data is structured into optimized intermediate formats suitable for LLMs. LlamaIndex enables seamless interaction and conversation with your data through query engines, chat interfaces, and LLM-powered data agents, all in natural language.

![](https://community.sap.com/legacyfs/online/storage/blog_attachments/2023/09/Captura-de-Pantalla-2023-09-02-a-las-22.37.13.png)

LlamaIndex vectorized the data, as we described in previous blogs, to prepare the data into a format that can be understood by the LLM.  The process primarily encompasses two key phases: the indexing phase and the querying phase**. The primary purpose of using LlamaIndex is the standardization of different sources and the performance increase this will provide.**  

# ![](https://community.sap.com/legacyfs/online/storage/blog_attachments/2016/02/sapnwabline_885687.png)

# Conclusion

In this blog, we introduced the concept and some details of using LangChain’s SQL Database Chain and Agents with large language models to perform natural language queries (NLQ) of any Phyton [SQLAlchemy](https://www.sqlalchemy.org/) database. I wanted to emphasize ***Agents***, a fundamental piece in all modern frameworks; LangChain uses Agents, LlamaIndex uses Agents, and Bedrock just introduced Agents.

Using LangChain’s SQL Database Chain and SQL Database Agent, we can leverage large language models (LLMs) to ask questions of multiple types of databases using natural language without building the query ourselves. Questions will be converted into SQL queries and executed against the database. Assuming the generated SQL query is well-formed, the query results will be converted into a textual explanation. For example, we ask questions like, “*How many customers have purchased this Material in the last 12 months?*” or “*What were the total purchases we had in August for this company code?*” These will be converted into SQL `SELECT` statements. The answer is then composed into textual explanations as a response to our application.

- [aws](https://community.sap.com/t5/tag/aws/tg-p/board-id/aiblog-board)
- [cohere](https://community.sap.com/t5/tag/cohere/tg-p/board-id/aiblog-board)
- [LangChain](https://community.sap.com/t5/tag/LangChain/tg-p/board-id/aiblog-board)
- [LlamaIndex](https://community.sap.com/t5/tag/LlamaIndex/tg-p/board-id/aiblog-board)
- [LLM](https://community.sap.com/t5/tag/LLM/tg-p/board-id/aiblog-board)

---

https://www.sqlalchemy.org/#:~:text=SQLAlchemy%20is%20the%20Python%20SQL,power%20and%20flexibility%20of%20SQL.



# The Python SQL Toolkit and Object Relational Mapper

SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

It provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.

Documentation

- [**Current Documentation (version 2.0)**](https://docs.sqlalchemy.org/) - learn SQLAlchemy here
  - [Documentation Overview](https://docs.sqlalchemy.org/)
  - [Installation Guide](https://docs.sqlalchemy.org/intro.html#installation)
  - [ORM Quickstart](https://docs.sqlalchemy.org/orm/quickstart.html)
  - [Comprehensive Tutorial](https://docs.sqlalchemy.org/tutorial/index.html)
  - **Reference Guides**
    - [Object Relational Mapping (ORM)](https://docs.sqlalchemy.org/orm/)
    - [Core (Connections, Schema Management, SQL)](https://docs.sqlalchemy.org/core/)
    - [Dialects (specific backends)](https://docs.sqlalchemy.org/dialects/)
- **Documentation by Version**
  - [Version 2.1 (beta)](https://docs.sqlalchemy.org/en/21/)
  - [Version 2.0](https://docs.sqlalchemy.org/en/20/)
  - [Version 1.4](https://docs.sqlalchemy.org/en/14/)

Learn More

- **Front Matter**
  - [SQLAlchemy's Philosophy](https://www.sqlalchemy.org/philosophy.html)
  - [Overview of Key Features](https://www.sqlalchemy.org/features.html)
  - [Testimonials](https://www.sqlalchemy.org/quotes.html)
- [**Library**](https://www.sqlalchemy.org/library.html) - Articles and Talks
  - [Talks and Tutorials](https://www.sqlalchemy.org/library.html#talks)
  - [Architecture](https://www.sqlalchemy.org/library.html#architecture)

Resources

- [Release History / Download Information](https://www.sqlalchemy.org/download.html)
- [News and Announcements](https://www.sqlalchemy.org/blog/)
- **Community**
  - [Getting Support](https://www.sqlalchemy.org/support.html)
  - [Participate in the Project](https://www.sqlalchemy.org/participate.html)
  - [Get Involved with Development](https://www.sqlalchemy.org/develop.html)
  - [Code of Conduct](https://www.sqlalchemy.org/codeofconduct.html)



---

# Motherduck integrations

Copy page

Integrate with Motherduck using LangChain Python.

> [MotherDuck](https://motherduck.com/) is a cloud data warehouse powered by DuckDB.

## 

[​

](https://docs.langchain.com/oss/python/integrations/providers/motherduck#installation-and-setup)

Installation and setup

First, you need to install `duckdb` python package.

pip

uv

```
pip install duckdb
```

You will also need to sign up for an account at [MotherDuck](https://motherduck.com/)After that, you should set up a connection string - we mostly integrate with Motherduck through SQLAlchemy. The connection string is likely in the form:

```
token="..."

conn_str = f"duckdb:///md:my_db?motherduck_token={token}"
```

For more authentication options, see the [MotherDuck SQLAlchemy documentation](https://motherduck.com/docs/integrations/language-apis-and-drivers/python/sqlalchemy/).

## 

[​

](https://docs.langchain.com/oss/python/integrations/providers/motherduck#sqlchain)

SQLChain

You can use the SQLChain to query data in your MotherDuck instance in natural language.

```
from langchain_openai import OpenAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
db = SQLDatabase.from_uri(conn_str)
db_chain = SQLDatabaseChain.from_llm(OpenAI(temperature=0), db, verbose=True)
```

## 

[​

](https://docs.langchain.com/oss/python/integrations/providers/motherduck#llmcache)

LLMCache

You can also easily use MotherDuck to cache LLM requests. Once again this is done through the SQLAlchemy wrapper.

```
import sqlalchemy
from langchain.globals import set_llm_cache
eng = sqlalchemy.create_engine(conn_str)
set_llm_cache(SQLAlchemyCache(engine=eng))
```

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/python/integrations/providers/motherduck.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](https://docs.langchain.com/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

Was this page helpful?

---

# Build a SQL agent

Copy page

## 

[​

](https://docs.langchain.com/oss/python/langchain/sql-agent#overview)

Overview

In this tutorial, you will learn how to build an agent that can answer questions about a SQL database using LangChain [agents](https://docs.langchain.com/oss/python/langchain/agents).At a high level, the agent will:

1

[

](https://docs.langchain.com/oss/python/langchain/sql-agent#)

Fetch the available tables and schemas from the database

2

[

](https://docs.langchain.com/oss/python/langchain/sql-agent#)

Decide which tables are relevant to the question

3

[

](https://docs.langchain.com/oss/python/langchain/sql-agent#)

Fetch the schemas for the relevant tables

4

[

](https://docs.langchain.com/oss/python/langchain/sql-agent#)

Generate a query based on the question and information from the schemas

5

[

](https://docs.langchain.com/oss/python/langchain/sql-agent#)

Double-check the query for common mistakes using an LLM

6

[

](https://docs.langchain.com/oss/python/langchain/sql-agent#)

Execute the query and return the results

7

[

](https://docs.langchain.com/oss/python/langchain/sql-agent#)

Correct mistakes surfaced by the database engine until the query is successful

8

[

](https://docs.langchain.com/oss/python/langchain/sql-agent#)

Formulate a response based on the results

Building Q&A systems of SQL databases requires executing model-generated SQL queries. There are inherent risks in doing this. Make sure that your database connection permissions are always scoped as narrowly as possible for your agent’s needs. This will mitigate, though not eliminate, the risks of building a model-driven system.

### 

[​

](https://docs.langchain.com/oss/python/langchain/sql-agent#concepts)

Concepts

We will cover the following concepts:

- [Tools](https://docs.langchain.com/oss/python/langchain/tools) for reading from SQL databases
- LangChain [agents](https://docs.langchain.com/oss/python/langchain/agents)
- [Human-in-the-loop](https://docs.langchain.com/oss/python/langchain/human-in-the-loop) processes

## 

[​

](https://docs.langchain.com/oss/python/langchain/sql-agent#setup)

Setup

### 

[​

](https://docs.langchain.com/oss/python/langchain/sql-agent#installation)

Installation

pip

```
pip install langchain  langgraph  langchain-community
```

### 

[​

](https://docs.langchain.com/oss/python/langchain/sql-agent#langsmith)

LangSmith

Set up [LangSmith](https://smith.langchain.com/) to inspect what is happening inside your chain or agent. Then set the following environment variables:

```
export LANGSMITH_TRACING="true"
export LANGSMITH_API_KEY="..."
```

## 

[​

](https://docs.langchain.com/oss/python/langchain/sql-agent#1-select-an-llm)

1. Select an LLM

Select a model that supports [tool-calling](https://docs.langchain.com/oss/python/integrations/providers/overview):

- OpenAI

- Anthropic

- Azure

- Google Gemini

- AWS Bedrock

- HuggingFace

👉 Read the [OpenAI chat model integration docs](https://docs.langchain.com/oss/python/integrations/chat/openai)

```
pip install -U "langchain[openai]"
```

init_chat_model

Model Class

```
import os
from langchain.chat_models import init_chat_model

os.environ["OPENAI_API_KEY"] = "sk-..."

model = init_chat_model("gpt-4.1")
```

The output shown in the examples below used OpenAI.

## 

[​

](https://docs.langchain.com/oss/python/langchain/sql-agent#2-configure-the-database)

2. Configure the database

You will be creating a [SQLite database](https://www.sqlitetutorial.net/sqlite-sample-database/) for this tutorial. SQLite is a lightweight database that is easy to set up and use. We will be loading the `chinook` database, which is a sample database that represents a digital media store.For convenience, we have hosted the database (`Chinook.db`) on a public GCS bucket.

```
import requests, pathlib

url = "https://storage.googleapis.com/benchmarks-artifacts/chinook/Chinook.db"
local_path = pathlib.Path("Chinook.db")

if local_path.exists():
    print(f"{local_path} already exists, skipping download.")
else:
    response = requests.get(url)
    if response.status_code == 200:
        local_path.write_bytes(response.content)
        print(f"File downloaded and saved as {local_path}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
```

We will use a handy SQL database wrapper available in the `langchain_community` package to interact with the database. The wrapper provides a simple interface to execute SQL queries and fetch results:

```
from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///Chinook.db")

print(f"Dialect: {db.dialect}")
print(f"Available tables: {db.get_usable_table_names()}")
print(f'Sample output: {db.run("SELECT * FROM Artist LIMIT 5;")}')
```

```
Dialect: sqlite
Available tables: ['Album', 'Artist', 'Customer', 'Employee', 'Genre', 'Invoice', 'InvoiceLine', 'MediaType', 'Playlist', 'PlaylistTrack', 'Track']
Sample output: [(1, 'AC/DC'), (2, 'Accept'), (3, 'Aerosmith'), (4, 'Alanis Morissette'), (5, 'Alice In Chains')]
```

## 

[​

](https://docs.langchain.com/oss/python/langchain/sql-agent#3-add-tools-for-database-interactions)

3. Add tools for database interactions

Use the `SQLDatabase` wrapper available in the `langchain_community` package to interact with the database. The wrapper provides a simple interface to execute SQL queries and fetch results:

```
from langchain_community.agent_toolkits import SQLDatabaseToolkit

toolkit = SQLDatabaseToolkit(db=db, llm=model)

tools = toolkit.get_tools()

for tool in tools:
    print(f"{tool.name}: {tool.description}\n")
```

```
sql_db_query: Input to this tool is a detailed and correct SQL query, output is a result from the database. If the query is not correct, an error message will be returned. If an error is returned, rewrite the query, check the query, and try again. If you encounter an issue with Unknown column 'xxxx' in 'field list', use sql_db_schema to query the correct table fields.

sql_db_schema: Input to this tool is a comma-separated list of tables, output is the schema and sample rows for those tables. Be sure that the tables actually exist by calling sql_db_list_tables first! Example Input: table1, table2, table3

sql_db_list_tables: Input is an empty string, output is a comma-separated list of tables in the database.

sql_db_query_checker: Use this tool to double check if your query is correct before executing it. Always use this tool before executing a query with sql_db_query!
```

## 

[​

](https://docs.langchain.com/oss/python/langchain/sql-agent#4-use-create-agent)

4. Use `create_agent`

Use [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent) to build a [ReAct agent](https://arxiv.org/pdf/2210.03629) with minimal code. The agent will interpret the request and generate a SQL command, which the tools will execute. If the command has an error, the error message is returned to the model. The model can then examine the original request and the new error message and generate a new command. This can continue until the LLM generates the command successfully or reaches an end count. This pattern of providing a model with feedback - error messages in this case - is very powerful.Initialize the agent with a descriptive system prompt to customize its behavior:

```
system_prompt = """
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run,
then look at the results of the query and return the answer. Unless the user
specifies a specific number of examples they wish to obtain, always limit your
query to at most {top_k} results.

You can order the results by a relevant column to return the most interesting
examples in the database. Never query for all the columns from a specific table,
only ask for the relevant columns given the question.

You MUST double check your query before executing it. If you get an error while
executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
database.

To start you should ALWAYS look at the tables in the database to see what you
can query. Do NOT skip this step.

Then you should query the schema of the most relevant tables.
""".format(
    dialect=db.dialect,
    top_k=5,
)
```

Now, create an agent with the model, tools, and prompt:

```
from langchain.agents import create_agent


agent = create_agent(
    model,
    tools,
    system_prompt=system_prompt,
)
```

## 

[​

](https://docs.langchain.com/oss/python/langchain/sql-agent#5-run-the-agent)

5. Run the agent

Run the agent on a sample query and observe its behavior:

```
question = "Which genre on average has the longest tracks?"

for step in agent.stream(
    {"messages": [{"role": "user", "content": question}]},
    stream_mode="values",
):
    step["messages"][-1].pretty_print()
```

```
================================ Human Message =================================

Which genre on average has the longest tracks?
================================== Ai Message ==================================
Tool Calls:
  sql_db_list_tables (call_BQsWg8P65apHc8BTJ1NPDvnM)
 Call ID: call_BQsWg8P65apHc8BTJ1NPDvnM
  Args:
================================= Tool Message =================================
Name: sql_db_list_tables

Album, Artist, Customer, Employee, Genre, Invoice, InvoiceLine, MediaType, Playlist, PlaylistTrack, Track
================================== Ai Message ==================================
Tool Calls:
  sql_db_schema (call_i89tjKECFSeERbuACYm4w0cU)
 Call ID: call_i89tjKECFSeERbuACYm4w0cU
  Args:
    table_names: Track, Genre
================================= Tool Message =================================
Name: sql_db_schema


CREATE TABLE "Genre" (
    "GenreId" INTEGER NOT NULL,
    "Name" NVARCHAR(120),
    PRIMARY KEY ("GenreId")
)

/*
3 rows from Genre table:
GenreId    Name
1    Rock
2    Jazz
3    Metal
*/


CREATE TABLE "Track" (
    "TrackId" INTEGER NOT NULL,
    "Name" NVARCHAR(200) NOT NULL,
    "AlbumId" INTEGER,
    "MediaTypeId" INTEGER NOT NULL,
    "GenreId" INTEGER,
    "Composer" NVARCHAR(220),
    "Milliseconds" INTEGER NOT NULL,
    "Bytes" INTEGER,
    "UnitPrice" NUMERIC(10, 2) NOT NULL,
    PRIMARY KEY ("TrackId"),
    FOREIGN KEY("MediaTypeId") REFERENCES "MediaType" ("MediaTypeId"),
    FOREIGN KEY("GenreId") REFERENCES "Genre" ("GenreId"),
    FOREIGN KEY("AlbumId") REFERENCES "Album" ("AlbumId")
)

/*
3 rows from Track table:
TrackId    Name    AlbumId    MediaTypeId    GenreId    Composer    Milliseconds    Bytes    UnitPrice
1    For Those About To Rock (We Salute You)    1    1    1    Angus Young, Malcolm Young, Brian Johnson    343719    11170334    0.99
2    Balls to the Wall    2    2    1    U. Dirkschneider, W. Hoffmann, H. Frank, P. Baltes, S. Kaufmann, G. Hoffmann    342562    5510424    0.99
3    Fast As a Shark    3    2    1    F. Baltes, S. Kaufman, U. Dirkscneider & W. Hoffman    230619    3990994    0.99
*/
================================== Ai Message ==================================
Tool Calls:
  sql_db_query_checker (call_G64yYm6R6UauiVPCXJZMA49b)
 Call ID: call_G64yYm6R6UauiVPCXJZMA49b
  Args:
    query: SELECT Genre.Name, AVG(Track.Milliseconds) AS AverageLength FROM Track INNER JOIN Genre ON Track.GenreId = Genre.GenreId GROUP BY Genre.Name ORDER BY AverageLength DESC LIMIT 5;
================================= Tool Message =================================
Name: sql_db_query_checker

SELECT Genre.Name, AVG(Track.Milliseconds) AS AverageLength FROM Track INNER JOIN Genre ON Track.GenreId = Genre.GenreId GROUP BY Genre.Name ORDER BY AverageLength DESC LIMIT 5;
================================== Ai Message ==================================
Tool Calls:
  sql_db_query (call_AnO3SrhD0ODJBxh6dHMwvHwZ)
 Call ID: call_AnO3SrhD0ODJBxh6dHMwvHwZ
  Args:
    query: SELECT Genre.Name, AVG(Track.Milliseconds) AS AverageLength FROM Track INNER JOIN Genre ON Track.GenreId = Genre.GenreId GROUP BY Genre.Name ORDER BY AverageLength DESC LIMIT 5;
================================= Tool Message =================================
Name: sql_db_query

[('Sci Fi & Fantasy', 2911783.0384615385), ('Science Fiction', 2625549.076923077), ('Drama', 2575283.78125), ('TV Shows', 2145041.0215053763), ('Comedy', 1585263.705882353)]
================================== Ai Message ==================================

On average, the genre with the longest tracks is "Sci Fi & Fantasy" with an average track length of approximately 2,911,783 milliseconds. This is followed by "Science Fiction," "Drama," "TV Shows," and "Comedy."
```

The agent correctly wrote a query, checked the query, and ran it to inform its final response.

You can inspect all aspects of the above run, including steps taken, tools invoked, what prompts were seen by the LLM, and more in the [LangSmith trace](https://smith.langchain.com/public/cd2ce887-388a-4bb1-a29d-48208ce50d15/r).

### 

[​

](https://docs.langchain.com/oss/python/langchain/sql-agent#optional-use-studio)

(Optional) Use Studio

[Studio](https://docs.langchain.com/langsmith/studio) provides a “client side” loop as well as memory so you can run this as a chat interface and query the database. You can ask questions like “Tell me the scheme of the database” or “Show me the invoices for the 5 top customers”. You will see the SQL command that is generated and the resulting output. The details of how to get that started are below.

Run your agent in Studio

## 

[​

](https://docs.langchain.com/oss/python/langchain/sql-agent#6-implement-human-in-the-loop-review)

6. Implement human-in-the-loop review

It can be prudent to check the agent’s SQL queries before they are executed for any unintended actions or inefficiencies.LangChain agents feature support for built-in [human-in-the-loop middleware](https://docs.langchain.com/oss/python/langchain/human-in-the-loop) to add oversight to agent tool calls. Let’s configure the agent to pause for human review on calling the `sql_db_query` tool:

```
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware 
from langgraph.checkpoint.memory import InMemorySaver 


agent = create_agent(
    model,
    tools,
    system_prompt=system_prompt,
    middleware=[ 
        HumanInTheLoopMiddleware( 
            interrupt_on={"sql_db_query": True}, 
            description_prefix="Tool execution pending approval", 
        ), 
    ], 
    checkpointer=InMemorySaver(), 
)
```

We’ve added a [checkpointer](https://docs.langchain.com/oss/python/langchain/short-term-memory) to our agent to allow execution to be paused and resumed. See the [human-in-the-loop guide](https://docs.langchain.com/oss/python/langchain/human-in-the-loop) for detalis on this as well as available middleware configurations.

On running the agent, it will now pause for review before executing the `sql_db_query` tool:

```
question = "Which genre on average has the longest tracks?"
config = {"configurable": {"thread_id": "1"}} 

for step in agent.stream(
    {"messages": [{"role": "user", "content": question}]},
    config, 
    stream_mode="values",
):
    if "__interrupt__" in step: 
        print("INTERRUPTED:") 
        interrupt = step["__interrupt__"][0] 
        for request in interrupt.value["action_requests"]: 
            print(request["description"]) 
    elif "messages" in step:
        step["messages"][-1].pretty_print()
    else:
        pass
```

```
...

INTERRUPTED:
Tool execution pending approval

Tool: sql_db_query
Args: {'query': 'SELECT g.Name AS Genre, AVG(t.Milliseconds) AS AvgTrackLength FROM Track t JOIN Genre g ON t.GenreId = g.GenreId GROUP BY g.Name ORDER BY AvgTrackLength DESC LIMIT 1;'}
```

We can resume execution, in this case accepting the query, using [Command](https://docs.langchain.com/oss/python/langgraph/use-graph-api#combine-control-flow-and-state-updates-with-command):

```
from langgraph.types import Command 

for step in agent.stream(
    Command(resume={"decisions": [{"type": "approve"}]}), 
    config,
    stream_mode="values",
):
    if "messages" in step:
        step["messages"][-1].pretty_print()
    elif "__interrupt__" in step:
        print("INTERRUPTED:")
        interrupt = step["__interrupt__"][0]
        for request in interrupt.value["action_requests"]:
            print(request["description"])
    else:
        pass
```

```
================================== Ai Message ==================================
Tool Calls:
  sql_db_query (call_7oz86Epg7lYRqi9rQHbZPS1U)
 Call ID: call_7oz86Epg7lYRqi9rQHbZPS1U
  Args:
    query: SELECT Genre.Name, AVG(Track.Milliseconds) AS AvgDuration FROM Track JOIN Genre ON Track.GenreId = Genre.GenreId GROUP BY Genre.Name ORDER BY AvgDuration DESC LIMIT 5;
================================= Tool Message =================================
Name: sql_db_query

[('Sci Fi & Fantasy', 2911783.0384615385), ('Science Fiction', 2625549.076923077), ('Drama', 2575283.78125), ('TV Shows', 2145041.0215053763), ('Comedy', 1585263.705882353)]
================================== Ai Message ==================================

The genre with the longest average track length is "Sci Fi & Fantasy" with an average duration of about 2,911,783 milliseconds, followed by "Science Fiction" and "Drama."
```

Refer to the [human-in-the-loop guide](https://docs.langchain.com/oss/python/langchain/human-in-the-loop) for details.

## 

[​

](https://docs.langchain.com/oss/python/langchain/sql-agent#next-steps)

Next steps

For deeper customization, check out [this tutorial](https://docs.langchain.com/oss/python/langgraph/sql-agent) for implementing a SQL agent directly using LangGraph primitives.



---

# Build a SQL assistant with on-demand skills

Copy page

This tutorial shows how to use **progressive disclosure** - a context management technique where the agent loads information on-demand rather than upfront - to implement **skills** (specialized prompt-based instructions). The agent loads skills via tool calls, rather than dynamically changing the system prompt, discovering and loading only the skills it needs for each task.**Use case:** Imagine building an agent to help write SQL queries across different business verticals in a large enterprise. Your organization might have separate datastores for each vertical, or a single monolithic database with thousands of tables. Either way, loading all schemas upfront would overwhelm the context window. Progressive disclosure solves this by loading only the relevant schema when needed. This architecture also enables different product owners and stakeholders to independently contribute and maintain skills for their specific business verticals.**What you’ll build:** A SQL query assistant with two skills (sales analytics and inventory management). The agent sees lightweight skill descriptions in its system prompt, then loads full database schemas and business logic through tool calls only when relevant to the user’s query.

For a more complete example of a SQL agent with query execution, error correction, and validation, see our [SQL Agent tutorial](https://docs.langchain.com/oss/python/langchain/sql-agent). This tutorial focuses on the progressive disclosure pattern which can be applied to any domain.

Progressive disclosure was popularized by Anthropic as a technique for building scalable agent skills systems. This approach uses a three-level architecture (metadata → core content → detailed resources) where agents load information only as needed. For more on this technique, see [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).

## 

[​

](https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant#how-it-works)

How it works

Here’s the flow when a user asks for a SQL query:

**Why progressive disclosure:**

- **Reduces context usage** - load only the 2-3 skills needed for a task, not all available skills
- **Enables team autonomy** - different teams can develop specialized skills independently (similar to other multi-agent architectures)
- **Scales efficiently** - add dozens or hundreds of skills without overwhelming context
- **Simplifies conversation history** - single agent with one conversation thread

**What are skills:** Skills, as popularized by Claude Code, are primarily prompt-based: self-contained units of specialized instructions for specific business tasks. In Claude Code, skills are exposed as directories with files on the file system, discovered through file operations. Skills guide behavior through prompts and can provide information about tool usage or include sample code for a coding agent to execute.

Skills with progressive disclosure can be viewed as a form of [RAG (Retrieval-Augmented Generation)](https://docs.langchain.com/oss/python/langchain/rag), where each skill is a retrieval unit—though not necessarily backed by embeddings or keyword search, but by tools for browsing content (like file operations or, in this tutorial, direct lookup).

**Trade-offs:**

- **Latency**: Loading skills on-demand requires additional tool calls, which adds latency to the first request that needs each skill
- **Workflow control**: Basic implementations rely on prompting to guide skill usage - you cannot enforce hard constraints like “always try skill A before skill B” without custom logic

**Implementing your own skills system**When building your own skills implementation (as we do in this tutorial), the core concept is progressive disclosure - loading information on-demand. Beyond that, you have full flexibility in implementation:

- **Storage**: databases, S3, in-memory data structures, or any backend
- **Discovery**: direct lookup (this tutorial), RAG for large skill collections, file system scanning, or API calls
- **Loading logic**: customize latency characteristics and add logic to search through skill content or rank relevance
- **Side effects**: define what happens when a skill loads, such as exposing tools associated with that skill (covered in section 8)

This flexibility lets you optimize for your specific requirements around performance, storage, and workflow control.

## 

[​

](https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant#setup)

Setup

### 

[​

](https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant#installation)

Installation

This tutorial requires the `langchain` package:

pip

uv

conda

```
pip install langchain
```

For more details, see our [Installation guide](https://docs.langchain.com/oss/python/langchain/install).

### 

[​

](https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant#langsmith)

LangSmith

Set up [LangSmith](https://smith.langchain.com/) to inspect what is happening inside your agent. Then set the following environment variables:

bash

python

```
export LANGSMITH_TRACING="true"
export LANGSMITH_API_KEY="..."
```

### 

[​

](https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant#select-an-llm)

Select an LLM

Select a chat model from LangChain’s suite of integrations:

- OpenAI

- Anthropic

- Azure

- Google Gemini

- AWS Bedrock

- HuggingFace

👉 Read the [OpenAI chat model integration docs](https://docs.langchain.com/oss/python/integrations/chat/openai)

```
pip install -U "langchain[openai]"
```

init_chat_model

Model Class

```
import os
from langchain.chat_models import init_chat_model

os.environ["OPENAI_API_KEY"] = "sk-..."

model = init_chat_model("gpt-4.1")
```

## 

[​

](https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant#1-define-skills)

1. Define skills

First, define the structure for skills. Each skill has a name, a brief description (shown in the system prompt), and full content (loaded on-demand):

```
from typing import TypedDict

class Skill(TypedDict):  
    """A skill that can be progressively disclosed to the agent."""
    name: str  # Unique identifier for the skill
    description: str  # 1-2 sentence description to show in system prompt
    content: str  # Full skill content with detailed instructions
```

Now define example skills for a SQL query assistant. The skills are designed to be **lightweight in description** (shown to the agent upfront) but **detailed in content** (loaded only when needed):

View complete skill definitions

## 

[​

](https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant#2-create-skill-loading-tool)

2. Create skill loading tool

Create a tool to load full skill content on-demand:

```
from langchain.tools import tool

@tool
def load_skill(skill_name: str) -> str:
    """Load the full content of a skill into the agent's context.

    Use this when you need detailed information about how to handle a specific
    type of request. This will provide you with comprehensive instructions,
    policies, and guidelines for the skill area.

    Args:
        skill_name: The name of the skill to load (e.g., "expense_reporting", "travel_booking")
    """
    # Find and return the requested skill
    for skill in SKILLS:
        if skill["name"] == skill_name:
            return f"Loaded skill: {skill_name}\n\n{skill['content']}"

    # Skill not found
    available = ", ".join(s["name"] for s in SKILLS)
    return f"Skill '{skill_name}' not found. Available skills: {available}"
```

The `load_skill` tool returns the full skill content as a string, which becomes part of the conversation as a ToolMessage. For more details on creating and using tools, see the [Tools guide](https://docs.langchain.com/oss/python/langchain/tools).

## 

[​

](https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant#3-build-skill-middleware)

3. Build skill middleware

Create custom middleware that injects skill descriptions into the system prompt. This middleware makes skills discoverable without loading their full content upfront.

This guide demonstrates creating custom middleware. For a comprehensive guide on middleware concepts and patterns, see the [custom middleware documentation](https://docs.langchain.com/oss/python/langchain/middleware/custom).

```
from langchain.agents.middleware import ModelRequest, ModelResponse, AgentMiddleware
from langchain.messages import SystemMessage
from typing import Callable

class SkillMiddleware(AgentMiddleware):  
    """Middleware that injects skill descriptions into the system prompt."""

    # Register the load_skill tool as a class variable
    tools = [load_skill]  

    def __init__(self):
        """Initialize and generate the skills prompt from SKILLS."""
        # Build skills prompt from the SKILLS list
        skills_list = []
        for skill in SKILLS:
            skills_list.append(
                f"- **{skill['name']}**: {skill['description']}"
            )
        self.skills_prompt = "\n".join(skills_list)

    def wrap_model_call(
        self,
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        """Sync: Inject skill descriptions into system prompt."""
        # Build the skills addendum
        skills_addendum = ( 
            f"\n\n## Available Skills\n\n{self.skills_prompt}\n\n"
            "Use the load_skill tool when you need detailed information "
            "about handling a specific type of request."
        )

        # Append to system message content blocks
        new_content = list(request.system_message.content_blocks) + [
            {"type": "text", "text": skills_addendum}
        ]
        new_system_message = SystemMessage(content=new_content)
        modified_request = request.override(system_message=new_system_message)
        return handler(modified_request)
```

The middleware appends skill descriptions to the system prompt, making the agent aware of available skills without loading their full content. The `load_skill` tool is registered as a class variable, making it available to the agent.

**Production consideration**: This tutorial loads the skill list in `__init__` for simplicity. In a production system, you may want to load skills in the `before_agent` hook instead, allowing them to be refreshed periodically to reflect up-to-date changes (e.g., when new skills are added or existing ones are modified). See the [before_agent hook documentation](https://docs.langchain.com/oss/python/langchain/middleware/custom#before_agent) for details.

## 

[​

](https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant#4-create-the-agent-with-skill-support)

4. Create the agent with skill support

Now create the agent with the skill middleware and a checkpointer for state persistence:

```
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

# Create the agent with skill support
agent = create_agent(
    model,
    system_prompt=(
        "You are a SQL query assistant that helps users "
        "write queries against business databases."
    ),
    middleware=[SkillMiddleware()],  
    checkpointer=InMemorySaver(),
)
```

The agent now has access to skill descriptions in its system prompt and can call `load_skill` to retrieve full skill content when needed. The checkpointer maintains conversation history across turns.

## 

[​

](https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant#5-test-progressive-disclosure)

5. Test progressive disclosure

Test the agent with a question that requires skill-specific knowledge:

```
import uuid

# Configuration for this conversation thread
thread_id = str(uuid.uuid4())
config = {"configurable": {"thread_id": thread_id}}

# Ask for a SQL query
result = agent.invoke(  
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Write a SQL query to find all customers "
                    "who made orders over $1000 in the last month"
                ),
            }
        ]
    },
    config
)

# Print the conversation
for message in result["messages"]:
    if hasattr(message, 'pretty_print'):
        message.pretty_print()
    else:
        print(f"{message.type}: {message.content}")
```

Expected output:

```
================================ Human Message =================================

Write a SQL query to find all customers who made orders over $1000 in the last month
================================== Ai Message ==================================
Tool Calls:
  load_skill (call_abc123)
 Call ID: call_abc123
  Args:
    skill_name: sales_analytics
================================= Tool Message =================================
Name: load_skill

Loaded skill: sales_analytics

# Sales Analytics Schema

## Tables

### customers
- customer_id (PRIMARY KEY)
- name
- email
- signup_date
- status (active/inactive)
- customer_tier (bronze/silver/gold/platinum)

### orders
- order_id (PRIMARY KEY)
- customer_id (FOREIGN KEY -> customers)
- order_date
- status (pending/completed/cancelled/refunded)
- total_amount
- sales_region (north/south/east/west)

[... rest of schema ...]

## Business Logic

**High-value orders**: Orders with `total_amount > 1000`
**Revenue calculation**: Only count orders with `status = 'completed'`

================================== Ai Message ==================================

Here's a SQL query to find all customers who made orders over $1000 in the last month:

\`\`\`sql
SELECT DISTINCT
    c.customer_id,
    c.name,
    c.email,
    c.customer_tier
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.total_amount > 1000
  AND o.status = 'completed'
  AND o.order_date >= CURRENT_DATE - INTERVAL '1 month'
ORDER BY c.customer_id;
\`\`\`

This query:
- Joins customers with their orders
- Filters for high-value orders (>$1000) using the total_amount field
- Only includes completed orders (as per the business logic)
- Restricts to orders from the last month
- Returns distinct customers to avoid duplicates if they made multiple qualifying orders
```

The agent saw the lightweight skill description in its system prompt, recognized the question required sales database knowledge, called `load_skill("sales_analytics")` to get the full schema and business logic, and then used that information to write a correct query following the database conventions.

## 

[​

](https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant#6-advanced-add-constraints-with-custom-state)

6. Advanced: Add constraints with custom state

Optional: Track loaded skills and enforce tool constraints

### 

[

](https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant#define-custom-state)

### 

[

](https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant#update-load-skill-to-modify-state)

### 

[

](https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant#create-constrained-tool)

### 

[

](https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant#update-middleware-and-agent)

## 

[​

](https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant#complete-example)

Complete example

View complete runnable script

## 

[​

](https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant#implementation-variations)

Implementation variations

View implementation options and trade-offs

## 

[​

](https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant#progressive-disclosure-and-context-engineering)

Progressive disclosure and context engineering

Combining with few-shot prompting and other techniques

**[](https://docs.langchain.com/oss/python/langchain/context-engineering)**

### 

[

](https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant#combining-with-few-shot-prompting)

## 

[​

](https://docs.langchain.com/oss/python/langchain/multi-agent/skills-sql-assistant#next-steps)

Next steps

- Learn about [middleware](https://docs.langchain.com/oss/python/langchain/middleware) for more dynamic agent behaviors
- Explore [context engineering](https://docs.langchain.com/oss/python/langchain/context-engineering) techniques for managing agent context
- Explore the [handoffs pattern](https://docs.langchain.com/oss/python/langchain/multi-agent/handoffs-customer-support) for sequential workflows
- Read the [subagents pattern](https://docs.langchain.com/oss/python/langchain/multi-agent/subagents-personal-assistant) for parallel task routing
- See [multi-agent patterns](https://docs.langchain.com/oss/python/langchain/multi-agent) for other approaches to specialized agents
- Use [LangSmith](https://smith.langchain.com/) to debug and monitor skill loading

# SQLite integrations

Copy page

Integrate with SQLite using LangChain Python.

> [SQLite](https://en.wikipedia.org/wiki/SQLite) is a database engine written in the C programming language. It is not a standalone app; rather, it is a library that software developers embed in their apps. As such, it belongs to the family of embedded databases. It is the most widely deployed database engine, as it is used by several of the top web browsers, operating systems, mobile phones, and other embedded systems.

## 

[​

](https://docs.langchain.com/oss/python/integrations/providers/sqlite#installation-and-setup)

Installation and setup

We need to install the `SQLAlchemy` python package.

pip

uv

```
pip install SQLAlchemy
```

## 

[​

](https://docs.langchain.com/oss/python/integrations/providers/sqlite#vector-store)

Vector store

See a [usage example](https://docs.langchain.com/oss/python/integrations/vectorstores/sqlitevec).

```
from langchain_community.vectorstores import SQLiteVec
from langchain_community.vectorstores import SQLiteVSS # legacy


```

---

# Connect to an external PostgreSQL database

Copy page

LangSmith uses a PostgreSQL database as the primary data store for transactional workloads and operational data (almost everything besides runs). By default, LangSmith Self-Hosted will use an internal PostgreSQL database. However, you can configure LangSmith to use an external PostgreSQL database. By configuring an external PostgreSQL database, you can more easily manage backups, scaling, and other operational tasks for your database.

**If you’re using a managed PostgreSQL service**, we recommend:

- [Amazon RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.PostgreSQL.html) (AWS)
- [Google Cloud SQL](https://cloud.google.com/curated-resources/cloud-sql#section-1) (GCP)
- [Azure Database for PostgreSQL](https://azure.microsoft.com/en-us/products/postgresql#features) (Azure)

For cloud-specific IAM/Workload Identity authentication, refer to the [IAM authentication section](https://docs.langchain.com/langsmith/self-host-external-postgres#iam-authentication).

## 

[​

](https://docs.langchain.com/langsmith/self-host-external-postgres#requirements)

Requirements

- A provisioned PostgreSQL database that your LangSmith instance will have network access to. We recommend using a managed PostgreSQL service like:
  - [Amazon RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.PostgreSQL.html)
  - [Google Cloud SQL](https://cloud.google.com/curated-resources/cloud-sql#section-1)
  - [Azure Database for PostgreSQL](https://azure.microsoft.com/en-us/products/postgresql#features)
- Note: We only officially support PostgreSQL versions >= 14.
- We support password and [IAM/Workload Identity](https://docs.langchain.com/langsmith/self-host-external-postgres#iam-authentication) authentication.
- A user with admin access to the PostgreSQL database. This user will be used to create the necessary tables, indexes, and schemas.
- This user will also need to have the ability to create extensions in the database. We use/will try to install the `btree_gin`, `btree_gist`, `pgcrypto`, `citext`, `ltree`, and `pg_trgm` extensions.
- If using a schema other than public, ensure that you do not have any other schemas with the extensions enabled, or you must include that in your search path.
- Support for pgbouncer and other connection poolers is community-based. Community members have reported that pgbouncer has worked with `pool_mode` = `session` and a suitable setting for `ignore_startup_parameters` (as of writing, `search_path` and `lock_timeout` need to be ignored). Care is needed to avoid polluting connection pools; some level of PostgreSQL expertise is advisable. LangChain Inc currently does not have roadmap plans for formal test coverage or commercial support of pgbouncer or amazon rds proxy or any other poolers, but the community is welcome to discuss and collaborate on support through GitHub issues.
- By default, we recommend an instance with **at least 2 vCPUs and 8GB of memory**. However, the actual requirements will depend on your workload and the number of users you have. We recommend monitoring your PostgreSQL instance and scaling up as needed.

## 

[​

](https://docs.langchain.com/langsmith/self-host-external-postgres#connection-string)

Connection string

You will need to provide a connection string to your PostgreSQL database. This connection string should include the following information:

- Host
- Port
- Database
- Username
- Password (Make sure to url encode this if there are any special characters) - **Note:** When using IAM authentication, the password is not required in the connection string. More below.
- URL params

This will take the form of:

```
username:password@host:port/database?<url_params>
```

An example connection string might look like:

```
myuser:mypassword@myhost:5432/mydatabase?sslmode=disable
```

Without url parameters, the connection string would look like:

```
myuser:mypassword@myhost:5432/mydatabase
```

For IAM authentication, omit the password and use the identity name as the username:

```
my-workload-identity@myhost:5432/mydatabase?sslmode=require
```

## 

[​

](https://docs.langchain.com/langsmith/self-host-external-postgres#configuration)

Configuration

With your connection string in hand, you can configure your LangSmith instance to use an external PostgreSQL database. You can do this by modifying the `values` file for your LangSmith Helm Chart installation or the `.env` file for your Docker installation.

Helm

Docker

```
postgres:
  external:
    enabled: true
    connectionUrl: "Your connection url"
```

Once configured, you should be able to reinstall your LangSmith instance. If everything is configured correctly, your LangSmith instance should now be using your external PostgreSQL database.

## 

[​

](https://docs.langchain.com/langsmith/self-host-external-postgres#tls-with-postgresql)

TLS with PostgreSQL

Use this section to configure TLS for PostgreSQL connections. For mounting internal/public CAs so LangSmith trusts your PostgreSQL server certificate, see [Configure custom TLS certificates](https://docs.langchain.com/langsmith/self-host-custom-tls-certificates#mount-internal-cas-for-tls).

### 

[​

](https://docs.langchain.com/langsmith/self-host-external-postgres#server-tls-one-way)

Server TLS (one-way)

To validate the PostgreSQL server certificate:

- Provide a CA bundle using `config.customCa.secretName` and `config.customCa.secretKey`.
- Use `sslmode=require` or `sslmode=verify-full`, as well as `sslrootcert=system` to your connection URL.

Mount a custom CA only when your PostgreSQL server uses an internal or private CA. Publicly trusted CAs do not require this configuration.

Helm (server TLS)

Kubernetes Secret (CA bundle)

```
config:
  customCa:
    secretName: "langsmith-custom-ca"  # Secret containing your CA bundle
    secretKey: "ca.crt"    # Key in the Secret with the CA bundle
postgres:
  external:
    enabled: true
    connectionUrl: "myuser:mypassword@myhost:5432/mydatabase?sslmode=verify-full&sslrootcert=system"
    customTls: true
```

### 

[​

](https://docs.langchain.com/langsmith/self-host-external-postgres#mutual-tls-with-client-auth-mtls)

Mutual TLS with client auth (mTLS)

As of LangSmith helm chart version **0.12.29**, we support mTLS for PostgreSQL clients. For server-side authentication in mTLS, use the [Server TLS steps](https://docs.langchain.com/langsmith/self-host-external-postgres#server-tls-one-way) (custom CA) in addition to the following client certificate configuration.If your PostgreSQL server requires client certificate authentication:

- Provide a Secret with your client certificate and key.
- Reference it via `postgres.external.clientCert.secretName` and specify the keys with `certSecretKey` and `keySecretKey`.
- Use `sslmode=verify-full` and `sslrootcert=system` in your connection URL.

Helm (client Auth)

Kubernetes Secret (client cert/key)

```
postgres:
  external:
    enabled: true
    connectionUrl: "myuser:mypassword@myhost:5432/mydatabase?sslmode=verify-full&sslrootcert=system"
    customTls: true
    clientCert:
      secretName: "postgres-mtls-secret"
      certSecretKey: "tls.crt"
      keySecretKey: "tls.key"
```

#### 

[​

](https://docs.langchain.com/langsmith/self-host-external-postgres#pod-security-context-for-certificate-volumes)

Pod security context for certificate volumes

The certificate volumes mounted for mTLS are protected by file access restrictions. To ensure all LangSmith pods can read the certificate files, you must set `fsGroup: 1000` in the pod security context.You can configure this in one of two ways:**Option 1: Use `commonPodSecurityContext`**Set the `fsGroup` at the top level to apply it to all pods:

```
commonPodSecurityContext:
  fsGroup: 1000
```

**Option 2: Add to individual pod security contexts**If you need more granular control, add the `fsGroup` to each pod’s security context individually. See the [mTLS configuration example](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/examples/mtls_config.yaml) for a complete reference.

## 

[​

](https://docs.langchain.com/langsmith/self-host-external-postgres#iam-authentication)

IAM authentication

As of LangSmith helm chart version **0.12.34**, we support IAM authentication for PostgreSQL. This allows you to use cloud provider workload identity instead of static passwords.

IAM authentication only handles connection authentication. You may still need to run SQL commands in your database to create the IAM user/role and grant it the necessary permissions and privileges to access the LangSmith schema.

- AWS

- GCP

- Azure

### 

[​

](https://docs.langchain.com/langsmith/self-host-external-postgres#amazon-rds-iam-authentication)

Amazon RDS IAM authentication

Amazon RDS supports [IAM database authentication](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html), which allows you to authenticate to your PostgreSQL instance using AWS IAM credentials instead of database passwords.

#### 

[​

](https://docs.langchain.com/langsmith/self-host-external-postgres#prerequisites)

Prerequisites

1. **Configure workload identity** in your Kubernetes cluster using [AWS IRSA](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) or [EKS Pod Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html)
2. **Enable IAM authentication** on your RDS PostgreSQL instance and grant access to your workload identity

#### 

[​

](https://docs.langchain.com/langsmith/self-host-external-postgres#configuration-2)

Configuration

If you switch to a new IAM user after LangSmith has already run initial migrations, you may need to transfer ownership of existing tables to the new IAM user. Otherwise, migrations may fail due to insufficient privileges on tables owned by the previous user.

Set the `iamAuthProvider` to `"aws"` and provide an IAM-compatible connection string (without password):

```
postgres:
  external:
    enabled: true
    existingSecretName: "postgres-secret"
    iamAuthProvider: "aws"
```

```
apiVersion: v1
kind: Secret
metadata:
  name: postgres-secret
type: Opaque
stringData:
  # IAM connection URL - note no password, username is the IAM identity name
  connection_url: "<iam-identity-name>@<rds-host>:5432/<database>?sslmode=require"
```

IAM authentication requires TLS. You must include `sslmode=require` in your connection string.

#### 

[​

](https://docs.langchain.com/langsmith/self-host-external-postgres#required-annotations)

Required annotations

You must apply the ServiceAccount annotations required by AWS IRSA to all LangSmith components that connect to PostgreSQL:**Deployments:** `backend`, `queue`, `platformBackend`, `hostBackend`, `ingestQueue`**Jobs:** `migrations`, `authBootstrap`, `feedbackConfigMigration`, `feedbackDataMigration`, `e2eTest`

All jobs listed above (except `e2eTest`) use the `backend` service account. The `e2eTest` job uses its own service account and requires separate annotation configuration.

Example configuration for the backend service:

```
backend:
  serviceAccount:
    annotations:
      eks.amazonaws.com/role-arn: "arn:aws:iam::<account-id>:role/<role-name>"

queue:
  serviceAccount:
    annotations:
      eks.amazonaws.com/role-arn: "arn:aws:iam::<account-id>:role/<role-name>"

platformBackend:
  serviceAccount:
    annotations:
      eks.amazonaws.com/role-arn: "arn:aws:iam::<account-id>:role/<role-name>"

hostBackend:
  serviceAccount:
    annotations:
      eks.amazonaws.com/role-arn: "arn:aws:iam::<account-id>:role/<role-name>"

ingestQueue:
  serviceAccount:
    annotations:
      eks.amazonaws.com/role-arn: "arn:aws:iam::<account-id>:role/<role-name>"
```

See the [Helm values reference](https://github.com/langchain-ai/helm/blob/main/charts/langsmith/values.yaml) for the full list of configurable services.

---
