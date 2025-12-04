from typing import List, Optional
from sqlalchemy.orm import Session
from src.core_database import crud, models
import sys

def generate_learning_pack(
    student_id: int,
    syllabus_topic_codes: List[str],
    db: Session
) -> Optional[models.LearningPack]:
    """
    Generates a learning pack for a given student and syllabus topics.

    Args:
        student_id: The ID of the student.
        syllabus_topic_codes: A list of syllabus topic codes to include in the pack.
        db: The database session.

    Returns:
        The newly created LearningPack object, or None if no relevant resources are found.
    """
    try:
        # 1. Find syllabus points from codes
        syllabus_points = db.query(models.SyllabusPoint).filter(
            models.SyllabusPoint.code.in_(syllabus_topic_codes)
        ).all()
        
        if not syllabus_points:
            print(f"No syllabus points found for codes: {syllabus_topic_codes}", file=sys.stderr)
            return None

        # 2. Find relevant resources for these syllabus points (placeholder logic)
        # This is where a more advanced algorithm would go.
        # For now, let's just find any resource related to the subject of the first syllabus point.
        subject = syllabus_points[0].subject
        relevant_resources = db.query(models.Resource).filter(
            models.Resource.subject == subject
        ).limit(5).all() # Limit to 5 resources for now

        if not relevant_resources:
            print(f"No resources found for subject: {subject}", file=sys.stderr)
            return None
        
        # 3. Create the learning pack
        learning_pack = crud.create_learning_pack_with_syllabus(
            db=db,
            student_id=student_id,
            syllabus_point_ids=[sp.id for sp in syllabus_points]
        )
        
        # 4. Associate the found resources with the learning pack
        learning_pack.resources.extend(relevant_resources)
        db.commit()
        db.refresh(learning_pack)

        return learning_pack
    except Exception as e:
        print(f"Error generating learning pack: {e}", file=sys.stderr)
        return None