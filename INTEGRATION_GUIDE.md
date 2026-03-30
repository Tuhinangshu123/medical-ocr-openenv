# Integrating Matrika OCR with OpenEnv

This guide shows how to connect your existing Matrika OCR services to the OpenEnv adapter.

## Step 1: Connect Your OCR Service

In `environment.py`, replace the placeholder methods with actual calls to your OCR service:

```python
def _run_ocr(self, image_data: str) -> Dict[str, Any]:
    """Run OCR on image - integrate your existing OCR service"""
    import requests
    import base64
    
    # Decode base64 image
    image_bytes = base64.b64decode(image_data)
    
    # Call your OCR service (adjust URL to your deployment)
    response = requests.post(
        "http://localhost:8000/api/ocr/process",
        files={"file": image_bytes}
    )
    
    result = response.json()
    return {
        "text": result.get("text", ""),
        "confidence": result.get("confidence", 0.0)
    }

def _run_ensemble_ocr(self, image_data: str) -> Dict[str, Any]:
    """Run ensemble OCR - integrate your ensemble approach"""
    import requests
    import base64
    
    image_bytes = base64.b64decode(image_data)
    
    # Call your ensemble OCR endpoint
    response = requests.post(
        "http://localhost:8000/api/ocr/ensemble",
        files={"file": image_bytes}
    )
    
    result = response.json()
    return {
        "text": result.get("text", ""),
        "confidence": result.get("confidence", 0.0)
    }
```

## Step 2: Add Test Data

Create a `test_data/` directory with sample prescriptions:

```bash
mkdir -p test_data/easy test_data/medium test_data/hard
```

Add your prescription images and ground truth labels:

```
test_data/
├── easy/
│   ├── prescription_001.jpg
│   └── prescription_001.json  # Ground truth
├── medium/
│   ├── prescription_002.jpg
│   └── prescription_002.json
└── hard/
    ├── prescription_003.jpg
    └── prescription_003.json
```

Ground truth JSON format:
```json
{
  "text": "Full prescription text here...",
  "fields": {
    "patient_name": "John Doe",
    "medications": ["Amoxicillin", "Ibuprofen"],
    "dosage": ["500mg", "200mg"],
    "doctor_name": "Dr. Smith"
  }
}
```

## Step 3: Update Data Loading

Modify `_load_task_image()` and `_load_ground_truth()`:

```python
def _load_task_image(self, task_id: str) -> str:
    """Load test image for specific task"""
    import base64
    from pathlib import Path
    
    # Map task to difficulty
    difficulty = task_id.split("_")[0]  # easy, medium, hard
    
    # Load first image from test data
    test_dir = Path(__file__).parent / "test_data" / difficulty
    images = list(test_dir.glob("*.jpg")) + list(test_dir.glob("*.png"))
    
    if not images:
        raise FileNotFoundError(f"No test images found in {test_dir}")
    
    # Load and encode image
    with open(images[0], "rb") as f:
        image_bytes = f.read()
    
    return base64.b64encode(image_bytes).decode("utf-8")

def _load_ground_truth(self, task_id: str) -> Dict[str, Any]:
    """Load ground truth labels for task"""
    import json
    from pathlib import Path
    
    difficulty = task_id.split("_")[0]
    test_dir = Path(__file__).parent / "test_data" / difficulty
    
    # Load corresponding JSON
    json_files = list(test_dir.glob("*.json"))
    if not json_files:
        raise FileNotFoundError(f"No ground truth found in {test_dir}")
    
    with open(json_files[0], "r") as f:
        return json.load(f)
```

## Step 4: Test Locally

1. Start your Matrika OCR service:
```bash
cd packages/ocr-service
python app_ensemble_ocr.py
```

2. Test the OpenEnv adapter:
```bash
cd openenv-adapter
python inference.py
```

## Step 5: Deploy to Hugging Face

1. Create a new Space: https://huggingface.co/new-space
2. Choose "Docker" as the SDK
3. Add the `openenv` tag
4. Push your code:

```bash
git init
git add .
git commit -m "Initial OpenEnv adapter"
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/medical-ocr-env
git push space main
```

5. Set environment secrets in Space settings

## Step 6: Validate Submission

Run the pre-submission validator:

```bash
curl -fsSL https://raw.githubusercontent.com/openenv/openenv/main/scripts/validate-submission.sh | bash -s -- https://YOUR_USERNAME-medical-ocr-env.hf.space
```

## Quick Wins

To maximize your score quickly:

1. **Use your best OCR model**: The ensemble approach you already have
2. **Add 5-10 test cases per difficulty**: More test data = better evaluation
3. **Tune the reward function**: Adjust weights based on what matters most
4. **Document thoroughly**: Good README increases your creativity score
5. **Show real impact**: Include examples of actual prescriptions (anonymized)

## Timeline

- **Now - March 25**: Integrate and test locally
- **March 25 - 28**: Deploy to HF Spaces and validate
- **March 28**: Submit when window opens
- **March 28 - April 8**: Iterate based on feedback

## Questions?

Join the Discord community mentioned in the hackathon page for support.
