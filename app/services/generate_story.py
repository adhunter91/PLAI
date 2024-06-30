from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
print(load_dotenv(find_dotenv()))
# AI Tools: Claude, Sumo, 11laps, Midjourney, github copilot,
print(f"OpenAI API KEY: {os.getenv("OPENAI_API_KEY")} ")
def generate_story(score: int, max_tokens=500):

    OpenAI.api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
            {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
        ]
    )

    print(completion.choices[0].message)

    # Define a prompt based on the score
    #prompt = (f"You are a early child hood education specialist & a children's author with over 20 years of experience."
    #          f"You will generate stories for parents to read with their child."
    #          f"Generate a story that reflects a score of {score}. The scale is from 1 to 10. Any score under 7 requires a story."
    #           f" Write a kid's story about a princess named"
    #           f"Daisy. She's smart and loves to have fun. Include whimsical elements of traveling through a forest."
    #           f"Ensure the letter 'r' appears often in the story. Many words will use the letter r because that"
    #           f"is where the child is struggling.")

    # response = openai.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are an early child hood education specialist & a children's author with over 20 years of experience."
    #          "You will generate stories for parents to read with their child."
    #          },
    #         {"role": "user", "content": prompt}
    #     ],
    #     max_tokens=max_tokens,
        #n=1,
        #stop=None,
        #temperature=0.7,
    #)
    story = completion.choices[0].message
    # story = response.choices[0].text.strip()
    return story

if __name__ == "__main__":
    user_prompt = "Once upon a time in a land far, far away,"
    story = generate_story(5)
    print("Generated Story:")
    print(story)