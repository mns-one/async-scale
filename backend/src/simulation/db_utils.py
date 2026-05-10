import random

from sqlalchemy.orm import Session

from ..database.engine import SessionLocal
from ..database.models import Job, JobStatus


def create_random_jobs(size: int) -> int:
    # Create jobs with optional random dependencies
    if size <= 0:
        return 0

    created_count = 0
    db: Session = SessionLocal()
    try:
        # Get job_ids from db so dependencies only point to existing jobs
        existing_ids = [row[0] for row in db.query(Job.job_id).all()]

        for _ in range(size):
            depends_on = None
            # Use random to pick existing job dependency
            roll = random.randint(1, 100)
            if existing_ids and roll % 5 == 0:
                depends_on = random.choice(existing_ids)

            job = Job(status=JobStatus.PENDING, depends_on=depends_on)
            db.add(job)

            db.flush()
            existing_ids.append(job.job_id)
            created_count += 1

        db.commit()
        return created_count
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def clear_jobs() -> int:
    # To clear the jobs table
    db: Session = SessionLocal()
    try:
        deleted_count = db.query(Job).delete(synchronize_session=False)
        db.commit()
        return deleted_count
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
