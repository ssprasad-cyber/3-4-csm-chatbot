import spacy
import sqlite3
import pandas as pd

# Load Spacy model
# Use the correct model name, e.g., 'en_core_web_sm'
nlp = spacy.load("en_core_web_sm")

entities = {
    "name": ["what is the name", "who is", "tell me the name"],
    "roll_number": ["roll number", "register number", "id"],
}

# Function to populate SQLite database
def create_student_db_from_excel(excel_file, db_name="student_database.db"):
    df = pd.read_excel(excel_file)
    # Rename columns if necessary to match SQLite schema
    df.rename(columns={
        "Full Name": "FullName",
        "Register Number": "RegisterNumber",
        "Date of Birth": "DateOfBirth",
        "Phone Number": "PhoneNumber",
        "Parent's Name": "ParentsName",
        "Parent's Contact": "ParentsContact",
        "Blood Group": "BloodGroup",
        "Batch Year": "BatchYear",
        "1st Sem SGPA": "Sem1_SGPA",
        "2nd Sem SGPA": "Sem2_SGPA",
        "3rd Sem SGPA": "Sem3_SGPA",
        "4th Sem SGPA": "Sem4_SGPA",
        "Number of Projects Done": "ProjectsDone",
        "Are you in any clubs?": "ClubMembership",
        "If yes, please enter club name": "ClubName",
        "Certifications or Achievements": "Certifications",
        "LinkedIn Profile": "LinkedInProfile",
        "GitHub Profile": "GitHubProfile"
    }, inplace=True)

    conn = sqlite3.connect(db_name)
    df.to_sql('Students', conn, if_exists='replace', index=False)
    conn.close()
    print("Database created and populated successfully!")


# NLP Function to extract information
def process_query(query, db_name="student_database.db"):
    # Analyze query using Spacy
    doc = nlp(query.lower())
    tokens = [token.text for token in doc]

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Example: Identify queries based on tokens
    if "name" in query and "roll number" in query:
        roll_number = [int(token) for token in tokens if token.isdigit()]
        if roll_number:
            roll_number = roll_number[0]
            query = f"SELECT FullName FROM Students WHERE RegisterNumber={roll_number}"
            cursor.execute(query)
            result = cursor.fetchone()
            conn.close()
            return f"The name of roll number {roll_number} is {result[0]}" if result else "Roll number not found."

    # Add more query handlers here (e.g., CGPA, skills, etc.)

    conn.close()
    return "I couldn't understand your query."

# Main program
if __name__ == "__main__":
    # Provide the path to the Excel file
    excel_file = "./students_data.xlsx"
    create_student_db_from_excel(excel_file)

    # Test the NLP-based query system
    while True:
        user_query = input("Ask a question: ")
        if user_query.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        response = process_query(user_query)
        print(response)
