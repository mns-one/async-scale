import random

from .errors import DatabaseError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, aliased
from sqlalchemy import or_, and_, exists, text

from ..database.engine import SessionLocal
from ..database.models import Job, JobStatus

def create_random_jobs(size: int) -> int:
    # create jobs with optional random dependencies
    if size <= 0:
        return 0

    created_count = 0
    db: Session = SessionLocal()
    try:
        # only allow dependencies on jobs that are not FAILED
        eligible_ids = [
            row[0]
            for row in db.query(Job.job_id)
            .filter(Job.status != JobStatus.FAILED)
            .all()
        ]

        for _ in range(size):
            depends_on = None
            # use random to pick existing job dependency
            roll = random.randint(1, 100)
            if eligible_ids and roll % 5 == 0:
                depends_on = random.choice(eligible_ids)

            job = Job(status=JobStatus.PENDING, depends_on=depends_on)
            db.add(job)

            db.flush()
            eligible_ids.append(job.job_id)
            created_count += 1

        db.commit()
        return created_count
    
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError(
            f"Failed create_random_jobs in DB"
        ) from e
    finally:
        db.close()


def clear_jobs() -> int:
    # to clear the jobs table
    db: Session = SessionLocal()
    try:
        deleted_count = db.query(Job).delete(synchronize_session=False)
        db.commit()
        return deleted_count
    
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError(
            f"Failed clear_jobss in DB"
        ) from e
    finally:
        db.close()


def claim_pending_job() -> int:
    # fetch one pending job and update status to processing
    db: Session = SessionLocal()
    try:
        dep = aliased(Job)
        
        job = (
            db.query(Job)
            .filter(Job.status == JobStatus.PENDING)
            .filter(
                or_(
                    Job.depends_on.is_(None),
                    exists().where(
                        and_(
                            dep.job_id == Job.depends_on,
                            dep.status == JobStatus.COMPLETED,
                        )
                    ),
                )
            )
            .order_by(Job.created_at.asc())
            .with_for_update(skip_locked=True)
            .first()
        )
        if not job:
            db.rollback()
            return -1

        job.status = JobStatus.PROCESSING
        db.commit()
        return job.job_id
    
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError(
            f"Failed claim_pending_job in DB"
        ) from e
    finally:
        db.close()


def mark_job_completed(job_id: int, is_success: bool) -> bool:
    # mark a job based on execution outcome
    status = JobStatus.COMPLETED if is_success else JobStatus.FAILED

    db: Session = SessionLocal()
    try:
        updated_count = (
            db.query(Job)
            .filter(Job.job_id == job_id)
            .update({Job.status: status}, synchronize_session=False)
        )
        if updated_count == 0:
            db.rollback()
            return False

        db.commit()
        return True
    
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError(
            f"Failed mark_job_completed in DB"
        ) from e
    finally:
        db.close()
        

def mark_dependent_jobs_failed(job_id: int) -> int:
    # mark pending descendant jobs as failed (excluding root job itself)
    db: Session = SessionLocal()
    try:
        sql = text("""
            WITH RECURSIVE descendants AS (
                -- direct children of root job
                SELECT j.job_id
                FROM jobs j
                WHERE j.depends_on = :root_job_id

                UNION

                -- recursive descendants
                SELECT c.job_id
                FROM jobs c
                JOIN descendants d
                    ON c.depends_on = d.job_id
            )

            UPDATE jobs AS target
            SET status = 'FAILED',
                updated_at = now()
            WHERE target.job_id IN (
                SELECT job_id
                FROM descendants
            )
              AND target.status = 'PENDING'
            RETURNING target.job_id;
        """)

        result = db.execute(sql, {"root_job_id": job_id})
        updated_count = len(result.fetchall())
        db.commit()

        return updated_count
    
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError(
            f"Failed mark_dependent_jobs_failed in DB"
        ) from e
    finally:
        db.close()
