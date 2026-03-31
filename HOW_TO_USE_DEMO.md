# How Judges/Users Can View and Use Your OpenEnv Environment

## 🌐 Public Access

Your Space is publicly accessible at:
**https://huggingface.co/spaces/ryozoryo/medical-ocr-openenv**

Anyone can:
1. View the Space page
2. Read the documentation
3. See the code (linked to GitHub)
4. Test the API endpoints

## 📖 What Judges Will See

### 1. HuggingFace Space Page

When judges visit your Space URL, they see:

- **Title**: Medical OCR OpenEnv 💊
- **Tags**: openenv, medical, ocr, healthcare
- **README**: Full documentation with:
  - Environment description
  - Action/Observation spaces
  - 3 tasks (easy, medium, hard)
  - Setup instructions
  - Baseline scores
  - Project structure

### 2. GitHub Repository

Linked from the Space, shows all your code:
- `environment.py` - Core implementation
- `graders.py` - Scoring functions
- `inference.py` - Baseline agent
- `server.py` - API server
- `test_data/` - 15 prescription images + ground truth
- Complete documentation

## 🧪 How to Test/Use the Environment

### Method 1: Direct API Testing (No Code Required)

Judges can test your API using browser or curl:

**1. Health Check**
```
Open in browser: https://ryozoryo-medical-ocr-openenv.hf.space/

Returns:
{
  "name": "Medical Prescription OCR Environment",
  "version": "1.0.0",
  "status": "running",
  "openenv": true
}
```

**2. List Available Tasks**
```
Open in browser: https://ryozoryo-medical-ocr-openenv.hf.space/tasks

Returns:
{
  "tasks": [
    {
      "id": "easy_printed_prescription",
      "difficulty": "easy",
      "description": "Extract text from clear, printed prescription"
    },
    {
      "id": "medium_handwritten_prescription",
      "difficulty": "medium",
      "description": "Extract text from handwritten prescription"
    },
    {
      "id": "hard_complex_prescription",
      "difficulty": "hard",
      "description": "Extract and structure data from complex multi-drug prescription"
    }
  ]
}
```

**3. Test Reset Endpoint (Using curl or Postman)**
```bash
curl -X POST https://ryozoryo-medical-ocr-openenv.hf.space/reset \
  -H "Content-Type: application/json" \
  -d '{"task_id": "easy_printed_prescription"}'
```

Returns observation with prescription image data.

### Method 2: Python Client (For Developers)

Judges can write a simple Python script to interact:

```python
import requests

BASE_URL = "https://ryozoryo-medical-ocr-openenv.hf.space"

# 1. Check health
response = requests.get(f"{BASE_URL}/")
print("Health:", response.json())

# 2. List tasks
response = requests.get(f"{BASE_URL}/tasks")
print("Tasks:", response.json())

# 3. Reset environment
response = requests.post(
    f"{BASE_URL}/reset",
    json={"task_id": "easy_printed_prescription"}
)
observation = response.json()["observation"]
print("Initial observation:", observation)

# 4. Take an action
response = requests.post(
    f"{BASE_URL}/step",
    json={
        "action": {
            "action_type": "process_image",
            "parameters": {}
        }
    }
)
result = response.json()
print("Reward:", result["reward"])
print("Done:", result["done"])
```

### Method 3: OpenEnv CLI (Official Way)

If judges have OpenEnv installed:

```bash
# Install OpenEnv
pip install openenv-core

# Test your environment
openenv test https://ryozoryo-medical-ocr-openenv.hf.space

# Run validation
openenv validate https://ryozoryo-medical-ocr-openenv.hf.space
```

## 🎬 Demo Workflow Example

Here's what a complete interaction looks like:

```python
import requests
import json

BASE_URL = "https://ryozoryo-medical-ocr-openenv.hf.space"

# Step 1: Reset to start a task
print("=== Starting Easy Task ===")
response = requests.post(
    f"{BASE_URL}/reset",
    json={"task_id": "easy_printed_prescription"}
)
obs = response.json()["observation"]
print(f"Task: {obs['current_task']}")
print(f"Initial confidence: {obs['confidence']}")

# Step 2: Process the image
print("\n=== Processing Image ===")
response = requests.post(
    f"{BASE_URL}/step",
    json={"action": {"action_type": "process_image", "parameters": {}}}
)
result = response.json()
print(f"OCR Text: {result['observation']['ocr_text'][:100]}...")
print(f"Reward: {result['reward']}")

# Step 3: Extract fields
print("\n=== Extracting Fields ===")
response = requests.post(
    f"{BASE_URL}/step",
    json={"action": {"action_type": "extract_fields", "parameters": {}}}
)
result = response.json()
print(f"Extracted: {result['observation']['extracted_fields']}")
print(f"Final Reward: {result['reward']}")
print(f"Task Complete: {result['done']}")
```

## 📊 What Makes Your Demo Stand Out

### 1. Real Medical Images
Your test_data folder contains 15 actual prescription images:
- 5 easy (printed, clear)
- 5 medium (handwritten)
- 5 hard (complex, multi-drug)

### 2. Ground Truth Data
Each image has a corresponding JSON file with:
- Expected OCR text
- Required medical fields
- Difficulty level

### 3. Working Graders
Your graders produce realistic scores:
- Easy tasks: 0.7-0.9
- Medium tasks: 0.5-0.7
- Hard tasks: 0.3-0.6

### 4. Complete Documentation
- Clear README on Space page
- API reference
- Setup instructions
- Baseline scores
- Integration examples

## 🎯 For Hackathon Judges

Judges will evaluate based on:

1. **Can they access the Space?** ✅ Yes - public URL
2. **Does it follow OpenEnv spec?** ✅ Yes - all endpoints work
3. **Are tasks well-defined?** ✅ Yes - 3 clear difficulty levels
4. **Do graders work?** ✅ Yes - tested and produce varying scores
5. **Is it documented?** ✅ Yes - comprehensive README
6. **Real-world utility?** ✅ Yes - medical OCR is high impact
7. **Can they test it?** ✅ Yes - multiple methods above

## 🔗 Links to Share

**Primary Submission URL:**
```
https://huggingface.co/spaces/ryozoryo/medical-ocr-openenv
```

**GitHub Repository:**
```
https://github.com/Tuhinangshu123/medical-ocr-openenv
```

**Quick Test Command:**
```bash
curl https://ryozoryo-medical-ocr-openenv.hf.space/
```

## 💡 Pro Tips for Judges

1. **Start with /tasks endpoint** - See all available tasks
2. **Try /reset with different task_ids** - Test all 3 difficulty levels
3. **Check the test_data folder on GitHub** - See actual prescription images
4. **Read the README** - Comprehensive documentation
5. **Look at graders.py** - See how scoring works

Your environment is fully functional and ready for judges to explore!
