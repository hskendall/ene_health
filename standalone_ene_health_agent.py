#!/usr/bin/env python3
"""
Standalone EneHealths Agent - No external dependencies required
"""

class SimpleHallucinationDetector:
    """Simple hallucination detector for mental health topics"""
    
    def __init__(self, threshold=0.7):
        self.threshold = threshold
        self.medical_claims = [
            "cure", "guaranteed", "always works", "100% effective",
            "miracle", "instant relief", "permanent solution"
        ]
    
    def check_hallucination(self, text):
        """Check if text contains potential hallucinations"""
        text = text.lower()
        
        # Check for absolute medical claims
        for claim in self.medical_claims:
            if claim in text:
                return {
                    "is_hallucination": True,
                    "explanation": f"The statement contains potentially misleading medical claims like '{claim}'. Mental health treatments vary in effectiveness for different individuals."
                }
        
        return {
            "is_hallucination": False,
            "explanation": "No potential hallucinations detected."
        }

class SimpleThoughtTracker:
    """Simple thought process tracker"""
    
    def __init__(self, max_history=10):
        self.thoughts = []
        self.max_history = max_history
    
    def add_thought(self, thought):
        """Add a thought to the history"""
        self.thoughts.append(thought)
        if len(self.thoughts) > self.max_history:
            self.thoughts.pop(0)
    
    def get_thoughts(self):
        """Get all thoughts in history"""
        return self.thoughts

class EneHealthsAgent:
    """
    Standalone EneHealths agent for mental health support.
    No external dependencies required.
    """
    
    def __init__(self):
        """Initialize the EneHealths agent"""
        # Load configuration
        self.config = self._load_config()
        
        # Initialize components
        self.hallucination_detector = SimpleHallucinationDetector(
            threshold=self.config.get('hallucination_threshold', 0.7)
        )
        
        self.thought_tracker = SimpleThoughtTracker(
            max_history=self.config.get('thought_history_size', 10)
        )
        
        # Load knowledge base
        self.knowledge_base = self._load_knowledge_base()
        
        # Set up sensitive content handling
        self.sensitive_topics = self.config.get('sensitive_topics', [])
        self.crisis_keywords = self.config.get('crisis_keywords', [])
        self.support_resources = self.config.get('support_resources', {})
    
    def _load_config(self):
        """Load configuration"""
        return {
            'name': 'EneHealths Assistant',
            'hallucination_threshold': 0.8,
            'thought_history_size': 15,
            'sensitive_topics': [
                'suicide', 'self-harm', 'abuse', 'trauma', 
                'eating disorders', 'addiction', 'crisis'
            ],
            'crisis_keywords': [
                'kill myself', 'end my life', 'suicide', 'hurt myself',
                'self-harm', 'die', 'don\'t want to live', 'emergency'
            ],
            'support_resources': {
                'crisis': '988 Suicide & Crisis Lifeline (call or text 988)',
                'text': 'Text HOME to 741741 to reach Crisis Text Line',
                'veterans': 'Veterans Crisis Line: 1-800-273-8255 and Press 1',
                'general': 'SAMHSA\'s National Helpline: 1-800-662-HELP (4357)'
            }
        }
    
    def _load_knowledge_base(self):
        """Load knowledge base"""
        return {
            'organization': {
                'name': 'EneHealths',
                'website': 'https://enehealths.org',
                'mission': 'To provide accessible mental health resources and support to all individuals.',
                'vision': 'A world where mental health care is accessible, stigma-free, and integrated into everyday life.'
            },
            'mental_health_topics': [
                'anxiety', 'depression', 'stress management', 'trauma',
                'self-care', 'mindfulness', 'therapy options', 'medication',
                'crisis support', 'support groups', 'wellness', 'resilience'
            ],
            'services': {
                'counseling': 'Individual and group counseling services',
                'assessment': 'Mental health assessments and screening',
                'referrals': 'Referrals to specialized mental health providers',
                'education': 'Mental health education and workshops',
                'support_groups': 'Peer support groups for various mental health concerns',
                'crisis_intervention': 'Crisis intervention and support'
            },
            'resources': {
                'articles': 'Evidence-based articles on mental health topics',
                'videos': 'Educational videos about mental health',
                'worksheets': 'Self-help worksheets and exercises',
                'apps': 'Recommended mental health apps and digital tools',
                'books': 'Recommended reading on mental health topics',
                'community': 'Online community forums for peer support'
            },
            'faqs': {
                'what_is_therapy': 'Therapy is a collaborative treatment based on the relationship between an individual and a mental health professional.',
                'how_to_find_therapist': 'You can find a therapist through your insurance provider, referrals from healthcare providers, or community mental health centers.',
                'therapy_cost': 'The cost of therapy varies based on location, therapist credentials, and insurance coverage.',
                'crisis_help': 'If you\'re experiencing a mental health crisis, contact emergency services (911) or call the 988 Suicide & Crisis Lifeline.'
            }
        }
    
    def process_input(self, user_input):
        """Process user input and generate response"""
        # Track thought process
        self.thought_tracker.add_thought(f"Received input: {user_input}")
        
        # Check for crisis or sensitive content
        if self._is_crisis_situation(user_input):
            self.thought_tracker.add_thought("Detected crisis situation, providing emergency resources")
            return self._handle_crisis_situation()
        
        if self._contains_sensitive_topic(user_input):
            self.thought_tracker.add_thought("Detected sensitive topic, providing careful response")
            return self._handle_sensitive_topic(user_input)
        
        # Check for hallucination risk
        hallucination_check = self.hallucination_detector.check_hallucination(user_input)
        if hallucination_check['is_hallucination']:
            self.thought_tracker.add_thought(f"Potential hallucination detected: {hallucination_check['explanation']}")
            return self._handle_hallucination(hallucination_check)
        
        # Process regular input
        self.thought_tracker.add_thought("Processing regular input")
        return self._generate_response(user_input)
    
    def _is_crisis_situation(self, text):
        """Check if text indicates a crisis situation"""
        text = text.lower()
        for keyword in self.crisis_keywords:
            if keyword in text:
                return True
        return False
    
    def _contains_sensitive_topic(self, text):
        """Check if text contains sensitive topics"""
        text = text.lower()
        for topic in self.sensitive_topics:
            if topic in text:
                return True
        return False
    
    def _handle_crisis_situation(self):
        """Handle crisis situation"""
        response = "I notice you may be experiencing a crisis. Your well-being is important, and immediate support is available.\n\n"
        response += "Please consider these resources:\n"
        
        for resource_name, resource_info in self.support_resources.items():
            response += f"- {resource_info}\n"
            
        response += "\nIf you're in immediate danger, please call emergency services (911) or go to your nearest emergency room."
        
        return response
    
    def _handle_sensitive_topic(self, user_input):
        """Handle sensitive topic"""
        # Identify which sensitive topic is present
        topic = None
        for t in self.sensitive_topics:
            if t in user_input.lower():
                topic = t
                break
                
        # Formulate a careful response
        response = f"I understand you're asking about {topic}, which is an important mental health concern. "
        response += "I want to provide helpful information while acknowledging that everyone's experience is unique.\n\n"
        
        response += "EneHealths offers resources and support for individuals dealing with this issue. "
        response += "Speaking with a mental health professional can provide personalized support."
        
        return response
    
    def _handle_hallucination(self, hallucination_check):
        """Handle potential hallucination"""
        response = "I want to make sure I provide accurate information. "
        response += hallucination_check['explanation'] + " "
        response += "I can help you find reliable information about mental health topics from EneHealths."
        
        return response
    
    def _generate_response(self, user_input):
        """Generate response based on user input"""
        user_input = user_input.lower()
        
        # About EneHealths
        if any(keyword in user_input for keyword in ['who are you', 'about enehealths', 'what is enehealths']):
            return self._get_about_response()
            
        # Services information
        if any(keyword in user_input for keyword in ['services', 'help', 'support', 'offer']):
            return self._get_services_response()
            
        # Mental health topics
        for topic in self.knowledge_base['mental_health_topics']:
            if topic in user_input:
                return self._get_topic_info(topic)
                
        # FAQ responses
        for question, answer in self.knowledge_base['faqs'].items():
            keywords = question.split('_')
            if all(keyword in user_input for keyword in keywords):
                return answer
                
        # Default response
        return "I'm here to provide information about mental health and EneHealths services. How can I assist you today?"
    
    def _get_about_response(self):
        """Get information about EneHealths"""
        org = self.knowledge_base['organization']
        response = f"{org['name']} is a mental health organization dedicated to {org['mission']}\n\n"
        response += f"Our vision is {org['vision']}\n\n"
        response += f"You can learn more at {org['website']}"
        
        return response
    
    def _get_services_response(self):
        """Get information about EneHealths services"""
        response = "EneHealths offers the following mental health services:\n\n"
        
        for service, description in self.knowledge_base['services'].items():
            response += f"- {service.replace('_', ' ').title()}: {description}\n"
            
        return response
    
    def _get_topic_info(self, topic):
        """Get information about a specific mental health topic"""
        response = f"Information about {topic}:\n\n"
        
        if topic == 'anxiety':
            response += "Anxiety is a normal emotion that can cause feelings of worry, fear, or tension. When these feelings become excessive, it may be an anxiety disorder. Treatment options include therapy, medication, and self-care practices."
        elif topic == 'depression':
            response += "Depression is a common but serious mood disorder that causes persistent feelings of sadness and loss of interest. Treatment typically includes therapy, medication, or a combination of both."
        elif topic == 'stress management':
            response += "Stress management encompasses techniques to cope with and reduce stress. Effective strategies include regular exercise, relaxation techniques, maintaining social connections, and practicing self-care."
        else:
            response += f"EneHealths provides resources, education, and support for individuals dealing with {topic}."
            
        return response
    
    def get_thought_history(self):
        """Get thought process history"""
        return self.thought_tracker.get_thoughts()
    
    def get_mission_and_vision(self):
        """Get EneHealths mission and vision"""
        org = self.knowledge_base['organization']
        return org['mission'], org['vision']


def main():
    """Main function to demonstrate EneHealths agent"""
    print("Initializing EneHealths Agent...")
    agent = EneHealthsAgent()
    
    # Print mission and vision
    print("\n=== EneHealths Mission and Vision ===")
    mission, vision = agent.get_mission_and_vision()
    print(f"Mission: {mission}")
    print(f"Vision: {vision}")
    
    # Demo scenarios
    scenarios = [
        "What is EneHealths?",
        "What services do you offer?",
        "I'm feeling anxious all the time",
        "I think I have a rare condition called hypersomnolent disorder that makes me sleep 20 hours a day",
        "I'm having thoughts about hurting myself"
    ]
    
    print("\n=== Demo Scenarios ===")
    for i, scenario in enumerate(scenarios, 1):
        print(f"\nScenario {i}: '{scenario}'")
        response = agent.process_input(scenario)
        print(f"Response: {response}")
        
        # Show thought process for this scenario
        print("\nThought Process:")
        thoughts = agent.get_thought_history()
        # Show only the last 3 thoughts related to this scenario
        for thought in thoughts[-3:]:
            print(f"- {thought}")
        
        print("\n" + "-"*50)
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()