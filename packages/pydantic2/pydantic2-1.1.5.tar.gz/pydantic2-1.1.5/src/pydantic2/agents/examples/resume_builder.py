#!/usr/bin/env python
"""
Resume builder example that demonstrates schema_to_model functionality.
"""

import os
import asyncio
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
import json

# Import from our library
from pydantic2.agents import FormProcessor, BaseAnalyticsTools, OpenRouterProvider
from pydantic2.agents import schema_to_model

# Get API key from environment
API_KEY = os.environ.get("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("Please set the OPENROUTER_API_KEY environment variable")

# Define the resume schema (instead of direct Pydantic models)
resume_schema = {
    "title": "ResumeForm",
    "type": "object",
    "properties": {
        "personal_info": {
            "type": "object",
            "title": "PersonalInfo",
            "description": "Personal information",
            "properties": {
                "full_name": {
                    "type": "string",
                    "description": "Full name"
                },
                "email": {
                    "type": "string",
                    "description": "Email address"
                },
                "phone": {
                    "type": "string",
                    "description": "Phone number"
                },
                "location": {
                    "type": "string",
                    "description": "City, State/Province, Country"
                },
                "linkedin": {
                    "type": "string",
                    "description": "LinkedIn profile URL"
                },
                "portfolio": {
                    "type": "string",
                    "description": "Portfolio or personal website URL"
                }
            }
        },
        "professional_summary": {
            "type": "string",
            "description": "Brief professional summary or objective statement"
        },
        "skills": {
            "type": "array",
            "description": "List of professional skills",
            "items": {
                "type": "string",
                "description": "Professional skill"
            }
        },
        "work_experience": {
            "type": "array",
            "description": "Professional work experience",
            "items": {
                "type": "object",
                "properties": {
                    "company": {
                        "type": "string",
                        "description": "Company name"
                    },
                    "position": {
                        "type": "string",
                        "description": "Job title"
                    },
                    "location": {
                        "type": "string",
                        "description": "Job location"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Start date (MM/YYYY)"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "End date (MM/YYYY or 'Present')"
                    },
                    "achievements": {
                        "type": "array",
                        "description": "Key achievements and responsibilities",
                        "items": {
                            "type": "string"
                        }
                    }
                }
            }
        },
        "education": {
            "type": "array",
            "description": "Educational background",
            "items": {
                "type": "object",
                "properties": {
                    "institution": {
                        "type": "string",
                        "description": "Institution name"
                    },
                    "degree": {
                        "type": "string",
                        "description": "Degree obtained"
                    },
                    "field_of_study": {
                        "type": "string",
                        "description": "Field of study"
                    },
                    "graduation_date": {
                        "type": "string",
                        "description": "Graduation date (MM/YYYY)"
                    },
                    "gpa": {
                        "type": "string",
                        "description": "GPA or academic achievements"
                    },
                    "activities": {
                        "type": "array",
                        "description": "Relevant activities and societies",
                        "items": {
                            "type": "string"
                        }
                    }
                }
            }
        },
        "certifications": {
            "type": "array",
            "description": "Professional certifications",
            "items": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Certification name"
                    },
                    "issuer": {
                        "type": "string",
                        "description": "Issuing organization"
                    },
                    "date": {
                        "type": "string",
                        "description": "Date obtained (MM/YYYY)"
                    },
                    "expires": {
                        "type": "boolean",
                        "description": "Whether the certification expires"
                    },
                    "expiration_date": {
                        "type": "string",
                        "description": "Expiration date if applicable (MM/YYYY)"
                    }
                }
            }
        },
        "languages": {
            "type": "array",
            "description": "Languages spoken",
            "items": {
                "type": "object",
                "properties": {
                    "language": {
                        "type": "string",
                        "description": "Language name"
                    },
                    "proficiency": {
                        "type": "string",
                        "description": "Proficiency level (Basic, Conversational, Fluent, Native)"
                    }
                }
            }
        },
        "references": {
            "type": "array",
            "description": "Professional references",
            "items": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Reference name"
                    },
                    "relationship": {
                        "type": "string",
                        "description": "Professional relationship"
                    },
                    "company": {
                        "type": "string",
                        "description": "Company"
                    },
                    "contact": {
                        "type": "string",
                        "description": "Contact information (email or phone)"
                    }
                }
            }
        }
    }
}

# Convert schema to Pydantic model using schema_to_model utility
ResumeForm = schema_to_model(resume_schema)

# Create analytics class for resume review
class ResumeAnalytics(BaseAnalyticsTools):
    def get_analysis_prompt(self, form_data, form_schema):
        """Customize system prompt for resume analysis."""
        return f"""
        You are a professional resume reviewer. Analyze this resume data and provide feedback.

        RESUME DATA:
        ```json
        {json.dumps(form_data, indent=2)}
        ```

        Generate a comprehensive resume analysis with these components:
        1. Overall strength assessment (scale 1-10)
        2. Key strengths identified
        3. Areas for improvement
        4. ATS compatibility assessment
        5. Content gap analysis
        6. Industry-specific recommendations

        Return your analysis as a structured JSON object with these fields.
        """

    def get_insights_prompt(self, form_data, analysis):
        """Customize system prompt for resume insights."""
        return f"""
        Generate specific recommendations to improve this resume based on the analysis.

        RESUME DATA:
        ```json
        {json.dumps(form_data, indent=2)}
        ```

        ANALYSIS:
        ```json
        {json.dumps(analysis, indent=2)}
        ```

        Generate 5-7 specific, actionable recommendations to improve this resume, covering:
        - Content enhancement
        - Format optimization
        - Keyword optimization for ATS
        - Achievement highlighting
        - Industry-specific best practices

        Each recommendation should be specific and actionable.
        """

    def get_default_analysis_result(self, form_data, error_message):
        """Custom default analysis for resume."""
        return {
            "error": error_message,
            "overall_strength": 0,
            "key_strengths": [],
            "areas_for_improvement": [],
            "ats_compatibility": "Unable to assess",
            "content_gaps": [],
            "industry_recommendations": []
        }

async def main():
    print("Resume schema converted to Pydantic model:", ResumeForm.__name__)

    # Create provider
    provider = OpenRouterProvider(
        api_key=API_KEY,
        model_name="openai/gpt-4o-mini"
    )

    # Create analytics
    analytics = ResumeAnalytics(provider=provider, verbose=True)

    # Create form processor
    processor = FormProcessor(
        form_class=ResumeForm,
        analytics_tools=analytics,
        openrouter_api_key=API_KEY,
        verbose=True
    )

    # Initialize session
    session_id, first_question = await processor.initialize()
    print(f"\nSession: {session_id}")
    print(f"Assistant: {first_question}")

    # Simulate a conversation to build a resume
    messages = [
        "My name is Alex Johnson and I'm a software engineer. My email is alex.johnson@email.com " +
        "and my phone number is (555) 123-4567. I live in Seattle, WA. " +
        "My LinkedIn is linkedin.com/in/alexjohnson and my portfolio is alexjohnson.dev",

        "I'm a full-stack developer with 7 years of experience building scalable web applications. " +
        "I specialize in React, Node.js, and cloud architecture with a focus on performance optimization " +
        "and developer experience.",

        "My skills include JavaScript (Expert, 7 years), React (Advanced, 5 years), Node.js (Advanced, 5 years), " +
        "Python (Intermediate, 3 years), AWS (Advanced, 4 years), and Docker (Intermediate, 3 years).",

        "I worked at TechCorp as a Senior Software Engineer in Seattle from 07/2019 to Present. " +
        "My achievements include: Redesigned the authentication system reducing login times by 40%, " +
        "Led a team of 5 developers to rebuild the customer dashboard improving user engagement by 25%, " +
        "and Implemented CI/CD pipeline reducing deployment time from days to hours.",

        "Before that, I was at WebSolutions as a Software Developer in Portland from 06/2016 to 06/2019. " +
        "I built RESTful APIs serving 2M+ daily requests, optimized database queries reducing load times by 30%, " +
        "and mentored junior developers through pair programming and code reviews.",

        "I have a Bachelor of Science in Computer Science from University of Washington, graduated 05/2016 " +
        "with a 3.8 GPA. I was part of the Coding Club and Hackathon Team.",

        "I'm certified as an AWS Solutions Architect (title: 'AWS Solutions Architect', issuer: Amazon, date: 05/2020, expires: true, expiration_date: 05/2023) and as a " +
        "React Certified Developer (title: 'React Certified Developer', issuer: Meta, date: 03/2021, expires: false, no expiration date).",

        "I speak English (Native) and Spanish (Conversational).",

        "For references, you can contact Sarah Miller, my former manager at TechCorp (name: 'Sarah Miller', relationship: 'Former Manager', company: 'TechCorp', contact: 'sarah.miller@techcorp.com'), " +
        "and David Wong, Lead Developer at WebSolutions (name: 'David Wong', relationship: 'Lead Developer', company: 'WebSolutions', contact: 'david.wong@websolutions.com').",

        "Can you review my resume and suggest improvements?"
    ]

    for message in messages:
        print(f"\nUser: {message}")
        result = await processor.process_message(message, session_id)
        print(f"Assistant: {result.message}")
        print(f"Progress: {result.progress}%")

    # Get final form state
    state = await processor.get_form_state(session_id)
    print("\nFinal resume data:")
    print(json.dumps(state.form, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
