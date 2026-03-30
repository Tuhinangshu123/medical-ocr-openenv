#!/usr/bin/env python3
"""
Baseline inference script for Medical OCR Environment
Uses OpenAI API client to run agent against the environment
"""
import os
import sys
from typing import List, Dict, Any
from openai import OpenAI
from environment import MedicalOCREnv, Action
from graders import grade_task


# Read from environment variables as per requirements
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("ERROR: OPENAI_API_KEY environment variable not set")
    sys.exit(1)


def run_agent_on_task(task_id: str, max_steps: int = 10) -> float:
    """Run agent on a single task and return final score"""
    
    # Initialize environment
    env = MedicalOCREnv(task_id=task_id)
    observation = env.reset()
    
    # Initialize OpenAI client
    client = OpenAI(
        api_key=OPENAI_API_KEY,
        base_url=API_BASE_URL
    )
    
    print(f"\n{'='*60}")
    print(f"Running task: {task_id}")
    print(f"{'='*60}")
    
    done = False
    step = 0
    
    while not done and step < max_steps:
        step += 1
        
        # Build prompt for the agent
        prompt = f"""You are an AI agent controlling a medical prescription OCR system.

Current State:
- Task: {observation.current_task}
- OCR Text: {observation.ocr_text[:200] if observation.ocr_text else '(not yet extracted)'}
- Extracted Fields: {observation.extracted_fields}
- Confidence: {observation.confidence}
- Step: {step}/{max_steps}

Available Actions:
1. process_image - Run OCR on the prescription image
2. extract_fields - Extract structured medical data from OCR text
3. validate_output - Validate the extracted data
4. retry_with_ensemble - Use ensemble OCR for better accuracy

Choose the next action to maximize OCR accuracy and field extraction completeness.
Respond with ONLY the action type (e.g., "process_image").
"""
        
        # Get action from model
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=50
            )
            
            action_text = response.choices[0].message.content.strip().lower()
            
            # Parse action
            if "process_image" in action_text:
                action = Action(action_type="process_image")
            elif "extract_fields" in action_text:
                action = Action(action_type="extract_fields")
            elif "validate_output" in action_text:
                action = Action(action_type="validate_output")
            elif "retry_with_ensemble" in action_text or "ensemble" in action_text:
                action = Action(action_type="retry_with_ensemble")
            else:
                # Default fallback
                action = Action(action_type="process_image")
            
            print(f"Step {step}: {action.action_type}")
            
            # Execute action
            observation, reward, done, info = env.step(action)
            print(f"  Reward: {reward.score:.3f} (accuracy: {reward.accuracy:.3f}, completeness: {reward.completeness:.3f})")
            
        except Exception as e:
            print(f"Error at step {step}: {e}")
            break
    
    # Final grading
    state = env.state()
    final_score = grade_task(
        task_id,
        state["observation"],
        state["ground_truth"]
    )
    
    print(f"\nFinal Score: {final_score:.3f}")
    return final_score


def main():
    """Run baseline agent on all tasks"""
    
    tasks = [
        "easy_printed_prescription",
        "medium_handwritten_prescription",
        "hard_complex_prescription"
    ]
    
    print("="*60)
    print("Medical OCR Environment - Baseline Inference")
    print("="*60)
    print(f"Model: {MODEL_NAME}")
    print(f"API Base: {API_BASE_URL}")
    
    scores = {}
    
    for task_id in tasks:
        try:
            score = run_agent_on_task(task_id)
            scores[task_id] = score
        except Exception as e:
            print(f"Failed on task {task_id}: {e}")
            scores[task_id] = 0.0
    
    # Summary
    print("\n" + "="*60)
    print("BASELINE RESULTS")
    print("="*60)
    for task_id, score in scores.items():
        print(f"{task_id:40s}: {score:.3f}")
    
    avg_score = sum(scores.values()) / len(scores)
    print(f"\n{'Average Score':40s}: {avg_score:.3f}")
    print("="*60)
    
    return scores


if __name__ == "__main__":
    main()
