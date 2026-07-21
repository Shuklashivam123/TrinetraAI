# ============================================================
# PART 1: Database Configuration
# ------------------------------------------------------------
# - Create the data folder if it doesn't exist.
# - Configure the SQLite database path.
# - Create the database connection (engine).
# - Create a Session factory for database operations.
# - Create the Base class for ORM models.
# ============================================================

# ============================================================
# PART 2: Database Tables (ORM Models)
# ------------------------------------------------------------
# Define all database tables using SQLAlchemy ORM:
#
# 1. Conversation
#    -> Stores chat/conversation details.
#
# 2. ChatMessage
#    -> Stores every user and assistant message.
#
# 3. LongTermMemory
#    -> Stores user preferences and important facts.
# ============================================================

# ============================================================
# PART 3: Database Initialization
# ------------------------------------------------------------
# Create all tables in the database if they don't already exist.
# This function should be called once when the application starts.
# ============================================================

# ============================================================
# PART 4: CRUD Operations
# ------------------------------------------------------------
# Functions used to interact with the database:
#
# - create_or_update_conversation()
# - list_conversations()
# - save_chat_message()
# - get_chat_history()
#
# These functions Create, Read and Update chat data.
# ============================================================


# ============================================================
# PART 5: Long-Term Memory Operations
# ------------------------------------------------------------
# Functions responsible for storing and retrieving
# long-term user memories.
#
# - save_memory()
# - search_memory()
# ============================================================




# File structure kuch aisa dikhega:-

# PART 1
imports...
engine...
SessionLocal...

# PART 2
class Conversation...
class ChatMessage...
class LongTermMemory...

# PART 3
init_db()

# PART 4
create_or_update_conversation()
list_conversations()
save_chat_message()
get_chat_history()

# PART 5
save_memory()
search_memory()





# All are the sme steps as above

database.py

PART 1 → Database Setup
↓
SQLite + Engine + Session + Base

PART 2 → Models (Tables)
↓
Conversation
ChatMessage
LongTermMemory

PART 3 → Initialize Database
↓
init_db()

PART 4 → Chat CRUD
↓
Create Conversation
Save Message
Get History
List Conversations

PART 5 → Long-Term Memory
↓
Save Memory
Recall/Search Memory