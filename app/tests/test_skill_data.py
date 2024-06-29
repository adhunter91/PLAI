from app.services.skill_data import SkillData  # Ensure the correct path to your SkillData class

def main():
    # Instantiate the SkillData class
    skill_data = SkillData()

    # Add skills
    skill_data.add_skill("language_and_literacy", "test_skill_category1", "test_skill_id", 10)
    #skill_data.add_skill("Domain1", "Skill_Category1", "Skill_Name2_Skill_ID2", 20)

    # Retrieve a specific skill
    print(skill_data.get_skill("language_and_literacy", "test_skill_category", "test_skill_id"))  # Output: 10

    # Retrieve all values from a category
    all_values = skill_data.get_all_values_from_category("language_and_literacy", "test_skill_category")
    print(f"All values language_and_literacy from -> test_skill_category:", list(all_values))

    # Perform calculations on the retrieved values
    values_list = [value for skill_name_id, value in all_values]
    total = sum(values_list)
    average = total / len(values_list) if values_list else 0

    print(f"Total: {total}")
    print(f"Average: {average}")

    # Print the entire data structure
    print("Data structure:", skill_data)

    # Upload one skill to database
    response = skill_data.upsert_skill_value("11122233","language_and_literacy", "test_skill_category", "test_skill_id", 567)
    print("Upload response:", response)

    # Upload skills to the database (use a dummy user ID for testing)
    # response = skill_data.upload_to_db("11122233")
    #print("Upload response:", response)

    # Load skills from the database (use the same dummy user ID)
    skill_data.load_from_db("11122233")
    print("Loaded data structure:", skill_data)

if __name__ == "__main__":
    main()