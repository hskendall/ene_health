#!/usr/bin/env python3
"""
Standalone Demo for EneHealths Deepfake Counselor and Mental Health Advice

This script demonstrates the functionality of the DeepfakeCounselorAgent
without any external dependencies.
"""

import sys
import os

# Add the src directory to the path to import the agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.agents.deepfake_counselor import DeepfakeCounselorAgent


def run_interactive_demo():
    """Run an interactive demo of the DeepfakeCounselorAgent."""
    counselor = DeepfakeCounselorAgent()
    
    print("=" * 80)
    print("EneHealths Deepfake Counselor and Mental Health Advice Demo")
    print("=" * 80)
    print("\nThis agent can provide support for:")
    print("1. Deepfake-related concerns (victimization, anxiety about deepfakes)")
    print("2. Common mental health issues (anxiety, depression, stress, etc.)")
    print("\nType 'exit' to quit the demo.")
    print("=" * 80)
    
    while True:
        user_input = input("\nPlease enter your concern or question: ")
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("\nThank you for using the EneHealths Deepfake Counselor. Take care!")
            break
        
        response = counselor.process_input(user_input)
        print("\nCounselor Response:")
        print(response)


def run_preset_scenarios():
    """Run preset scenarios to demonstrate the DeepfakeCounselorAgent."""
    counselor = DeepfakeCounselorAgent()
    
    scenarios = [
        {
            "title": "Deepfake Victimization Concern",
            "input": "I just found out someone created a deepfake video with my face in it. I'm freaking out and don't know what to do."
        },
        {
            "title": "General Deepfake Anxiety",
            "input": "I'm worried about all these deepfakes I keep hearing about. How can I protect myself from being targeted?"
        },
        {
            "title": "Anxiety Symptoms",
            "input": "I've been feeling really anxious lately. My heart races, I worry constantly, and I'm having trouble sleeping. What can I do?"
        },
        {
            "title": "Depression Symptoms",
            "input": "I've been feeling really down for weeks. I don't enjoy anything anymore and just feel empty. Is this depression?"
        },
        {
            "title": "Grief Processing",
            "input": "My grandmother passed away last month and I'm still struggling to cope with it. I feel sad all the time."
        },
        {
            "title": "Insomnia Issues",
            "input": "I can't sleep at night. I lie awake for hours and when I do fall asleep, I wake up multiple times. I'm exhausted."
        },
        {
            "title": "Crisis Detection",
            "input": "I don't see any point in living anymore. Everything feels hopeless."
        }
    ]
    
    print("=" * 80)
    print("EneHealths Deepfake Counselor and Mental Health Advice Demo")
    print("=" * 80)
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\nScenario {i}: {scenario['title']}")
        print("-" * 40)
        print(f"User Input: {scenario['input']}")
        
        # Process the input and get response
        response = counselor.process_input(scenario['input'])
        
        print("\nCounselor Response:")
        print(response)
        print("=" * 80)
        
        # Pause between scenarios for readability
        if i < len(scenarios):
            input("\nPress Enter to continue to the next scenario...")


if __name__ == "__main__":
    print("Choose demo mode:")
    print("1. Run preset scenarios")
    print("2. Interactive mode")
    
    choice = input("\nEnter your choice (1 or 2): ")
    
    if choice == "1":
        run_preset_scenarios()
    elif choice == "2":
        run_interactive_demo()
    else:
        print("Invalid choice. Running preset scenarios by default.")
        run_preset_scenarios()