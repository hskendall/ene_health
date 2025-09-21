#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Voice Agent with Hallucination Detection

This application creates a voice agent that can detect hallucinations in AI responses
and narrate its thought process when requested by the user.
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import local modules
from src.voice_agent import VoiceAgent
from src.ui.main_window import MainWindow
from PyQt5.QtWidgets import QApplication


def main():
    """Main entry point for the application."""
    # Initialize the application
    app = QApplication(sys.argv)
    
    # Create the voice agent
    voice_agent = VoiceAgent()
    
    # Create and show the main window
    main_window = MainWindow(voice_agent)
    main_window.show()
    
    # Start the application event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()