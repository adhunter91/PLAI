import os
from dotenv import load_dotenv, find_dotenv
from supabase import create_client, Client

### Note: add mapping to search for category names with category_id
### Mapping category_id -> {phonologoical awareness : 1, Print Knowledge : 2...}

# Load environment variables from .env file
load_dotenv(find_dotenv())
print(f"Supabase_URL: {os.getenv('SUPABASE_URL')}")
print(f"Supabase_API_KEY: {os.getenv('SUPABASE_KEY')}")
class SkillData:
    def __init__(self):
        self.data = {}
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_API_KEY')
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)

    def add_skill(self, domain, category, skill_name_id, value):
        if domain not in self.data:
            self.data[domain] = {}
        if category not in self.data[domain]:
            self.data[domain][category] = {}
        self.data[domain][category][skill_name_id] = value

    def get_skill(self, domain, category, skill_name_id):
        return self.data.get(domain, {}).get(category, {}).get(skill_name_id, None)

    def get_all_values_from_category(self, domain, category):
        return self.data.get(domain, {}).get(category, {}).items()

    def __str__(self):
        return str(self.data)

    def upsert_skill_value(self, user_id, domain, category, skill_name_id, value):
        # Create a dictionary for the skill filter
        skill_filter = {
            "user_id": user_id,
            "domain": domain,
            "category": category,
            "skill_name_id": skill_name_id,
        }

        # Check if the record exists # .match("{"skill_name_is" : TSkill83}")
        #existing_record = self.supabase.from_("skills").select("skill_name_id").match(skill_filter).execute()
        existing_record = self.supabase.from_("skills").select("skill_name_id").match({"skill_name_id" : "TSkill83"}).execute()
        print(f"This is the existing record: {existing_record}")

        if existing_record.data:
            # Record exists, update the value #VALUE NOT UPDTAED

            response = self.supabase.from_("skills").update({"value": value}).match({"skill_name_id" : "TSkill83"}).execute()
            print(f"Record alreadys exists, response: {response}, updated value: {value}")

        else:
            # Record does not exist, insert a new one
            skill_to_insert = skill_filter.copy()
            skill_to_insert["value"] = value
            print(f"Skill to insert: {skill_to_insert}")

            response = self.supabase.from_("skills").insert(skill_to_insert).execute()
            print(f"Record does not exist, response: {response}")

        return response
    def update_skill_value(self, user_id, domain, category, skill_name_id, value):
        # Create a dictionary for the skill to update
        skill_filter = {
            "user_id": user_id,
            "domain": domain,
            "category": category,
            "skill_name_id": skill_name_id,
        }

        # Update the value of the specified skill
        response = self.supabase.from_("skills").update({"value": value}).match(skill_filter).execute()
        return response
    def upload_all_to_db(self, user_id):
        # Flatten the data for upload
        skills_to_upload = []
        for domain, categories in self.data.items():
            for category, skills in categories.items():
                for skill_name_id, value in skills.items():
                    skills_to_upload.append({
                        "user_id": user_id,
                        "domain": domain,
                        "category": category,
                        "skill_name_id": skill_name_id,
                        "value": value
                    })

        response = self.supabase.from_("skills").insert(skills_to_upload).execute()
        return response

    def load_from_db(self, user_id):
        response = self.supabase.from_("skills").select("*").eq("user_id", user_id).execute()
        self.data = {}
        for record in response.data:
            domain, category, skill_name_id = record["domain"], record["category"], record["skill_name_id"]
            if domain not in self.data:
                self.data[domain] = {}
            if category not in self.data[domain]:
                self.data[domain][category] = {}
            self.data[domain][category][skill_name_id] = record["value"]
