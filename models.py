# models.py
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import numpy as np

class AIModel:
    def __init__(self):
        # Initialize a small language model
        self.generator = pipeline('text-generation', model='gpt2')
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
    
    def generate_response(self, user_input, knowledge_base):
        # First check knowledge base
        kb_response = self._check_knowledge_base(user_input, knowledge_base)
        if kb_response:
            return kb_response
        
        # Fallback to generative model
        return self.generator(user_input, max_length=50, do_sample=True)[0]['generated_text']
    
    def _check_knowledge_base(self, user_input, knowledge_base):
        # Encode user input
        input_embedding = self.encoder.encode(user_input, convert_to_tensor=True)
        
        # Compare against all knowledge topics
        best_match = None
        best_score = 0
        
        for topic_file in knowledge_base.storage_path.glob('*.json'):
            with open(topic_file, 'r') as f:
                topic_data = json.load(f)
                topic = topic_data['topic']
                
                # Encode topic
                topic_embedding = self.encoder.encode(topic, convert_to_tensor=True)
                
                # Calculate similarity
                score = util.pytorch_cos_sim(input_embedding, topic_embedding).item()
                
                if score > best_score:
                    best_score = score
                    best_match = topic_data
        
        if best_score > 0.7:  # Similarity threshold
            return f"Regarding {best_match['topic']}: {np.random.choice(best_match['information'])}"
        
        return None