import os
import json
import logging
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Problem, CheatSheet, User, UserSettings
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_database(db: Session = None):
    should_close = False
    if db is None:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        should_close = True

    try:
        # 1. Seed Problems
        problems_file = os.path.join(settings.DATA_DIR, "problems.json")
        if os.path.exists(problems_file):
            with open(problems_file, "r", encoding="utf-8") as f:
                problems_data = json.load(f)

            existing_count = db.query(Problem).count()
            logger.info(f"Existing problems in DB: {existing_count}")
            
            existing_numbers = {p.number for p in db.query(Problem.number).all()}
            to_insert = []

            for p in problems_data:
                if p["number"] not in existing_numbers:
                    to_insert.append(
                        Problem(
                            number=p["number"],
                            title=p["title"],
                            difficulty=p["difficulty"],
                            topic=p["topic"],
                            pattern=p.get("pattern", ""),
                            similar_to=p.get("similar_to", ""),
                            url=p.get("url", f"https://leetcode.com/problems/{p['title'].lower().replace(' ', '-')}/")
                        )
                    )
            
            if to_insert:
                db.bulk_save_objects(to_insert)
                db.commit()
                logger.info(f"Inserted {len(to_insert)} new problems into DB.")
            else:
                logger.info("All problems already seeded.")

        # 2. Seed CheatSheets
        cheatsheets_dir = os.path.join(settings.DATA_DIR, "cheatsheets")
        if os.path.exists(cheatsheets_dir):
            for filename in os.listdir(cheatsheets_dir):
                if filename.endswith(".json"):
                    file_path = os.path.join(cheatsheets_dir, filename)
                    with open(file_path, "r", encoding="utf-8") as f:
                        cs_data = json.load(f)

                    topic = cs_data.get("topic")
                    if not topic:
                        continue

                    existing_cs = db.query(CheatSheet).filter(CheatSheet.topic == topic).first()
                    if existing_cs:
                        existing_cs.content = cs_data
                    else:
                        new_cs = CheatSheet(topic=topic, content=cs_data)
                        db.add(new_cs)

            db.commit()
            logger.info("Cheat sheets seeded/updated successfully.")

    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}")
        raise e
    finally:
        if should_close:
            db.close()

if __name__ == "__main__":
    seed_database()
