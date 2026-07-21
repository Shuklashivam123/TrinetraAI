from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine,Column,Integer,String,Text,DateTime

Path("data").mkdir(exist_ok=True)

DATABASE_URL="sqlite:///data/chatbot_memory.db"

engine=create_engine(DATABASE_URL,connect_args={"check_same_thread":False})

SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)
Base=declarative_base()

# Part 2 Tables

class Conversation(Base):
    __tablename__="conversations"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Unique conversation/thread id
    thread_id = Column(String, unique=True, index=True)

    # Chat title shown in sidebar
    title = Column(String, default="New Chat")

    # Conversation creation time
    created_at = Column(DateTime, default=datetime.utcnow)

    # Last updated time
    updated_at = Column(DateTime, default=datetime.utcnow)

# ==========================
# Chat Messages Table
# Stores every user and AI message
# ==========================
class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)

    # Which conversation this message belongs to
    thread_id = Column(String, index=True)

    # Message sender ("user" or "assistant")
    role = Column(String)

    # Actual message text
    content = Column(Text)

    # Message timestamp
    created_at = Column(DateTime, default=datetime.utcnow)



# ==========================
# Long Term Memory Table
# Stores user preferences/facts permanently
# ==========================
class LongTermMemory(Base):
    __tablename__ = "long_term_memory"

    id = Column(Integer, primary_key=True, index=True)

    # Conversation/User identifier
    thread_id = Column(String, index=True)

    # Saved memory text
    memory = Column(Text)

    # Memory creation time
    created_at = Column(DateTime, default=datetime.utcnow)



def init_db():
    Base.metadata.create_all(bind=engine)



def create_or_update_conversation(thread_id:str,first_message:str|None=None):
    db=SessionLocal()

    try:
        conversation=(
            db.query(Conversation).filter(Conversation.thread_id==thread_id).first()
        )

        if not conversation:
            title="New Chat"

            if first_message:
                title=first_message.strip()[:40]

                if len(first_message.strip())>40:
                    title=title + "..."

            conversation=Conversation(
                thread_id=thread_id,
                title=title,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            db.add(conversation)
        else:
            conversation.updated_at=datetime.utcnow()

        db.commit()

    finally:
        db.close()




def list_conversations():
    db=SessionLocal()

    try:
        return(
            db.query(Conversation).order_by(Conversation.updated_at.desc()).all()
        )

    finally:
        db.close()





def save_chat_message(thread_id:str,role:str,content:str):
    db=SessionLocal()

    try:
        msg=ChatMessage(
            thread_id=thread_id,
            role=role,
            content=content,
            created_at=datetime.utcnow()
        )

        db.add(msg)

        conversation=(
            db.query(Conversation).filter(Conversation.thread_id==thread_id).first()
        )

        if conversation:
            conversation.updated_at=datetime.utcnow()

        db.commit()

    finally:
        db.close()





def get_chat_history(thread_id:str):
    db=SessionLocal()

    try:
        db.query(ChatMessage).filter(ChatMessage.thread_id==thread_id).order_by(ChatMessage.created_at.asc().all())

    finally:
        db.close()



def save_memory(thread_id:str,memory:str):
    db=SessionLocal()

    try:
        item=LongTermMemory(
            thread_id=thread_id,
            memory=memory,
            created_at=datetime.utcnow()
        )

        db.add(item)

        db.commit()

        return "Memory saved successfully. . ."

    finally:
        db.close()




# Retrieve saved memories
def search_memory(thread_id: str, query: str):

    db = SessionLocal()

    try:

        # Get latest 20 memories for this thread
        memories = (
            db.query(LongTermMemory)
            .filter(LongTermMemory.thread_id == thread_id)
            .order_by(LongTermMemory.created_at.desc())
            .limit(20)
            .all()
        )

        if not memories:
            return "No saved memory found."

        # Return memories as bullet list
        return "\n".join([f"- {m.memory}" for m in memories])

    finally:
        db.close()