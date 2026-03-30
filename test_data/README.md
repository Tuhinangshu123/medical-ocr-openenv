# Test Data for Medical OCR Environment

This directory contains test prescription images and ground truth labels for evaluating the OpenEnv environment.

## Structure

```
test_data/
├── easy/           # Clear, printed prescriptions
│   ├── prescription_001.jpg
│   ├── prescription_001.json
│   └── ... (5 total)
├── medium/         # Handwritten-style prescriptions
│   ├── prescription_001.jpg
│   ├── prescription_001.json
│   └── ... (5 total)
└── hard/           # Complex, multi-drug prescriptions
    ├── prescription_001.jpg
    ├── prescription_001.json
    └── ... (5 total)
```

## Ground Truth Format

Each JSON file contains:

```json
{
  "text": "Full prescription text...",
  "fields": {
    "patient_name": "John Doe",
    "medications": ["Medicine A", "Medicine B"],
    "dosage": ["10mg", "20mg"],
    "doctor_name": "Dr. Smith"
  }
}
```

## Difficulty Levels

### Easy (5 images)
- Clear, printed text
- Standard prescription format
- High contrast
- Expected OCR accuracy: >90%

### Medium (5 images)
- Handwritten-style text
- Abbreviated medical terms
- Some noise
- Expected OCR accuracy: 70-85%

### Hard (5 images)
- Complex multi-drug prescriptions
- Dense text with medical abbreviations
- Multiple fields to extract
- Expected OCR accuracy: 60-75%

## Using Real Prescription Images

To replace synthetic images with real prescriptions:

1. Collect prescription images (ensure patient privacy - anonymize!)
2. Save as JPG in appropriate difficulty folder
3. Create corresponding JSON with ground truth
4. Name files consistently: `prescription_NNN.jpg` and `prescription_NNN.json`

## Privacy & Ethics

- All synthetic images are generated, not real prescriptions
- If using real prescriptions:
  - Remove all personally identifiable information
  - Blur patient names, addresses, phone numbers
  - Get appropriate permissions
  - Follow HIPAA/local privacy regulations

## Image Requirements

- Format: JPG or PNG
- Resolution: 800x1000 to 1200x1600 pixels
- File size: < 2MB per image
- Color: RGB or grayscale

## Regenerating Synthetic Images

If you need to regenerate the synthetic images:

```bash
python generate_test_images.py
```

This will create new images from the JSON ground truth files.

## Testing

To test the environment with this data:

```bash
python test_environment.py
```

## Adding More Test Cases

To add more test cases:

1. Create new JSON file with ground truth
2. Generate image: `python generate_test_images.py`
3. Or add real prescription image with same base name
4. Test: `python test_environment.py`

## Statistics

- Total images: 15
- Easy: 5 (33%)
- Medium: 5 (33%)
- Hard: 5 (33%)
- Average text length: 150-400 characters
- Fields per prescription: 3-6
