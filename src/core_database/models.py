from sqlalchemy import Column, Integer, String, DateTime, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

learning_pack_syllabus = Table(
    "learning_pack_syllabus",
    Base.metadata,
    Column("learning_pack_id", Integer, ForeignKey("learning_packs.id")),
    Column("syllabus_point_id", Integer, ForeignKey("syllabus_points.id")),
)

learning_pack_resources = Table(
    "learning_pack_resources",
    Base.metadata,
    Column("learning_pack_id", Integer, ForeignKey("learning_packs.id")),
    Column("resource_id", Integer, ForeignKey("resources.id")),
)

mock_exam_questions = Table(
    "mock_exam_questions",
    Base.metadata,
    Column("mock_exam_id", Integer, ForeignKey("mock_exams.id")),
    Column("question_id", Integer, ForeignKey("questions.id")),
)

class Student(Base):
    """Represents a user of the system."""
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Resource(Base):
    """Represents a single educational file."""
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    year = Column(Integer)
    paper = Column(Integer)
    variant = Column(Integer)
    type = Column(String)
    path = Column(String, unique=True, index=True)
    last_seen = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class SyllabusPoint(Base):
    """A trackable item from a subject's syllabus."""
    __tablename__ = "syllabus_points"
    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    code = Column(String, unique=True, index=True)
    description = Column(String)

class LearningPack(Base):
    """A collection of resources for a study session."""
    __tablename__ = "learning_packs"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    syllabus_points = relationship("SyllabusPoint", secondary=learning_pack_syllabus)
    resources = relationship("Resource", secondary=learning_pack_resources)

class Question(Base):
    """Represents a single question from a past paper."""
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    resource_id = Column(Integer, ForeignKey("resources.id")) # From which past paper
    question_number = Column(String) # e.g., "1a", "2b(i)"
    max_marks = Column(Integer)

class MockExam(Base):
    """A generated test paper for a student."""
    __tablename__ = "mock_exams"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    questions = relationship("Question", secondary=mock_exam_questions)

class ExamAttempt(Base):
    """A student's submission for a mock exam."""
    __tablename__ = "exam_attempts"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    mock_exam_id = Column(Integer, ForeignKey("mock_exams.id"))
    score = Column(Float)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

class AttemptedQuestion(Base):
    """Represents a student's answer to a single question in an exam attempt."""
    __tablename__ = "attempted_questions"
    id = Column(Integer, primary_key=True, index=True)
    exam_attempt_id = Column(Integer, ForeignKey("exam_attempts.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    score = Column(Float)
    diagnosed_weakness = Column(String)
