import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Index, func, text
from sqlalchemy.orm import relationship

from .engine import Base


class JobStatus(str, enum.Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    FAILED = "Failed"


class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(JobStatus, name="job_status"), nullable=False, default=JobStatus.PENDING)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    depends_on = Column(Integer, ForeignKey("jobs.job_id"), nullable=True)
    dependency = relationship("Job", remote_side=[job_id], uselist=False)

    __table_args__ = (
        # partial index to get pending jobs
        Index(
            "ix_jobs_pending_created_at_asc",
            created_at.asc(),
            postgresql_where=text("status = 'PENDING'")
        ),
        Index("ix_jobs_depends_on", "depends_on"),
    )
    

    