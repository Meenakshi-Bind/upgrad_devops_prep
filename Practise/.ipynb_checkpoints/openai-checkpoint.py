import openai
import os

# Set your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

def evaluate_writing(topic, answer):
    prompt = f"""
    You are an English language evaluator for the Duolingo English Test. Your task is to assess the following written response based on the given topic. Provide a score out of 30 and a brief explanation highlighting the strengths and areas for improvement.

    **Topic:**
    {topic}

    **Answer:**
    {answer}

    **Evaluation:**
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that evaluates English writing based on the Duolingo English Test criteria."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.5,
    )

    evaluation = response.choices[0].message['content'].strip()
    return evaluation

def main():
    print("=== Duolingo English Test Writing Evaluator ===\n")
    
    topic = input("Enter the writing topic: ")
    print("\nEnter your answer below. When you're done, press Enter twice:\n")
    
    # Collect multi-line input
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    answer = "\n".join(lines)
    
    print("\nEvaluating your writing...\n")
    evaluation = evaluate_writing(topic, answer)
    print("=== Evaluation ===")
    print(evaluation)

if __name__ == "__main__":
    main()
