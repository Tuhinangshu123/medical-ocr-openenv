#!/usr/bin/env python3
"""
Baseline inference script for Medical OCR Environment
Uses OpenAI API client to run agent against the environment
"""
import os
import sys
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from openai import OpenAI
except ImportError as e:
    logger.error(f"Failed to import openai: {e}")
    logger.info("Install with: pip install openai")
    sys.exit(1)

try:
    from environment import MedicalOCREnv, Action
    from graders import grade_task
except ImportError as e:
    logger.error(f"Failed to import environment modules: {e}")
    sys.exit(1)


# Read from environment variables as per requirements
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    logger.warning("OPENAI_API_KEY environment variable not set")
    logger.warning("Using mock mode for testing")
    MOCK_MODE = True
else:
    MOCK_MODE = False


def run_agent_on_task(task_id: str, max_steps: int = 10) -> float:
    """Run agent on a single task and return final score"""
    
    try:
        # Initialize environment
        env = MedicalOCREnv(task_id=task_id)
        observation = env.reset()
    except Exception as e:
        logger.error(f"Failed to initialize environment for {task_id}: {e}")
        return 0.0
    
    # Initialize OpenAI client if not in mock mode
    if not MOCK_MODE:
        try:
            client = OpenAI(
                api_key=OPENAI_API_KEY,
                base_url=API_BASE_URL
            )
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            return 0.0
    else:
        client = None
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Running task: {task_id}")
    logger.info(f"{'='*60}")
    
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
        
        # Get action from model or use simple heuristic in mock mode
        try:
            if MOCK_MODE:
                # Simple heuristic agent for testing
                if step == 1:
                    action = Action(action_type="process_image")
                elif step == 2:
                    action = Action(action_type="extract_fields")
                elif step == 3:
                    action = Action(action_type="validate_output")
                else:
                    action = Action(action_type="process_image")
            else:
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
            
            logger.info(f"Step {step}: {action.action_type}")
            
            # Execute action
            observation, reward, done, info = env.step(action)
            logger.info(f"  Reward: {reward.score:.3f} (accuracy: {reward.accuracy:.3f}, completeness: {reward.completeness:.3f})")
            
        except Exception as e:
            logger.error(f"Error at step {step}: {e}")
            break
    
    # Final grading
    try:
        state = env.state()
        final_score = grade_task(
            task_id,
            state["observation"],
            state["ground_truth"]
        )
    except Exception as e:
        logger.error(f"Failed to grade task {task_id}: {e}")
        final_score = 0.0
    
    logger.info(f"\nFinal Score: {final_score:.3f}")
    return final_score


def main():
    """Run baseline agent on all tasks"""
    
    tasks = [
        "easy_printed_prescription",
        "medium_handwritten_prescription",
        "hard_complex_prescription"
    ]
    
    try:
        logger.info("="*60)
        logger.info("Medical OCR Environment - Baseline Inference")
        logger.info("="*60)
        logger.info(f"Model: {MODEL_NAME}")
        logger.info(f"API Base: {API_BASE_URL}")
        logger.info(f"Mock Mode: {MOCK_MODE}")
        
        scores = {}
        
        for task_id in tasks:
            try:
                score = run_agent_on_task(task_id)
                scores[task_id] = score
            except Exception as e:
                logger.error(f"Failed on task {task_id}: {e}")
                scores[task_id] = 0.0
        
        # Summary
        logger.info("\n" + "="*60)
        logger.info("BASELINE RESULTS")
        logger.info("="*60)
        for task_id, score in scores.items():
            logger.info(f"{task_id:40s}: {score:.3f}")
        
        avg_score = sum(scores.values()) / len(scores) if scores else 0.0
        logger.info(f"\n{'Average Score':40s}: {avg_score:.3f}")
        logger.info("="*60)
        
        return scores
        
    except Exception as e:
        logger.error(f"Fatal error in main: {e}")
        import traceback
        traceback.print_exc()
        return {}


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Unhandled exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
