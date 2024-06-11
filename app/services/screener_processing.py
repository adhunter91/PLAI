
#Filters data by skill which is denoted by "." in data
def filter_data_by_skill(data: dict[str, any]) -> dict[str, any]:
    filtered_data: dict = {}
    temp_key_1: list = []
    temp_key_2: list = []
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
    prefix_skills: dict[str, any] = {}
    prefix_counts: dict[str, int] = {}
    prefix_final: dict[str, float] = {}

    for key, value in data.items():
        prefix = key.rsplit('_', 1)[0] # splits the key value by "_" and grabs the first entry

        if value == "choice one" or "yes":
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
            total = prefix_skills[prefix]
            count = prefix_counts[prefix]
            prefix_final[prefix] = round(total / count, 2)

        #Likely will beed to edit this final output to keep track of outputs for database usage
        #print(f"Prefix_final: {prefix_final}")
    return prefix_final