import json
import os
from datetime import datetime
from pathlib import Path
from systems.react_agent import ReActAgents
import time

class Pass1Runner:
    
    def __init__(self):
        self.agent = ReActAgents(
            model_name="llama-3.3-70b-versatile",
            api_key="COMPLETE_RUN"
        )
        # create results directory if it doesn't exist
        os.makedirs("results/raw", exist_ok=True)

    def _extract_final_answer(self, text: str) -> str:
        if "Final Answer:" in text:
            return text.split("Final Answer:")[-1].strip()
        return text  # if no marker found, return full text

    def load_questions(self, filepath: str) -> list:
        """
        Load questions from a JSON file.
        
        Args:
            filepath: Path to the JSON file containing questions.
                Can be absolute or relative path.
        
        Returns:
            A list of questions loaded from the file.
            Returns empty list if file not found or JSON is invalid.
            # load questions from a json file
            # return the list of questions
        """
        path = Path(filepath)
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            questions = data.get('questions', [])
            return questions


    def run_question(self, question: dict) -> dict:
        query = question['question']
        question_id = question['id']
        correct_answer = question['correct_answer']
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                agent_result = self.agent.run(query)
                return {
                    'question_id': question_id,
                    'question': query,
                    'correct_answer': correct_answer,
                    'agent_answer': self._extract_final_answer(
                        agent_result.get('final_answer', '')
                    ),
                    'trace': agent_result.get('trace'),
                    'timestamp': datetime.now().isoformat()
                }
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for {question_id}: {e}")
                time.sleep(2)
                
        return {
            'question_id': question_id,
            'question': query,
            'correct_answer': correct_answer,
            'agent_answer': "FAILED after 3 attempts",
            'trace': [],
            'timestamp': datetime.now().isoformat()
        }
                
    def save_result(self, result: dict) -> None:
        """
        Save one result to results/raw/{question_id}.json.
        
        Args:
            result: Dictionary containing question results with 'question_id' key.
        """
        question_id = result.get('question_id', 'unknown')
        filepath = Path("results/raw") / f"{question_id}.json"
        filepath.parent.mkdir(parents=True, exist_ok=True)
    
        # Save as formatted JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"Saved: {filepath}")


    def run_all(self) -> None:
        math_questions = self.load_questions("questions/math.json")
        research_questions = self.load_questions("questions/research.json")
        for question in math_questions: 
            result = self.run_question(question)
            self.save_result(result)
            print("question saved")
            print("*"* 50)

        for question in research_questions: 
            result = self.run_question(question)
            self.save_result(result)
            print("question saved")
            print("*"* 50)
        

if __name__ == "__main__":
    runner = Pass1Runner()
    runner.run_all()
    
