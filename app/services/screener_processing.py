
#Filters data by skill which is denoted by "." in data
def filter_data_by_skill(data: dict[str, any]) -> dict[str, any]:
    filtered_data: dict = {}
    temp_key_1: list = []
    temp_key_2: list = []
    # Domain.Skill_Category.Skill.Skill_ID
    # Maybe I make multiple functions for filtering
    # This one is for skill, make one for each level
    # -> Skill_Category.Skill.Skill_ID
    # -> Skill.Skill_ID
    # -> I can also make a nested dictionary
    for key, value in data.items():
        if isinstance(value, str):
            temp_key_1 = key.split(".")
            if len(temp_key_1) > 1:
                temp_key_2 = temp_key_1[1:]
                key_out = temp_key_2[0] + "_" + temp_key_2[1]
                filtered_data[key_out] = value.lower()
        else:
            pass
    return filtered_data


def find_total_skills(data: dict[str, str]) -> dict[str, any]:

    # Initialize Dictionaries to track matched skills and to track total number of skills
    prefix_skills: dict[str, any] = {}
    prefix_counts: dict[str, int] = {}
    prefix_final: dict[str, float] = {}
    positive_values = {"choice one", "yes"}

    for key, value in data.items():
        prefix = key.rsplit('_', 1)[0] # splits the key value by "_" and grabs the first entry

        if value in positive_values:
            value = 1
        else:
            value = 0

        if prefix in prefix_skills:
            prefix_skills[prefix] += value
            prefix_counts[prefix] += 1
        else:
            prefix_skills[prefix] = value
            prefix_counts[prefix] = 1

        #print(f"Current Prefix value: {prefix_skills}")
        for prefix in prefix_skills:
            matched = prefix_skills[prefix]
            total = prefix_counts[prefix]
            prefix_final[prefix] = [matched, total]
            #prefix_final[prefix] = round(total / count, 2)

        #Likely will need to edit this final output to keep track of outputs for database usage
        #print(f"Prefix_final: {prefix_final}")
    return prefix_final

def map_skills_to_categories(data: dict[str, any]) -> dict[str, any]:
    # Domain.Skill_Category.Skill_name.KR1
    # Take input from previous mapping to categories.
    # Map categories to output numbers for
    # define naming convention for mapping in setup so logic is easier
    # Will need specific KR skill AND Skill Category, maybe include both in naming?
    pass



def pass_result_to_url(result: list[int]):
    base_url:str = "https://kready.com/view-my-report"
    url_with_params:str = f"{base_url}?result={result}"
    #PA Phonological Awareness
    #PK Print Knowledge
    #Alphabet Knowledge