import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'test_value12345678910'
    SUPABASE_URL = os.getenv('SUPABASE_URL') #or supabase_url
    SUPABASE_KEY = os.getenv('SUPABASE_KEY') #or supabase_key
    DEBUG = True
    #DEBUG = False