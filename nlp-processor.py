#!/usr/bin/env python3
import sys
import spacy
import json

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Compliance keywords (including multi-word phrases)
compliance_keywords = {"user data", "pii","encrypted","encryption", "gdpr", "pci dss"}

# Read from stdin
for line in sys.stdin:
    try:
        # Load the event in JSON format
        event = json.loads(line)
        log_message = event.get("message", "")
        print(f"Debug: Log message = {log_message}", file=sys.stderr)  # Debug statement

        # Convert log message to lowercase for case-insensitive matching
        log_message_lower = log_message.lower()

        # Extract compliance-related keywords
        extracted_keywords = [keyword for keyword in compliance_keywords if keyword in log_message_lower]

        print(f"Debug: Extracted keywords = {extracted_keywords}", file=sys.stderr)  # Debug statement

        # Add extracted keywords to the event
        if extracted_keywords:
            event["compliance_data"] = extracted_keywords
            print(json.dumps(event))
        else:
            # Optionally handle messages without compliance data
            print(json.dumps(event))
    except Exception as e:
        # Handle exceptions (e.g., invalid JSON)
        print(f"Error: {e}", file=sys.stderr)  # Debug statement
        print(json.dumps(event))