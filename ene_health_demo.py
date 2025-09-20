#!/usr/bin/env python3
"""
EneHealths Agent Demo - Simple demonstration of the EneHealths agent functionality
"""

import sys
import os

from src.agents.ene_health_agent import EneHealthAgent

def main():
    """Main function to demonstrate EneHealths agent functionality."""
    print("Initializing EneHealths Agent...")
    
    # Initialize the EneHealths agent
    agent = EneHealthAgent()
    
    # Print welcome message
    print("\n" + "="*50)
    print("EneHealths Mental Health Support Agent")
    print("="*50)
    
    # Get mission and vision
    mission, vision = agent.get_mission_and_vision()
    print(f"\nMission: {mission}")
    print(f"Vision: {vision}")
    print("\n" + "="*50)
    
    # Demo scenarios
    scenarios = [
        "Tell me about EneHealths and what you do",
        "Can you tell me about depression symptoms?",
        "I've been feeling really down lately and sometimes think about hurting myself",
        "Is there a guaranteed cure for anxiety?",
        "What kind of support does EneHealths offer?"
    ]
    
    scenario_titles = [
        "About EneHealths",
        "Mental Health Information",
        "Sensitive Topic Handling",
        "Hallucination Detection",
        "Support Resources"
    ]
    
    for i, (title, scenario) in enumerate(zip(scenario_titles, scenarios), 1):
        print(f"\nDEMO SCENARIO {i}: {title}")
        print(f"\nUser: {scenario}")
        response = agent.process_input(scenario)
        print(f"Agent: {response}")
        
        # Show thought process for this scenario
        print("\nThought Process:")
        thoughts = agent.get_thought_history()
        # Show only the last 3 thoughts related to this scenario
        for thought in thoughts[-3:]:
            print(f"- {thought}")
            
        print("\n" + "-"*50)
    
    print("\n" + "="*50)
    print("End of EneHealths Agent Demo")
    print("="*50)

if __name__ == "__main__":
    main()