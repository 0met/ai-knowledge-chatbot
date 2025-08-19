# database.py
import json
import os
from pathlib import Path

class KnowledgeBase:
    def __init__(self, storage_path):
        self.storage_path = Path(storage_path)
        os.makedirs(self.storage_path, exist_ok=True)
    
    def add_knowledge(self, topic, information):
        topic_file = self.storage_path / f"{topic.lower().replace(' ', '_')}.json"
        
        if topic_file.exists():
            with open(topic_file, 'r') as f:
                data = json.load(f)
            data['information'].append(information)
        else:
            data = {'topic': topic, 'information': [information]}
        
        with open(topic_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def import_from_file(self, file):
        # Support various formats: JSON, TXT, CSV
        filename = file.filename.lower()
        
        if filename.endswith('.json'):
            data = json.load(file)
            for topic, info in data.items():
                self.add_knowledge(topic, info)
        
        elif filename.endswith('.txt'):
            content = file.read().decode('utf-8')
            # Simple format: Topic: Information
            for line in content.split('\n'):
                if ':' in line:
                    topic, info = line.split(':', 1)
                    self.add_knowledge(topic.strip(), info.strip())
        
        # Add other formats as needed
    
    def get_knowledge(self, topic):
        topic_file = self.storage_path / f"{topic.lower().replace(' ', '_')}.json"
        if topic_file.exists():
            with open(topic_file, 'r') as f:
                return json.load(f)
        return None