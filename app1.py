import sqlite3
import re
import spacy
import logging
from typing import Optional, List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Load spaCy model with error handling
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    logger.warning("SpaCy model not found. Some NLP features may be limited.")
    nlp = None

class MiniNLPChatbot:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        
        # Define a larger set of intent mappings with underscores for method names
        self.intent_map = {
            "roll_number": ["roll number", "registration number", "student id", "student roll", "student identifier", "enrollment number"],
            "cgpa": ["cgpa", "gpa", "grades", "academic performance", "cgpa score", "grade point average", "academic standing"],
            "batch": ["batch", "year of admission", "students in batch", "year group", "admission year"],
            "certifications": ["certifications", "courses completed", "achievements", "credentials", "certificates"],
            "skills": ["skills", "competencies", "abilities", "expertise", "proficiencies", "technical skills"],
            "projects": ["projects", "assignments", "work done", "completed projects", "project list", "academic projects"],
            "address": ["address", "location", "residence", "living in", "staying at", "home address"],
            "attendance": ["attendance", "presence", "absences", "attended classes", "class attendance"],
            "department": ["department", "branch", "course", "academic stream", "major"],
            "dob": ["dob", "date of birth", "birthdate", "birthday"],
            "contact": ["contact", "phone number", "email", "phone", "contact details"],
            "academic_calendar": ["academic calendar", "important dates", "semester schedule", "academic events"],
            "backlogs": ["backlogs", "failed subjects", "arrears", "pending subjects", "uncleared courses"]
        }

        # Caching mechanism to reduce database lookups
        self.query_cache: Dict[str, Any] = {}

    def process_query(self, query):
        query = query.lower().strip()
        
        # Check cache first
        if query in self.query_cache:
            logger.info(f"Cache hit for query: {query}")
            return self.query_cache[query]

        for intent, keywords in self.intent_map.items():
            if any(keyword in query for keyword in keywords):
                try:
                    # Call the corresponding handler dynamically
                    result = getattr(self, f"handle_{intent}_query")(query)
                    # Cache the result
                    self.query_cache[query] = result
                    return result
                except Exception as e:
                    logger.error(f"Error processing {intent} query: {e}")
                    return "An error occurred while processing your query."

        return "I'm sorry, I didn't understand your query. Can you rephrase it?"

    def safe_database_query(self, query: str, params: tuple) -> Optional[List[Any]]:
        """
        Wrapper for database queries with error handling
        """
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Database query error: {e}")
            return None

    def extract_name(self, query):
        # Improved name extraction with multiple fallback mechanisms
        if nlp:
            doc = nlp(query)
            names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
            if names:
                return names[0]

        # Fallback to regex patterns for name extraction
        name_patterns = [
            r"of ([\w\s]+)",
            r"tell me about ([\w\s]+)",
            r"information for ([\w\s]+)",
            r"details of ([\w\s]+)"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, query)
            if match:
                return match.group(1).strip()

        return None

    def extract_year(self, query):
        # More robust year extraction
        years = re.findall(r'\b(19\d{2}|20\d{2})\b', query)
        return years[0] if years else None

    # Specific handler methods remain largely the same as in the original code
    def handle_roll_number_query(self, query):
        name = self.extract_name(query)
        if name:
            results = self.safe_database_query("SELECT RegisterNumber FROM Students WHERE FullName LIKE ?", (f"%{name}%",))
            if results and results[0]:
                return f"The roll number of {name} is {results[0][0]}."
            else:
                return f"No records found for {name}."
        return "Please specify the student's name."

    def handle_cgpa_query(self, query):
        name = self.extract_name(query)
        if name:
            results = self.safe_database_query("SELECT CGPA FROM Students WHERE FullName LIKE ?", (f"%{name}%",))
            if results and results[0]:
                return f"The CGPA of {name} is {results[0][0]}."
            else:
                return f"No records found for {name}."
        return "Please specify the student's name."

    def handle_batch_query(self, query):
        batch_year = self.extract_year(query)
        if batch_year:
            results = self.safe_database_query("SELECT FullName FROM Students WHERE BatchYear = ?", (batch_year,))
            if results:
                student_names = ", ".join([row[0] for row in results])
                return f"Students in the {batch_year} batch: {student_names}."
            else:
                return f"No records found for the {batch_year} batch."
        return "Please specify a batch year."

    def handle_certifications_query(self, query):
        name = self.extract_name(query)
        if name:
            results = self.safe_database_query("SELECT Certifications FROM Students WHERE FullName LIKE ?", (f"%{name}%",))
            if results and results[0] and results[0][0]:
                return f"Certifications of {name}: {results[0][0]}."
            else:
                return f"No certifications found for {name}."
        return "Please specify the student's name."

    def handle_skills_query(self, query):
        name = self.extract_name(query)
        if name:
            results = self.safe_database_query("SELECT Skills FROM Students WHERE FullName LIKE ?", (f"%{name}%",))
            if results and results[0] and results[0][0]:
                return f"Skills of {name}: {results[0][0]}."
            else:
                return f"No skills found for {name}."
        return "Please specify the student's name."

    def handle_projects_query(self, query):
        name = self.extract_name(query)
        if name:
            results = self.safe_database_query("SELECT `List of Projects` FROM Students WHERE FullName LIKE ?", (f"%{name}%",))
            if results and results[0] and results[0][0]:
                return f"Projects of {name}: {results[0][0]}."
            else:
                return f"No projects found for {name}."
        return "Please specify the student's name."

    def handle_address_query(self, query):
        name = self.extract_name(query)
        if name:
            results = self.safe_database_query("SELECT Address FROM Students WHERE FullName LIKE ?", (f"%{name}%",))
            if results and results[0]:
                return f"The address of {name} is {results[0][0]}."
            else:
                return f"No address found for {name}."
        return "Please specify the student's name."

    def handle_attendance_query(self, query):
        name = self.extract_name(query)
        if name:
            results = self.safe_database_query("SELECT Attendance FROM Students WHERE FullName LIKE ?", (f"%{name}%",))
            if results and results[0]:
                return f"The attendance of {name} is {results[0][0]}."
            else:
                return f"No attendance records found for {name}."
        return "Please specify the student's name."

    def handle_department_query(self, query):
        name = self.extract_name(query)
        if name:
            results = self.safe_database_query("SELECT Department FROM Students WHERE FullName LIKE ?", (f"%{name}%",))
            if results and results[0]:
                return f"{name} is in the {results[0][0]} department."
            else:
                return f"No department information found for {name}."
        return "Please specify the student's name."

    def handle_dob_query(self, query):
        name = self.extract_name(query)
        if name:
            results = self.safe_database_query("SELECT DateOfBirth FROM Students WHERE FullName LIKE ?", (f"%{name}%",))
            if results and results[0]:
                return f"The date of birth of {name} is {results[0][0]}."
            else:
                return f"No birthdate found for {name}."
        return "Please specify the student's name."

    def close_connection(self):
        """Properly close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed.")

def main():
    # Database connection
    db_path = 'student_database.db'
    
    try:
        connection = sqlite3.connect(db_path)
        
        # Instantiate the chatbot
        chatbot = MiniNLPChatbot(connection)

        # Test example queries
        test_queries = [
            "What is the roll number of Prasad?",
            "What is the CGPA of Prasad?",
            "Who are the students in the 2024 batch?",
            "What are the certifications of Prasad?",
            "What are the skills of Prasad?",
            "List the projects of Prasad.",
            "Where does Prasad live?",
            "What is the attendance of Prasad?",
            "What department is Prasad in?",
            "What is the date of birth of Prasad?"
        ]

        for query in test_queries:
            print(f"Query: {query}")
            print(f"Response: {chatbot.process_query(query)}")
            print()

        # Close the connection
        chatbot.close_connection()

    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()