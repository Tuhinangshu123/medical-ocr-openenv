#!/usr/bin/env python3
"""
Test the OpenEnv environment locally before deployment
"""
from environment import MedicalOCREnv, Action
from graders import grade_task


def test_single_task(task_id: str):
    """Test a single task"""
    print(f"\n{'='*60}")
    print(f"Testing: {task_id}")
    print(f"{'='*60}")
    
    # Initialize environment
    env = MedicalOCREnv(task_id=task_id)
    observation = env.reset()
    
    print(f"Initial state:")
    print(f"  Task: {observation.current_task}")
    print(f"  Image loaded: {len(observation.image_data)} bytes")
    
    # Step 1: Process image
    print(f"\nStep 1: Processing image...")
    action = Action(action_type="process_image")
    observation, reward, done, info = env.step(action)
    print(f"  OCR Text (first 200 chars): {observation.ocr_text[:200]}")
    print(f"  Confidence: {observation.confidence:.3f}")
    print(f"  Reward: {reward.score:.3f}")
    
    # Step 2: Extract fields
    print(f"\nStep 2: Extracting fields...")
    action = Action(action_type="extract_fields")
    observation, reward, done, info = env.step(action)
    print(f"  Extracted fields: {observation.extracted_fields}")
    print(f"  Reward: {reward.score:.3f}")
    
    # Final grading
    state = env.state()
    final_score = grade_task(task_id, state["observation"], state["ground_truth"])
    
    print(f"\n{'='*60}")
    print(f"Final Score: {final_score:.3f}")
    print(f"Ground Truth:")
    print(f"  Text (first 100 chars): {state['ground_truth']['text'][:100]}")
    print(f"  Fields: {state['ground_truth']['fields']}")
    print(f"{'='*60}")
    
    return final_score


def test_all_tasks():
    """Test all three tasks"""
    print("\n" + "="*60)
    print("TESTING MEDICAL OCR ENVIRONMENT")
    print("="*60)
    
    tasks = [
        "easy_printed_prescription",
        "medium_handwritten_prescription",
        "hard_complex_prescription"
    ]
    
    scores = {}
    
    for task_id in tasks:
        try:
            score = test_single_task(task_id)
            scores[task_id] = score
        except Exception as e:
            print(f"\n❌ Error testing {task_id}: {e}")
            import traceback
            traceback.print_exc()
            scores[task_id] = 0.0
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for task_id, score in scores.items():
        status = "✅" if score > 0.0 else "❌"
        print(f"{status} {task_id:40s}: {score:.3f}")
    
    avg_score = sum(scores.values()) / len(scores)
    print(f"\n{'Average Score':40s}: {avg_score:.3f}")
    
    if all(score > 0.0 for score in scores.values()):
        print("\n✅ All tasks working! Environment is ready.")
        return 0
    else:
        print("\n❌ Some tasks failed. Check errors above.")
        return 1


if __name__ == "__main__":
    exit(test_all_tasks())
