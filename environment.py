"""
OpenEnv-compliant Medical Prescription OCR Environment
"""
import base64
import json
import random
from typing import Dict, Any, Tuple, Optional
from pydantic import BaseModel, Field
from pathlib import Path


class Observation(BaseModel):
    """Current state of the OCR environment"""
    image_data: str = Field(description="Base64 encoded prescription image")
    ocr_text: str = Field(default="", description="Extracted text from OCR")
    extracted_fields: Dict[str, Any] = Field(default_factory=dict, description="Structured medical data")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="OCR confidence score")
    current_task: str = Field(default="", description="Current task ID")
    step_count: int = Field(default=0, description="Number of steps taken")


class Action(BaseModel):
    """Actions the agent can take"""
    action_type: str = Field(description="Type of action: process_image, extract_fields, validate_output, retry_with_ensemble")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Action parameters")


class Reward(BaseModel):
    """Reward signal for agent performance"""
    score: float = Field(ge=0.0, le=1.0, description="Reward score between 0 and 1")
    accuracy: float = Field(default=0.0, description="OCR accuracy")
    completeness: float = Field(default=0.0, description="Field extraction completeness")
    confidence: float = Field(default=0.0, description="Model confidence")


class MedicalOCREnv:
    """OpenEnv environment for medical prescription OCR"""
    
    def __init__(self, task_id: str = "easy_printed_prescription"):
        self.task_id = task_id
        self.current_observation: Optional[Observation] = None
        self.ground_truth: Dict[str, Any] = {}
        self.max_steps = 10
        self.step_count = 0
        
    def reset(self) -> Observation:
        """Reset environment to initial state"""
        self.step_count = 0
        
        # Load task-specific test image
        image_data = self._load_task_image(self.task_id)
        self.ground_truth = self._load_ground_truth(self.task_id)
        
        self.current_observation = Observation(
            image_data=image_data,
            current_task=self.task_id,
            step_count=0
        )
        
        return self.current_observation
    
    def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
        """Execute action and return new state"""
        self.step_count += 1
        
        if action.action_type == "process_image":
            # Simulate OCR processing
            ocr_result = self._run_ocr(self.current_observation.image_data)
            self.current_observation.ocr_text = ocr_result["text"]
            self.current_observation.confidence = ocr_result["confidence"]
            
        elif action.action_type == "extract_fields":
            # Extract structured fields from OCR text
            fields = self._extract_medical_fields(self.current_observation.ocr_text)
            self.current_observation.extracted_fields = fields
            
        elif action.action_type == "validate_output":
            # Validate extracted data
            pass
            
        elif action.action_type == "retry_with_ensemble":
            # Use ensemble OCR for better accuracy
            ocr_result = self._run_ensemble_ocr(self.current_observation.image_data)
            self.current_observation.ocr_text = ocr_result["text"]
            self.current_observation.confidence = ocr_result["confidence"]
        
        # Calculate reward
        reward = self._calculate_reward()
        
        # Check if episode is done
        done = self.step_count >= self.max_steps or self._is_task_complete()
        
        info = {
            "task_id": self.task_id,
            "ground_truth": self.ground_truth,
            "step_count": self.step_count
        }
        
        return self.current_observation, reward, done, info
    
    def state(self) -> Dict[str, Any]:
        """Return current environment state"""
        return {
            "observation": self.current_observation.model_dump() if self.current_observation else {},
            "task_id": self.task_id,
            "step_count": self.step_count,
            "ground_truth": self.ground_truth
        }
    
    def _load_task_image(self, task_id: str) -> str:
        """Load test image for specific task"""
        import random
        
        # Map task to difficulty
        if "easy" in task_id:
            difficulty = "easy"
        elif "medium" in task_id:
            difficulty = "medium"
        else:
            difficulty = "hard"
        
        # Load random image from test data
        test_dir = Path(__file__).parent / "test_data" / difficulty
        images = list(test_dir.glob("*.jpg")) + list(test_dir.glob("*.png"))
        
        if not images:
            raise FileNotFoundError(f"No test images found in {test_dir}")
        
        # Pick random image
        image_path = random.choice(images)
        self._current_image_path = image_path
        
        # Load and encode image
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        
        return base64.b64encode(image_bytes).decode("utf-8")
    
    def _load_ground_truth(self, task_id: str) -> Dict[str, Any]:
        """Load ground truth labels for task"""
        # Load corresponding JSON for the selected image
        if hasattr(self, '_current_image_path'):
            json_path = self._current_image_path.with_suffix('.json')
            if json_path.exists():
                with open(json_path, 'r') as f:
                    return json.load(f)
        
        # Fallback
        return {
            "text": "",
            "fields": {}
        }
    
    def _run_ocr(self, image_data: str) -> Dict[str, Any]:
        """Run OCR on image - integrate your existing OCR service"""
        try:
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            
            # Use Tesseract OCR (basic approach)
            import pytesseract
            from PIL import Image
            import io
            
            image = Image.open(io.BytesIO(image_bytes))
            text = pytesseract.image_to_string(image)
            
            # Calculate confidence (simple heuristic)
            confidence = min(0.9, len(text) / 500.0) if text else 0.0
            
            return {"text": text.strip(), "confidence": confidence}
        except Exception as e:
            print(f"OCR error: {e}")
            return {"text": "", "confidence": 0.0}
    
    def _run_ensemble_ocr(self, image_data: str) -> Dict[str, Any]:
        """Run ensemble OCR - integrate your ensemble approach"""
        try:
            # For now, use same as basic OCR but with higher confidence
            # TODO: Integrate your actual ensemble OCR service
            result = self._run_ocr(image_data)
            result["confidence"] = min(1.0, result["confidence"] + 0.1)
            return result
        except Exception as e:
            print(f"Ensemble OCR error: {e}")
            return {"text": "", "confidence": 0.0}
    
    def _extract_medical_fields(self, text: str) -> Dict[str, Any]:
        """Extract structured medical fields from text"""
        import re
        
        fields = {}
        
        # Extract patient name
        patient_patterns = [
            r"Patient[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
            r"Name[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
            r"Pt[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
        ]
        for pattern in patient_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                fields["patient_name"] = match.group(1).strip()
                break
        
        # Extract doctor name
        doctor_patterns = [
            r"Dr\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
        ]
        for pattern in doctor_patterns:
            matches = re.findall(pattern, text)
            if matches:
                fields["doctor_name"] = "Dr. " + matches[0].strip()
                break
        
        # Extract medications (simple approach)
        medications = []
        dosages = []
        
        # Look for common medication patterns
        med_patterns = [
            r"([A-Z][a-z]+(?:cillin|mycin|prazole|statin|olol|pril|sartan|formin))\s+(\d+\s*mg)",
            r"(\d+)\.\s+([A-Z][a-z]+)\s+(\d+\s*(?:mg|ml|IU))",
        ]
        
        for pattern in med_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match) >= 2:
                    medications.append(match[0] if match[0][0].isupper() else match[1])
                    dosages.append(match[1] if len(match) == 2 else match[2])
        
        if medications:
            fields["medications"] = medications
        if dosages:
            fields["dosage"] = dosages
        
        return fields
    
    def _calculate_reward(self) -> Reward:
        """Calculate reward based on OCR accuracy and field extraction"""
        if not self.current_observation:
            return Reward(score=0.0)
        
        # Calculate text accuracy
        text_accuracy = self._calculate_text_accuracy(
            self.current_observation.ocr_text,
            self.ground_truth.get("text", "")
        )
        
        # Calculate field extraction completeness
        completeness = self._calculate_field_completeness(
            self.current_observation.extracted_fields,
            self.ground_truth.get("fields", {})
        )
        
        # Combined score
        score = 0.6 * text_accuracy + 0.4 * completeness
        
        return Reward(
            score=score,
            accuracy=text_accuracy,
            completeness=completeness,
            confidence=self.current_observation.confidence
        )
    
    def _calculate_text_accuracy(self, predicted: str, ground_truth: str) -> float:
        """Calculate character-level accuracy"""
        if not ground_truth:
            return 0.0
        # Simple character accuracy - you can use your existing metrics
        correct = sum(1 for a, b in zip(predicted, ground_truth) if a == b)
        return correct / max(len(ground_truth), 1)
    
    def _calculate_field_completeness(self, predicted: Dict, ground_truth: Dict) -> float:
        """Calculate field extraction completeness"""
        if not ground_truth:
            return 0.0
        total_fields = len(ground_truth)
        correct_fields = sum(1 for k in ground_truth if k in predicted and predicted[k])
        return correct_fields / max(total_fields, 1)
    
    def _is_task_complete(self) -> bool:
        """Check if task is successfully completed"""
        if not self.current_observation:
            return False
        return (
            len(self.current_observation.ocr_text) > 0 and
            len(self.current_observation.extracted_fields) > 0 and
            self.current_observation.confidence > 0.7
        )
