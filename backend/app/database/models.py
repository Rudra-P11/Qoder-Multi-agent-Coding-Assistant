from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Session(Base):

    __tablename__ = "sessions"

    id = Column(String, primary_key=True)

    prompt = Column(Text)


class Message(Base):

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(String, ForeignKey("sessions.id"))

    role = Column(String)

    content = Column(Text)


class Plan(Base):

    __tablename__ = "plans"

    id = Column(Integer, primary_key=True)

    session_id = Column(String)

    step = Column(Text)


class TimelineEvent(Base):

    __tablename__ = "timeline_events"

    id = Column(Integer, primary_key=True)

    session_id = Column(String)

    agent = Column(String)

    message = Column(Text)

    data = Column(Text)