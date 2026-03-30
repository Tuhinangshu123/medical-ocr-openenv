#!/usr/bin/env python3
"""
Test graders to ensure they produce varying scores
This is CRITICAL - graders that always return the same score = DISQUALIFICATION
"""
from graders import grade_task


def test_easy_grader():
    """Test easy task grader with varying quality inputs"""
    print("\n" + "="*60)
    print("Testing Easy Grader (Printed Prescription)")
    print("="*60)
    
    ground_truth = {
        "text": "Patient: John Doe. Medication: Amoxicillin 500mg. Take twice daily.",
        "fields": {}
    }
    
    # Test case 1: Perfect match
    obs_perfect = {
        "ocr_text": "Patient: John Doe. Medication: Amoxicillin 500mg. Take twice daily.",
        "extracted_fields": {}
    }
    score_perfect = grade_task("easy_printed_prescription", obs_perfect, ground_truth)
    print(f"Perfect match: {score_perfect:.3f} (expected: 1.0)")
    
    # Test case 2: Good match (>80% similar)
    obs_good = {
        "ocr_text": "Patient: John Doe. Medication: Amoxicillin 500mg. Take twice dally.",  # typo
        "extracted_fields": {}
    }
    score_good = grade_task("easy_printed_prescription", obs_good, ground_truth)
    print(f"Good match: {score_good:.3f} (expected: 0.5-1.0)")
    
    # Test case 3: Partial match (60-80%)
    obs_partial = {
        "ocr_text": "Patient: John Doe. Medication: Amoxicillin 500mg.",
        "extracted_fields": {}
    }
    score_partial = grade_task("easy_printed_prescription", obs_partial, ground_truth)
    print(f"Partial match: {score_partial:.3f} (expected: 0.5)")
    
    # Test case 4: Poor match (<60%)
    obs_poor = {
        "ocr_text": "Patient: John Doe.",
        "extracted_fields": {}
    }
    score_poor = grade_task("easy_printed_prescription", obs_poor, ground_truth)
    print(f"Poor match: {score_poor:.3f} (expected: 0.0)")
    
    # Test case 5: Complete failure
    obs_fail = {
        "ocr_text": "",
        "extracted_fields": {}
    }
    score_fail = grade_task("easy_printed_prescription", obs_fail, ground_truth)
    print(f"Complete failure: {score_fail:.3f} (expected: 0.0)")
    
    # Variance check
    scores = [score_perfect, score_good, score_partial, score_poor, score_fail]
    variance = max(scores) - min(scores)
    print(f"\nScore variance: {variance:.3f} (must be > 0.0 to avoid disqualification)")
    
    if variance == 0.0:
        print("❌ CRITICAL: Grader always returns same score - WILL BE DISQUALIFIED!")
        return False
    else:
        print("✅ Grader produces varying scores")
        return True


def test_medium_grader():
    """Test medium task grader with varying quality inputs"""
    print("\n" + "="*60)
    print("Testing Medium Grader (Handwritten Prescription)")
    print("="*60)
    
    ground_truth = {
        "text": "Patient: Jane Smith. Medications: Ibuprofen 200mg, Paracetamol 500mg. Doctor: Dr. Brown",
        "fields": {
            "patient_name": "Jane Smith",
            "medications": ["Ibuprofen", "Paracetamol"],
            "doctor_name": "Dr. Brown"
        }
    }
    
    # Test case 1: Perfect
    obs_perfect = {
        "ocr_text": "Patient: Jane Smith. Medications: Ibuprofen 200mg, Paracetamol 500mg. Doctor: Dr. Brown",
        "extracted_fields": {
            "patient_name": "Jane Smith",
            "medications": ["Ibuprofen", "Paracetamol"],
            "doctor_name": "Dr. Brown"
        }
    }
    score_perfect = grade_task("medium_handwritten_prescription", obs_perfect, ground_truth)
    print(f"Perfect: {score_perfect:.3f} (expected: 1.0)")
    
    # Test case 2: Good text, some fields
    obs_good = {
        "ocr_text": "Patient: Jane Smith. Medications: Ibuprofen 200mg, Paracetamol 500mg.",
        "extracted_fields": {
            "patient_name": "Jane Smith",
            "medications": ["Ibuprofen", "Paracetamol"]
        }
    }
    score_good = grade_task("medium_handwritten_prescription", obs_good, ground_truth)
    print(f"Good text + 2 fields: {score_good:.3f} (expected: 0.7-0.9)")
    
    # Test case 3: Decent text, 1 field
    obs_partial = {
        "ocr_text": "Patient: Jane Smith. Medications: Ibuprofen 200mg.",
        "extracted_fields": {
            "patient_name": "Jane Smith"
        }
    }
    score_partial = grade_task("medium_handwritten_prescription", obs_partial, ground_truth)
    print(f"Partial text + 1 field: {score_partial:.3f} (expected: 0.3-0.5)")
    
    # Test case 4: Poor text, no fields
    obs_poor = {
        "ocr_text": "Patient: Jane.",
        "extracted_fields": {}
    }
    score_poor = grade_task("medium_handwritten_prescription", obs_poor, ground_truth)
    print(f"Poor text, no fields: {score_poor:.3f} (expected: 0.0-0.3)")
    
    # Variance check
    scores = [score_perfect, score_good, score_partial, score_poor]
    variance = max(scores) - min(scores)
    print(f"\nScore variance: {variance:.3f}")
    
    if variance == 0.0:
        print("❌ CRITICAL: Grader always returns same score - WILL BE DISQUALIFIED!")
        return False
    else:
        print("✅ Grader produces varying scores")
        return True


def test_hard_grader():
    """Test hard task grader with varying quality inputs"""
    print("\n" + "="*60)
    print("Testing Hard Grader (Complex Prescription)")
    print("="*60)
    
    ground_truth = {
        "text": "Patient: Robert Johnson. Medications: Amoxicillin 500mg TID, Lisinopril 10mg QD, Metformin 850mg BID. Dosage: 500mg, 10mg, 850mg. Doctor: Dr. Anderson",
        "fields": {
            "patient_name": "Robert Johnson",
            "medications": ["Amoxicillin", "Lisinopril", "Metformin"],
            "dosage": ["500mg", "10mg", "850mg"],
            "doctor_name": "Dr. Anderson"
        }
    }
    
    # Test case 1: Perfect
    obs_perfect = {
        "ocr_text": "Patient: Robert Johnson. Medications: Amoxicillin 500mg TID, Lisinopril 10mg QD, Metformin 850mg BID. Dosage: 500mg, 10mg, 850mg. Doctor: Dr. Anderson",
        "extracted_fields": {
            "patient_name": "Robert Johnson",
            "medications": ["Amoxicillin", "Lisinopril", "Metformin"],
            "dosage": ["500mg", "10mg", "850mg"],
            "doctor_name": "Dr. Anderson"
        }
    }
    score_perfect = grade_task("hard_complex_prescription", obs_perfect, ground_truth)
    print(f"Perfect: {score_perfect:.3f} (expected: 1.0)")
    
    # Test case 2: Good text, most fields
    obs_good = {
        "ocr_text": "Patient: Robert Johnson. Medications: Amoxicillin 500mg TID, Lisinopril 10mg QD, Metformin 850mg BID. Dosage: 500mg, 10mg, 850mg.",
        "extracted_fields": {
            "patient_name": "Robert Johnson",
            "medications": ["Amoxicillin", "Lisinopril", "Metformin"],
            "dosage": ["500mg", "10mg", "850mg"]
        }
    }
    score_good = grade_task("hard_complex_prescription", obs_good, ground_truth)
    print(f"Good text + 3/4 fields: {score_good:.3f} (expected: 0.6-0.8)")
    
    # Test case 3: Decent text, some fields
    obs_partial = {
        "ocr_text": "Patient: Robert Johnson. Medications: Amoxicillin 500mg, Lisinopril 10mg.",
        "extracted_fields": {
            "patient_name": "Robert Johnson",
            "medications": ["Amoxicillin", "Lisinopril"]
        }
    }
    score_partial = grade_task("hard_complex_prescription", obs_partial, ground_truth)
    print(f"Partial text + 2/4 fields: {score_partial:.3f} (expected: 0.3-0.5)")
    
    # Test case 4: Poor
    obs_poor = {
        "ocr_text": "Patient: Robert.",
        "extracted_fields": {
            "patient_name": "Robert"
        }
    }
    score_poor = grade_task("hard_complex_prescription", obs_poor, ground_truth)
    print(f"Poor text + 1/4 fields: {score_poor:.3f} (expected: 0.1-0.3)")
    
    # Variance check
    scores = [score_perfect, score_good, score_partial, score_poor]
    variance = max(scores) - min(scores)
    print(f"\nScore variance: {variance:.3f}")
    
    if variance == 0.0:
        print("❌ CRITICAL: Grader always returns same score - WILL BE DISQUALIFIED!")
        return False
    else:
        print("✅ Grader produces varying scores")
        return True


def main():
    """Run all grader tests"""
    print("\n" + "="*60)
    print("GRADER VALIDATION TEST")
    print("Testing if graders produce varying scores (required to avoid disqualification)")
    print("="*60)
    
    results = []
    results.append(test_easy_grader())
    results.append(test_medium_grader())
    results.append(test_hard_grader())
    
    print("\n" + "="*60)
    print("FINAL RESULT")
    print("="*60)
    
    if all(results):
        print("✅ ALL GRADERS PASS - Produces varying scores")
        print("✅ Safe to submit (no disqualification risk from graders)")
        return 0
    else:
        print("❌ GRADER VALIDATION FAILED")
        print("❌ DO NOT SUBMIT - Will be disqualified!")
        print("\nFix graders to produce different scores for different quality inputs")
        return 1


if __name__ == "__main__":
    exit(main())
