from supabase import create_client
import os
from config import settings

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
