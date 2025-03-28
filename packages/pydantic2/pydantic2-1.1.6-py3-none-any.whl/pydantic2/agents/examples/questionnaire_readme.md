# Questionnaire Example with Session Management

This example demonstrates a more complex form processing scenario with session management capabilities. It's designed for situations where a user might need to fill out a form across multiple sessions, such as long surveys or applications.

## Key Features

1. **Session Management**: Create new sessions or continue existing ones using a session ID
2. **Multi-part Form Structure**: The form has multiple sections with nested models
3. **Progress Tracking**: Shows completion percentage as the user progresses
4. **Session Persistence**: Automatically saves the session state to a local JSON file
5. **Analytics**: Provides insights based on the completed form data
6. **Type-safe Enums**: Uses Literal types to create enum-like fields

## Form Structure

The questionnaire consists of:

1. **Personal Information**: Basic contact details
2. **Professional Information**: Employment status, education, etc.
3. **Product Usage**: How the person uses the product and satisfaction level
4. **Feedback**: Suggestions and additional comments

## Running the Example

```bash
python -m src.pydantic2.agents17.examples.questionnaire
```

## Usage Flow

1. When started, you'll see a menu:
   ```
   ==================================================
     SURVEY QUESTIONNAIRE SYSTEM
   ==================================================
   1. Start a new survey
   2. Continue existing survey
   ==================================================
   ```

2. If you select option 1, a new session ID will be generated. Make note of this ID if you want to continue the session later.

3. If you select option 2, you'll be prompted to enter a previously saved session ID.

4. The assistant will guide you through filling out the form, asking questions to gather the required information.

5. At any point, you can type 'exit' to quit. Your session will be saved automatically.

6. When the form is complete, the system will display analytics and insights based on your responses.

## Session Files

Session state is saved to JSON files with the naming pattern `session_[UUID].json`. Each file contains:

- Timestamp of the last update
- Current form state
- Conversation history

## Example Use Cases

- Customer satisfaction surveys
- Job applications
- Product registration forms
- Medical intake forms
- Research questionnaires

This example demonstrates how the Pydantic AI Form Processor can handle complex real-world scenarios requiring session persistence and multi-stage data collection.
