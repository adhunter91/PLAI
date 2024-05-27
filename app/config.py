import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test_value12345678910'
    SUPABASE_URL = os.environ.get('SUPABASE_URL') or
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY') or
    DEBUG = False