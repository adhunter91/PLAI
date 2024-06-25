from services.skill_data import SkillData  # Ensure the correct path to your SkillData class

def main():
    # Instantiate the SkillData class
    skill_data = SkillData()

    # Add skills
    skill_data.add_skill("Domain1", "Skill_Category1", "Skill_Name1_Skill_ID1", 10)
    skill_data.add_skill("Domain1", "Skill_Category1", "Skill_Name2_Skill_ID2", 20)

    # Retrieve a specific skill
    print(skill_data.get_skill("Domain1", "Skill_Category1", "Skill_Name1_Skill_ID1"))  # Output: 10

    # Retrieve all values from a category
    all_values = skill_data.get_all_values_from_category("Domain1", "Skill_Category1")
    print("All values from Domain1 -> Skill_Category1:", list(all_values))

    # Perform calculations on the retrieved values
    values_list = [value for skill_name_id, value in all_values]
    total = sum(values_list)
    average = total / len(values_list) if values_list else 0

    print(f"Total: {total}")
    print(f"Average: {average}")

    # Print the entire data structure
    print("Data structure:", skill_data)

    # Upload skills to the database (use a dummy user ID for testing)
    response = skill_data.upload_to_db("user123")
    print("Upload response:", response)

    # Load skills from the database (use the same dummy user ID)
    skill_data.load_from_db("user123")
    print("Loaded data structure:", skill_data)

if __name__ == "__main__":
    main()