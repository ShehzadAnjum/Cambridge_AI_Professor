from sqlalchemy.orm import Session
from . import models

# Resource CRUD
def get_resource_by_path(db: Session, path: str):
    """
    Get a resource by its file path.

    Args:
        db: The database session.
        path: The file path of the resource.

    Returns:
        The resource object if found, otherwise None.
    """
    return db.query(models.Resource).filter(models.Resource.path == path).first()

def create_resource(db: Session, resource: dict):
    """
    Create a new resource.

    Args:
        db: The database session.
        resource: A dictionary containing the resource's data.

    Returns:
        The newly created resource object.
    """
    db_resource = models.Resource(**resource)
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

# Student CRUD
def get_student_by_username(db: Session, username: str):
    """
    Get a student by their username.

    Args:
        db: The database session.
        username: The student's username.

    Returns:
        The student object if found, otherwise None.
    """
    return db.query(models.Student).filter(models.Student.username == username).first()

def create_student(db: Session, username: str):
    """
    Create a new student.

    Args:
        db: The database session.
        username: The student's username.

    Returns:
        The newly created student object.
    """
    db_student = models.Student(username=username)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# SyllabusPoint CRUD
def create_syllabus_point(db: Session, syllabus_point: dict):
    """
    Create a new syllabus point.

    Args:
        db: The database session.
        syllabus_point: A dictionary containing the syllabus point's data.

    Returns:
        The newly created syllabus point object.
    """
    db_syllabus_point = models.SyllabusPoint(**syllabus_point)
    db.add(db_syllabus_point)
    db.commit()
    db.refresh(db_syllabus_point)
    return db_syllabus_point

# LearningPack CRUD
def create_learning_pack_with_syllabus(db: Session, student_id: int, syllabus_point_ids: list[int]):
    """
    Create a new learning pack and associate it with syllabus points.

    Args:
        db: The database session.
        student_id: The ID of the student.
        syllabus_point_ids: A list of IDs of the syllabus points to associate.

    Returns:
        The newly created learning pack object.
    """
    db_learning_pack = models.LearningPack(student_id=student_id)
    syllabus_points = db.query(models.SyllabusPoint).filter(models.SyllabusPoint.id.in_(syllabus_point_ids)).all()
    db_learning_pack.syllabus_points.extend(syllabus_points)
    db.add(db_learning_pack)
    db.commit()
    db.refresh(db_learning_pack)
    return db_learning_pack

# MockExam CRUD
def create_mock_exam(db: Session, student_id: int, subject: str, question_ids: list[int]):
    """
    Create a new mock exam and associate it with questions.

    Args:
        db: The database session.
        student_id: The ID of the student.
        subject: The subject of the mock exam.
        question_ids: A list of IDs of the questions to include.

    Returns:
        The newly created mock exam object.
    """
    db_mock_exam = models.MockExam(student_id=student_id, subject=subject)
    questions = db.query(models.Question).filter(models.Question.id.in_(question_ids)).all()
    db_mock_exam.questions.extend(questions)
    db.add(db_mock_exam)
    db.commit()
    db.refresh(db_mock_exam)
    return db_mock_exam
