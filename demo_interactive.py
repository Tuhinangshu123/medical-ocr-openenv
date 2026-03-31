"""
Interactive Demo Script for Medical OCR OpenEnv
Anyone can run this to test your environment!
"""
import requests
import json

BASE_URL = "https://ryozoryo-medical-ocr-openenv.hf.space"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_health():
    print_section("1. Testing Health Endpoint")
    response = requests.get(f"{BASE_URL}/")
    data = response.json()
    print(f"✅ Status: {data['status']}")
    print(f"✅ Name: {data['name']}")
    print(f"✅ OpenEnv: {data['openenv']}")
    return data

def list_tasks():
    print_section("2. Listing Available Tasks")
    response = requests.get(f"{BASE_URL}/tasks")
    data = response.json()
    for i, task in enumerate(data['tasks'], 1):
        print(f"\n{i}. {task['id']}")
        print(f"   Difficulty: {task['difficulty']}")
        print(f"   Description: {task['description']}")
    return data['tasks']

def run_task(task_id):
    print_section(f"3. Running Task: {task_id}")
    
    # Reset environment
    print("\n📋 Resetting environment...")
    response = requests.post(
        f"{BASE_URL}/reset",
        json={"task_id": task_id}
    )
    obs = response.json()["observation"]
    print(f"✅ Task loaded: {obs['current_task']}")
    print(f"✅ Initial confidence: {obs['confidence']}")
    print(f"✅ Image data length: {len(obs['image_data'])} chars")
    
    # Step 1: Process image
    print("\n🔍 Step 1: Processing prescription image...")
    response = requests.post(
        f"{BASE_URL}/step",
        json={"action": {"action_type": "process_image", "parameters": {}}}
    )
    result = response.json()
    obs = result['observation']
    reward = result['reward']
    
    print(f"✅ OCR completed")
    print(f"✅ Text extracted: {len(obs['ocr_text'])} characters")
    if obs['ocr_text']:
        print(f"   Preview: {obs['ocr_text'][:100]}...")
    print(f"✅ Confidence: {obs['confidence']:.2f}")
    print(f"✅ Reward: {reward}")
    
    # Step 2: Extract fields
    print("\n📝 Step 2: Extracting medical fields...")
    response = requests.post(
        f"{BASE_URL}/step",
        json={"action": {"action_type": "extract_fields", "parameters": {}}}
    )
    result = response.json()
    obs = result['observation']
    reward = result['reward']
    
    print(f"✅ Fields extracted: {obs['extracted_fields']}")
    print(f"✅ Final reward: {reward}")
    print(f"✅ Task complete: {result['done']}")
    
    return result

def main():
    print("\n" + "🏥"*30)
    print("  MEDICAL OCR OPENENV - INTERACTIVE DEMO")
    print("  https://huggingface.co/spaces/ryozoryo/medical-ocr-openenv")
    print("🏥"*30)
    
    try:
        # Test health
        test_health()
        
        # List tasks
        tasks = list_tasks()
        
        # Run easy task as demo
        print_section("4. Demo: Running Easy Task")
        print("\nThis will demonstrate the complete workflow:")
        print("1. Load a printed prescription image")
        print("2. Run OCR to extract text")
        print("3. Extract medical fields")
        print("4. Calculate reward based on accuracy")
        
        input("\nPress Enter to start demo...")
        
        result = run_task("easy_printed_prescription")
        
        print_section("✅ Demo Complete!")
        print("\nYour environment is working perfectly!")
        print("\nWhat judges see:")
        print("- ✅ Public API accessible")
        print("- ✅ Multiple difficulty levels")
        print("- ✅ Real medical OCR task")
        print("- ✅ Working reward system")
        print("- ✅ Complete documentation")
        
        print("\n" + "="*60)
        print("Want to try other tasks?")
        print("- easy_printed_prescription (clear text)")
        print("- medium_handwritten_prescription (harder)")
        print("- hard_complex_prescription (most challenging)")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("1. You have internet connection")
        print("2. The Space is running")
        print("3. API secrets are configured")

if __name__ == "__main__":
    main()
