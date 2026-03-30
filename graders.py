"""
Task graders for Medical OCR Environment
Each grader returns a score between 0.0 and 1.0
"""
from typing import Dict, Any
from difflib import SequenceMatcher


class TaskGrader:
    """Base class for task graders"""
    
    def grade(self, observation: Dict[str, Any], ground_truth: Dict[str, Any]) -> float:
        """Return score between 0.0 and 1.0"""
        raise NotImplementedError


class EasyPrintedPrescriptionGrader(TaskGrader):
    """Grader for easy printed prescription task"""
    
    def grade(self, observation: Dict[str, Any], ground_truth: Dict[str, Any]) -> float:
        """
        Easy task: Just need to extract text with >80% accuracy
        """
        predicted_text = observation.get("ocr_text", "")
        true_text = ground_truth.get("text", "")
        
        if not true_text:
            return 0.0
        
        # Calculate similarity ratio
        similarity = SequenceMatcher(None, predicted_text.lower(), true_text.lower()).ratio()
        
        # Pass threshold: 80%
        if similarity >= 0.8:
            return 1.0
        elif similarity >= 0.6:
            return 0.5  # Partial credit
        else:
            return 0.0


class MediumHandwrittenPrescriptionGrader(TaskGrader):
    """Grader for medium handwritten prescription task"""
    
    def grade(self, observation: Dict[str, Any], ground_truth: Dict[str, Any]) -> float:
        """
        Medium task: Extract text with >70% accuracy AND identify at least 2 key fields
        """
        predicted_text = observation.get("ocr_text", "")
        true_text = ground_truth.get("text", "")
        predicted_fields = observation.get("extracted_fields", {})
        true_fields = ground_truth.get("fields", {})
        
        # Text accuracy component (50% weight)
        text_similarity = SequenceMatcher(None, predicted_text.lower(), true_text.lower()).ratio()
        text_score = min(text_similarity / 0.7, 1.0)  # Normalize to 70% threshold
        
        # Field extraction component (50% weight)
        if not true_fields:
            field_score = 0.0
        else:
            correct_fields = sum(
                1 for key in true_fields 
                if key in predicted_fields and self._field_matches(predicted_fields[key], true_fields[key])
            )
            field_score = min(correct_fields / 2, 1.0)  # Need at least 2 fields
        
        # Combined score
        total_score = 0.5 * text_score + 0.5 * field_score
        
        # Return 1.0 if both thresholds met, otherwise proportional
        if text_similarity >= 0.7 and correct_fields >= 2:
            return 1.0
        else:
            return total_score
    
    def _field_matches(self, predicted: Any, true: Any) -> bool:
        """Check if predicted field matches ground truth"""
        if isinstance(predicted, str) and isinstance(true, str):
            return SequenceMatcher(None, predicted.lower(), true.lower()).ratio() > 0.8
        elif isinstance(predicted, list) and isinstance(true, list):
            return len(set(predicted) & set(true)) >= len(true) * 0.8
        else:
            return predicted == true


class HardComplexPrescriptionGrader(TaskGrader):
    """Grader for hard complex prescription task"""
    
    def grade(self, observation: Dict[str, Any], ground_truth: Dict[str, Any]) -> float:
        """
        Hard task: Extract text with >85% accuracy AND extract ALL key fields correctly
        """
        predicted_text = observation.get("ocr_text", "")
        true_text = ground_truth.get("text", "")
        predicted_fields = observation.get("extracted_fields", {})
        true_fields = ground_truth.get("fields", {})
        
        # Text accuracy must be high (40% weight)
        text_similarity = SequenceMatcher(None, predicted_text.lower(), true_text.lower()).ratio()
        if text_similarity < 0.85:
            text_score = text_similarity / 0.85  # Partial credit
        else:
            text_score = 1.0
        
        # All fields must be extracted (60% weight)
        if not true_fields:
            field_score = 0.0
        else:
            required_fields = ["patient_name", "medications", "dosage", "doctor_name"]
            correct_fields = sum(
                1 for key in required_fields 
                if key in predicted_fields and key in true_fields and 
                self._field_matches(predicted_fields[key], true_fields[key])
            )
            field_score = correct_fields / len(required_fields)
        
        # Strict grading: need both high text accuracy AND all fields
        total_score = 0.4 * text_score + 0.6 * field_score
        
        # Only return 1.0 if truly excellent
        if text_similarity >= 0.85 and field_score >= 0.9:
            return 1.0
        else:
            return total_score
    
    def _field_matches(self, predicted: Any, true: Any) -> bool:
        """Check if predicted field matches ground truth"""
        if isinstance(predicted, str) and isinstance(true, str):
            return SequenceMatcher(None, predicted.lower(), true.lower()).ratio() > 0.9
        elif isinstance(predicted, list) and isinstance(true, list):
            # For lists (like medications), need exact match
            return set(predicted) == set(true)
        else:
            return predicted == true


# Grader registry
GRADERS = {
    "easy_printed_prescription": EasyPrintedPrescriptionGrader(),
    "medium_handwritten_prescription": MediumHandwrittenPrescriptionGrader(),
    "hard_complex_prescription": HardComplexPrescriptionGrader(),
}


def grade_task(task_id: str, observation: Dict[str, Any], ground_truth: Dict[str, Any]) -> float:
    """Grade a task and return score 0.0-1.0"""
    grader = GRADERS.get(task_id)
    if not grader:
        raise ValueError(f"Unknown task_id: {task_id}")
    return grader.grade(observation, ground_truth)
