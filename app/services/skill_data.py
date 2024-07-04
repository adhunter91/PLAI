import os
import re
import logging
from dotenv import load_dotenv, find_dotenv
from supabase import create_client, Client

### Note: add mapping to search for category names with category_id
### Mapping category_id -> {phonologoical awareness : 1, Print Knowledge : 2...}

# Load environment variables from .env file
load_dotenv(find_dotenv())
print(f"Supabase_URL: {os.getenv('SUPABASE_URL')}")
print(f"Supabase_API_KEY: {os.getenv('SUPABASE_KEY')}")
class SkillData:

    # Mappings defined for easy mapping from the screener based on the skill_name_id

    skill_name_to_category: dict[str, str] = {
        'phaw' : 'phonological_awareness',
        'prkn' : 'print_knowledge',
        'ak' : 'alphabet_knowledge',
        'co' : 'comprehension',
        'ts' : 'text_structure',
        'wr' : 'writing',
        'tskill' : 'test_skill_category'
    }

    skill_name_to_domain: dict[str, str] = {
        'phaw': 'language_and_literacy',
        'prkn': 'language_and_literacy',
        'ak': 'language_and_literacy',
        'co': 'language_and_literacy',
        'ts': 'language_and_literacy',
        'wr': 'language_and_literacy',
        'tskill': 'language_and_literacy'
    }


    skill_category_to_skill_category_id: dict[str, int] = {
        'phonological_awareness' : 1,
        'print_knowledge' : 2,
        'alphabet_knowledge' : 3,
        'comprehension' : 4,
        'text_structure' : 5,
        'writing' : 6,
        'test_skill_category' : 7
    }

    positive_values = {'choice one', 'yes'}
    def __init__(self):
        self.data: dict[str, dict[str, dict[str, any]]] = {}
        self.supabase_url: str = os.getenv('SUPABASE_URL')
        self.supabase_key: str = os.getenv('SUPABASE_API_KEY')
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        self.skill_name_id_mapping: dict[str, str] = {
            'phaw': 'PhAw',
            'prkn': 'PrKn',
            'ak': 'AK',
            'co': 'CO',
            'ts': 'TS',
            'wr': 'WR',
            'tskill': 'TSkill'
        }

    def add_skill(self, domain, category, skill_name_id, value):
        binary_value = 1 if value.lower() in SkillData.positive_values else 0
        if domain not in self.data:
            self.data[domain] = {}
        if category not in self.data[domain]:
            self.data[domain][category] = {}

        if skill_name_id in self.data[domain][category]:
            logging.info(f"Updating existing skill: Domain='{domain}', Category='{category}', Skill ID='{skill_name_id}', Old Value='{self.data[domain][category][skill_name_id]}', New Value='{value}'")
        else:
            logging.info(f"Adding new skill: Domain='{domain}', Category='{category}', Skill ID='{skill_name_id}', Value='{value}'")
        self.data[domain][category][skill_name_id] = binary_value

    def get_skill(self, domain: str, category: str , skill_name_id: str) -> any:
        return self.data.get(domain, {}).get(category, {}).get(skill_name_id, None)

    def get_all_values_from_category(self, domain: str , category: str) -> dict[str, int].items:
        values = dict(self.data.get(domain, {}).get(category, {}).items())
        logging.info(f"Values for domain '{domain}', category '{category}': {values}")
        return values

    def __str__(self):
        return str(self.data)

    def determine_category(self, skill_name_id: str) -> str:
        cleaned_skill_name_id: str = ''.join([i for i in skill_name_id.lower() if not i.isdigit()])
        return SkillData.skill_name_to_category.get(cleaned_skill_name_id, "Unknown Category")

    def determine_domain(self, skill_name_id: str) -> str:
        cleaned_skill_name_id: str = ''.join([i for i in skill_name_id.lower() if not i.isdigit()])
        return SkillData.skill_name_to_domain.get(cleaned_skill_name_id, "Unknown Domain")

# Convert to upsert_value, make table selection dynamic


    #This categorizes the screener into the correct values for the database
    def preprocess_screener(self, webhook_data: dict[str, any]) -> None:
        for key, value in webhook_data.items():
            domain_with_skill, skill_value = key.lower(), value
            parts = domain_with_skill.split('.')


            if len(parts) < 2:
                print(f"Invalid key format: {key}")
                continue

            skill_name_id = parts[1]  # Only take the first two parts
            category = self.determine_category(skill_name_id)
            domain_full_name = self.determine_domain(skill_name_id)

            #logging.debug(f"Domain part: {domain}, Mapped domain: {domain_full_name}")
            #logging.debug(f"Skill name ID part: {skill_name_id}, Mapped category: {category}")

            if domain_full_name != "Unknown Domain" and category != "Unknown Category":
                self.add_skill(domain_full_name, category, skill_name_id, skill_value)
                logging.info(f"Domain: {domain_full_name}, Category: {category}, Skill ID: {skill_name_id}, Value: {value}")
            else:
                logging.warning(f"Unrecognized domain or category for {key}")

        logging.info(f"Data after preprocessing screener results: {self.data}")

    def print_skills(self) -> None:
        for domain, categories in self.data.items():
            for category, skills in categories.items():
                for skill_name_id, value in skills.items():
                    logging.info(f"Domain: {domain}, Category: {category}, Skill ID: {skill_name_id}, Value: {value}")
                    #print(f"Domain: {domain}, Category: {category}, Skill ID: {skill_name_id}, Value: {value}")

    def print_data(self) -> None:
        logging.info("Printing all data:")
        for domain, categories in self.data.items():
            logging.info(f"Domain: {domain}")
            for category, skills in categories.items():
                logging.info(f"  Category: {category}")
                for skill_name_id, value in skills.items():
                    logging.info(f"    Skill ID: {skill_name_id}, Value: {value}")

    def calculate_score_in_category(self, domain: str, category: str) -> dict[str, int]:
        values = self.get_all_values_from_category(domain, category)
        total_questions = len(values)
        correct_answers = sum(values.values())
        summary = {
            "total_questions": total_questions,
            "correct_answers": correct_answers
        }
        logging.info(f"Summary for domain '{domain}', category '{category}': {summary}")
        return summary

    def calculate_score_in_all_categories(self) -> dict[str, dict[str, dict[str, int]]]:
        scores = {}
        for domain, categories in self.data.items():
            scores[domain] = {}
            for category in categories:
                scores[domain][category] = self.calculate_score_in_category(domain, category)
        logging.info(f"Scores for all categories: {scores}")
        return scores

    def initialize_user_tmp(self, email: str) -> str:
        # Insert the user into the database
        response = self.supabase.from_("users").insert({"email": email}).execute()
        if not response.data:
            logging.error(f"Error inserting user: {response.status_code} - {response.error_message}")
            return None
        user_id = response.data[0]['user_id']
        logging.info(f"User initialized with ID: {user_id}")
        return user_id

    def extract_email_from_webhook(self, webhook_data: dict[str, any]) -> str:
        # Extract email from the webhook data
        email = webhook_data.get('email')
        if email:
            logging.info(f"Extracted email from webhook: {email}")
        else:
            logging.warning("No email found in webhook data")
        return email
    def update_skill_value(self, user_id: str, domain: str, category: str, skill_name_id: str, value: any):
        # Create a dictionary for the skill to update
        skill_filter = {
            "user_id": user_id,
            "domain": domain,
            "category": category,
            "skill_name_id": skill_name_id,
        }

        # Update the value of the specified skill
        response = self.supabase.from_("skills").update({"skill_value": skill_value}).match(skill_filter).execute()
        return response
    def upload_all_skill_values_to_db(self, user_id: int):
        # Flatten the data for upload
        skill_values_to_upload = []
        for domain, categories in self.data.items():
            for category, skills in categories.items():
                for skill_name_id, skill_value in skills.items():
                    print(f"    Processing skill: {skill_name_id} with value: {skill_value}")

                    # Transform the skill_name_id
                    transformed_skill_name_id = self.transform_variable_name(skill_name_id, self.skill_name_id_mapping)


                    skill_values_to_upload.append({
                        "user_id": user_id,
                        "skill_name_id": transformed_skill_name_id,
                        "skill_value": skill_value
                    })

                    #response = self.supabase.from_("skills").insert(skill_values_to_upload).execute()
                    response = self.upsert_skill_value(user_id, transformed_skill_name_id, skill_value)
        #if response.status not in range(200, 300):
        #    logging.error(f"Error inserting skill values: {response.status} - {response.data}")
        #else:
        #    logging.info(f"Inserted skill values successfully: {response.data}")
        return response

    #Add table into arguments and restructure
    def upsert_skill_value(self, user_id, skill_name_id, skill_value):
        # Create a dictionary for the skill filter
        skill_filter = {
            "user_id": user_id,
            "skill_name_id": skill_name_id,
        }

        # Check if the record exists # .match("{"skill_name_is" : TSkill83}")
        # existing_record = self.supabase.from_("skills").select("skill_name_id").match(skill_filter).execute()
        existing_record = self.supabase.from_("skill_scores").select("skill_name_id").match(skill_filter).execute()
        print(f"This is the existing record: {existing_record}")

        if existing_record.data:
            # Record exists, update the value #VALUE NOT UPDATED

            response = self.supabase.from_("skill_scores").update({"skill_value": skill_value}).match(
                skill_filter).execute()
            print(f"Record already exists, response: {response}, updated skill_value: {skill_value}")

        else:
            # Record does not exist, insert a new one
            skill_to_insert = skill_filter.copy()
            skill_to_insert["skill_value"] = skill_value
            skill_to_insert["user_id"] = user_id
            print(f"Skill to insert: {skill_to_insert}")

            response = self.supabase.from_("skill_scores").insert(skill_to_insert).execute()
            print(f"Record does not exist, response: {response}")

        return response


    def insert_scores_by_category_into_db(self, user_id: str, scores: dict[str, dict[str, dict[str, int]]]) -> None:
        score_records = []
        for domain, categories in scores.items():
            for category, score in categories.items():
                score_records.append({
                    "user_id": user_id,
                    "domain": domain,
                    "category": category,
                    "total_questions": score["total_questions"],
                    "correct_answers": score["correct_answers"]
                })

        # Assuming the table for scores is named 'category_scores'
        response = self.supabase.from_("category_scores").insert(score_records).execute()
        ### search for this error code, add into code
        #if response.status_code not in range(200, 300):
        #    logging.info(f"Inserted scores by category successfully: {response.data}")
        #else:
        #    logging.error(f"Error inserting scores by category: {response.status_code} - {response.error_message}")
        return response

    def load_from_db(self, user_id: int):
        response = self.supabase.from_("skills").select("*").eq("user_id", user_id).execute()
        self.data = {}
        for record in response.data:
            domain, category, skill_name_id = record["domain"], record["category"], record["skill_name_id"]
            if domain not in self.data:
                self.data[domain] = {}
            if category not in self.data[domain]:
                self.data[domain][category] = {}
            self.data[domain][category][skill_name_id] = record["value"]


    def transform_variable_name(self, variable_name: str, mapping: dict[str, str]) -> str:
        match = re.match(r"([a-zA-Z]+)(\d+)", variable_name)
        if not match:
            return variable_name

        alpha_part, num_part = match.groups()
        transformed_alpha_part = mapping.get(alpha_part, alpha_part)
        return f"{transformed_alpha_part}{num_part}"

    def transform_keys_in_dict(input_dict: dict[str, any], mapping: dict[str, str]) -> dict[str, any]:
        transformed_dict: dict[str, any] = {}
        for key, value in input_dict.items():
            transformed_key = transform_variable_name(key, mapping)
            transformed_dict[transformed_key] = value
        return transformed_dict