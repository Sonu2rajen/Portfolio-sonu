from app.services.parser import parse_resume

sample_text = """
Rahul Sharma
rahul.sharma@gmail.com
+919876543210

Skills:
Python, SQL, FastAPI, Machine Learning

Education:
B.Tech in Computer Science

Experience:
Software Engineer at XYZ Company
"""

parsed_data = parse_resume(sample_text)
print(parsed_data)
