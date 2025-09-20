#!/usr/bin/env python3
"""
Test script for EneHealths agent functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agents.ene_health_agent import EneHealthAgent
from src.agents.mental_health_detector import MentalHealthDetector
from src.agents.sensitive_content_handler import SensitiveContentHandler

def test_agent_initialization():
    """Test that the EneHealths agent initializes correctly."""
    print("Testing agent initialization...")
    agent = EneHealthAgent()
    assert agent is not None
    assert agent.ene_config is not None
    assert agent.knowledge_base is not None
    print("✓ Agent initialization successful")

def test_hallucination_detection():
    """Test mental health specific hallucination detection."""
    print("\nTesting hallucination detection...")
    detector = MentalHealthDetector(threshold=0.6)
    
    # Test with potentially misleading treatment claim
    response = "Depression can be completely cured with this revolutionary treatment that works for everyone."
    is_hallucination, score, explanation = detector.check_hallucination(response)
    assert is_hallucination, "Should detect hallucination in treatment claim"
    print(f"✓ Detected hallucination in treatment claim (score: {score:.2f})")
    
    # Test with appropriate treatment information
    response = "Research suggests that a combination of therapy and medication may be effective for many people with depression, though individual results vary."
    is_hallucination, score, explanation = detector.check_hallucination(response)
    assert not is_hallucination, "Should not detect hallucination in qualified statement"
    print(f"✓ Properly handled qualified treatment information (score: {score:.2f})")

def test_sensitive_content_handling():
    """Test sensitive content handling."""
    print("\nTesting sensitive content handling...")
    handler = SensitiveContentHandler()
    
    # Test crisis content detection
    crisis_text = "I've been thinking about suicide a lot lately"
    is_sensitive, is_crisis, topics = handler.check_content(crisis_text)
    assert is_sensitive and is_crisis, "Should detect crisis content"
    crisis_response = handler.get_crisis_response()
    assert "resources" in crisis_response.lower(), "Crisis response should include resources"
    print("✓ Crisis content detection and response working")
    
    # Test sensitive topic handling
    sensitive_text = "I experienced trauma in my childhood"
    is_sensitive, is_crisis, topics = handler.check_content(sensitive_text)
    assert is_sensitive and not is_crisis, "Should detect sensitive but not crisis content"
    formatted_response = handler.format_response("This is a response about trauma.", topics)
    assert "sensitive topic" in formatted_response.lower(), "Response should acknowledge sensitive nature"
    print("✓ Sensitive topic handling working")

def test_knowledge_integration():
    """Test that agent responses include knowledge from EneHealths."""
    print("\nTesting knowledge integration...")
    agent = EneHealthAgent()
    
    # Test response about EneHealths includes mission/vision
    response = agent._process_input("Tell me about EneHealths")
    assert "mission" in response.lower() or "vision" in response.lower(), "Response should include mission or vision"
    print("✓ EneHealths information integration working")

def main():
    """Run all tests."""
    print("="*50)
    print("TESTING ENEHEALTHS AGENT")
    print("="*50)
    
    try:
        test_agent_initialization()
        test_hallucination_detection()
        test_sensitive_content_handling()
        test_knowledge_integration()
        
        print("\n" + "="*50)
        print("✓ ALL TESTS PASSED")
        print("="*50)
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()