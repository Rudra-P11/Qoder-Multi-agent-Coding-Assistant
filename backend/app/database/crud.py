from app.database.database import SessionLocal
from app.database import models


def create_session(session_id, prompt):

    db = SessionLocal()

    session = models.Session(
        id=session_id,
        prompt=prompt
    )

    db.add(session)
    db.commit()

    db.close()


def store_message(session_id, role, content):

    db = SessionLocal()

    msg = models.Message(
        session_id=session_id,
        role=role,
        content=content
    )

    db.add(msg)
    db.commit()

    db.close()


def store_plan(session_id, steps):

    db = SessionLocal()

    for step in steps:

        plan = models.Plan(
            session_id=session_id,
            step=step
        )

        db.add(plan)

    db.commit()

    db.close()


def store_event(session_id, agent, message, data):

    db = SessionLocal()

    event = models.TimelineEvent(
        session_id=session_id,
        agent=agent,
        message=message,
        data=str(data)
    )

    db.add(event)
    db.commit()

    db.close()