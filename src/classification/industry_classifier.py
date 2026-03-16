import os
import sqlite3
import json
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class IndustryClassifier:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.industries = {
            "A": "Agricultura, ganadería, silvicultura y pesca",
            "B": "Explotación de minas y canteras",
            "C": "Industrias manufactureras",
            "D": "Suministro de electricidad, gas, vapor",
            "E": "Suministro de agua; alcantarillado",
            "F": "Construcción",
            "G": "Comercio al por mayor y menor",
            "H": "Transporte y almacenamiento",
            "I": "Alojamiento y servicios de comida",
            "J": "Información y comunicaciones",
            "K": "Actividades financieras y de seguros",
            "L": "Actividades inmobiliarias",
            "M": "Actividades profesionales, científicas",
            "N": "Actividades administrativas y de apoyo",
            "O": "Administración pública y defensa",
            "P": "Enseñanza",
            "Q": "Salud humana y asistencia social",
            "R": "Artes, entretenimiento y recreación",
            "S": "Otras actividades de servicios",
            "T": "Actividades de hogares",
            "U": "Actividades de organizaciones extraterritoriales"
        }

    def classify_repository(self, name, description, readme, topics, language):
        prompt = f"""Analyze this GitHub repository and classify it into ONE of the following industry categories based on its potential application or the industry it serves.

REPOSITORY INFORMATION:
- Name: {name}
- Description: {description or 'No description'}
- Primary Language: {language or 'Not specified'}
- Topics: {topics or 'None'}
- README (first 2000 chars): {readme[:2000] if readme else 'No README'}

INDUSTRY CATEGORIES:
{json.dumps(self.industries, indent=2)}

INSTRUCTIONS:
1. Analyze the repository's purpose, functionality, and potential use cases.
2. Consider what industry would most benefit from or use this software.
3. If it's a general-purpose tool, classify based on the most likely industry application.
4. If truly generic (e.g., "hello world"), use "J" (Information and communication).

Respond in JSON format:
{{
    "industry_code": "X",
    "industry_name": "Full industry name",
    "confidence": "high|medium|low",
    "reasoning": "Brief explanation of why this classification was chosen"
}}
"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini", # Using mini for cost efficiency while maintaining quality
                messages=[
                    {"role": "system", "content": "You are an expert at classifying software projects by industry. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Error classifying {name}: {e}")
            return None

def main():
    db_path = "data/github_peru.db"
    classifier = IndustryClassifier()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get repos that have readme but no industry classification
    cursor.execute("""
        SELECT id, name, description, readme, topics, language 
        FROM repos 
        WHERE (industry_code IS NULL OR industry_code = '') 
        AND (readme IS NOT NULL AND readme != '')
        LIMIT 1000
    """)
    repos = cursor.fetchall()
    
    print(f"Starting classification for {len(repos)} repositories...")
    
    processed = 0
    for repo_id, name, desc, readme, topics, lang in repos:
        result = classifier.classify_repository(name, desc, readme, topics, lang)
        
        if result:
            cursor.execute("""
                UPDATE repos 
                SET industry_code = ?, industry_name = ?, confidence = ?, reasoning = ?
                WHERE id = ?
            """, (
                result.get('industry_code'),
                result.get('industry_name'),
                result.get('confidence'),
                result.get('reasoning'),
                repo_id
            ))
            processed += 1
            
        if processed % 5 == 0:
            conn.commit()
            print(f"Processed {processed}/{len(repos)}...", end='\r')
            
    conn.commit()
    conn.close()
    print(f"\nDone. Classified {processed} repositories.")

if __name__ == "__main__":
    main()
