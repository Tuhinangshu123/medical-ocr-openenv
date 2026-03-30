---
title: Medical OCR OpenEnv
emoji: 💊
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
tags:
  - openenv
  - medical
  - ocr
  - healthcare
---

# Medical Prescription OCR - OpenEnv Environment

An OpenEnv-compliant environment for training and evaluating AI agents on medical prescription OCR and data extraction tasks.

## Environment Description

This environment simulates the real-world task of extracting text and structured medical data from prescription images. Healthcare providers worldwide need to digitize paper prescriptions, and this environment provides a standardized way to train and evaluate AI agents on this critical task.

### Why This Matters

- **Real-world utility**: Medical prescription digitization is used daily in hospitals and pharmacies
- **Challenging**: Handwritten prescriptions, varying formats, medical terminology
- **Measurable**: Clear success criteria (text accuracy, field extraction)
- **Scalable**: Can be extended to other medical document types

## Action Space

The agent can take the following actions:

```python
Action(action_type="process_image", parameters={})
Action(action_type="extract_fields", parameters={})
Action(action_type="validate_output", parameters={})
Action(action_type="retry_with_ensemble", parameters={})
```

- `process_image`: Run OCR on the prescription image
- `extract_fields`: Extract structured medical fields (patient name, medications, dosage, etc.)
- `validate_output`: Validate the extracted data for completeness
- `retry_with_ensemble`: Use ensemble OCR approach for higher accuracy

## Observation Space

```python
{
    "image_data": str,           # Base64 encoded prescription image
    "ocr_text": str,             # Extracted text from OCR
    "extracted_fields": dict,    # Structured medical data
    "confidence": float,         # OCR confidence score (0.0-1.0)
    "current_task": str,         # Current task ID
    "step_count": int            # Number of steps taken
}
```

## Tasks

### 1. Easy: Printed Prescription (easy_printed_prescription)
- **Objective**: Extract text from a clear, printed prescription
- **Success criteria**: >80% text accuracy
- **Expected difficulty**: Most models should achieve >0.8 score

### 2. Medium: Handwritten Prescription (medium_handwritten_prescription)
- **Objective**: Extract text from handwritten prescription and identify key fields
- **Success criteria**: >70% text accuracy AND at least 2 key fields extracted
- **Expected difficulty**: Requires both OCR and field extraction

### 3. Hard: Complex Multi-Drug Prescription (hard_complex_prescription)
- **Objective**: Extract and structure complete data from complex prescription
- **Success criteria**: >85% text accuracy AND all required fields (patient_name, medications, dosage, doctor_name)
- **Expected difficulty**: Challenges frontier models, requires strategic action sequencing

## Reward Function

The reward function provides continuous feedback:

```python
reward = 0.6 * text_accuracy + 0.4 * field_completeness
```

- **Text accuracy**: Character-level similarity to ground truth
- **Field completeness**: Percentage of required fields correctly extracted
- **Partial progress**: Rewards incremental improvements
- **Penalties**: Lower confidence scores reduce reward

## Setup Instructions

### Local Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export OPENAI_API_KEY="your-api-key"
export MODEL_NAME="gpt-4"
export API_BASE_URL="https://api.openai.com/v1"
```

3. Run baseline inference:
```bash
python inference.py
```

### Docker Setup

1. Build the image:
```bash
docker build -t medical-ocr-env .
```

2. Run the container:
```bash
docker run -p 7860:7860 \
  -e OPENAI_API_KEY="your-key" \
  medical-ocr-env
```

3. Test the API:
```bash
curl http://localhost:7860/
curl -X POST http://localhost:7860/reset -H "Content-Type: application/json" -d '{"task_id": "easy_printed_prescription"}'
```

### Hugging Face Spaces Deployment

1. Create a new Space on Hugging Face
2. Tag it with `openenv`
3. Push this repository to the Space
4. Set secrets in Space settings:
   - `OPENAI_API_KEY`
   - `MODEL_NAME`
   - `API_BASE_URL`

## Baseline Scores

Baseline scores using GPT-4 (as of testing):

| Task | Score | Notes |
|------|-------|-------|
| Easy (Printed) | 0.85 | High accuracy on clear text |
| Medium (Handwritten) | 0.62 | Struggles with field extraction |
| Hard (Complex) | 0.48 | Requires better strategy |

**Average**: 0.65

## Validation

Run OpenEnv validation:

```bash
openenv validate
```

## Project Structure

```
openenv-adapter/
├── openenv.yaml          # Environment metadata
├── environment.py        # Core environment implementation
├── graders.py           # Task graders (scoring functions)
├── inference.py         # Baseline agent script
├── server.py            # FastAPI server for HF Spaces
├── Dockerfile           # Container definition
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Integration with Existing Matrika System

This OpenEnv adapter wraps the existing Matrika OCR services:
- Uses Tesseract OCR backend
- Leverages ensemble OCR approach
- Integrates trained ML models
- Reuses field extraction logic

## Future Enhancements

- Add more task variations (lab reports, discharge summaries)
- Multi-page document support
- Real-time feedback on extraction quality
- Support for multiple languages (Hindi, regional languages)

## License

MIT License - See main Matrika project for details

## Contact

Tuhinangshu Das - tuhinangshudas610@gmail.com
