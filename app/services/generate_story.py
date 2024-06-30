from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
# AI Tools: Claude, Sumo, 11laps, Midjourney, github copilot,
#print(f"OpenAI API KEY: {os.getenv("OPENAI_API_KEY")} ")
def generate_story(score: int, max_tokens=500):

    OpenAI.api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI()
    role_prompt: str = f"""You are a early child hood education specialist & a children's author with over 20 years of experience.
              You will generate stories for parents to read with their child.
              The scale is from 1 to 10. Any score under 7 requires a story.
              Generate a story that based on a score of {score}."""
    prompt: str = f"""Write a children's story about a princess named Janelle.
              She's smart and loves to have fun. Include whimsical elements of traveling through a forest.
              Ensure words start letter 'r' often in the story. Many words will use the letter r because that
              is where the child is struggling. Use 100 words MAXIMUM. MAKE SURE TO END THE STORY BASED ON THE LIMIT"""
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": role_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    print(completion.choices[0].message.content)

    story = completion.choices[0].message.content # ".content" gives the story without other stuff

    # story = response.choices[0].text.strip()
    return story

if __name__ == "__main__":
    user_prompt = "Once upon a time in a land far, far away,"
    story = generate_story(5)
    print("Generated Story:")
    print(story)