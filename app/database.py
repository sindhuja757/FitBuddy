from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./fitbuddy.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    weight = Column(Float)
    goal = Column(String)
    intensity = Column(String)


class WorkoutPlan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    original_plan = Column(Text)
    updated_plan = Column(Text)


Base.metadata.create_all(bind=engine)


def save_user(user_id, name, age, weight, goal, intensity):
    db = SessionLocal()
    try:
        u = db.query(User).filter(User.id == user_id).first()
        if u:
            u.name, u.age, u.weight, u.goal, u.intensity = name, age, weight, goal, intensity
        else:
            db.add(User(id=user_id, name=name, age=age, weight=weight, goal=goal, intensity=intensity))
        db.commit()
    finally:
        db.close()


def save_plan(user_id, plan):
    db = SessionLocal()
    try:
        db.add(WorkoutPlan(user_id=user_id, original_plan=plan))
        db.commit()
    finally:
        db.close()


def update_plan(user_id, updated):
    db = SessionLocal()
    try:
        p = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
        if p:
            p.updated_plan = updated
        else:
            db.add(WorkoutPlan(user_id=user_id, original_plan="", updated_plan=updated))
        db.commit()
    finally:
        db.close()


def get_original_plan(user_id):
    db = SessionLocal()
    try:
        p = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user_id).first()
        return p.original_plan if p else None
    finally:
        db.close()


def get_all_users_with_plans():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        result = []
        for u in users:
            p = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == u.id).first()
            result.append({
                "id": u.id, "name": u.name, "age": u.age, "weight": u.weight,
                "goal": u.goal, "intensity": u.intensity,
                "original_plan": p.original_plan if p else "N/A",
                "updated_plan": p.updated_plan if p and p.updated_plan else "Not updated"
            })
        return result
    finally:
        db.close()