from typing import Dict, Any, List, Optional, Type
from pydantic import BaseModel
import json
import yaml
from ..providers.base import ProviderBase
from ..models.dependencies import FormDependencies

class FormTools:
    """
    Tools for form processing with intelligent data extraction.
    Responsible for extracting data from messages, calculating progress,
    and generating questions.
    """

    def __init__(self, provider: ProviderBase, verbose: bool = False):
        """
        Initialize form tools.

        Args:
            provider: LLM provider for API access
            verbose: Enable verbose logging
        """
        self.provider = provider
        self.verbose = verbose

    async def get_form_schema(self, form_class: Type[BaseModel]) -> Dict[str, Any]:
        """
        Get JSON schema for form.

        Args:
            form_class: Form class

        Returns:
            JSON schema
        """
        return form_class.model_json_schema()

    async def extract_data_from_message(
        self,
        message: str,
        form_data: Dict[str, Any],
        form_class: Type[BaseModel]
    ) -> Dict[str, Any]:
        """
        Extract structured data from a user message.

        Args:
            message: User message
            form_data: Current form data
            form_class: Form class

        Returns:
            Updated form data
        """
        schema = await self.get_form_schema(form_class)
        properties = schema.get("properties", {})

        # Logging for debugging
        if self.verbose:
            print(f"[FormTools] Extracting data from message: '{message}'")
            print(f"[FormTools] Current form data: {form_data}")
            print(f"[FormTools] Available form fields: {list(properties.keys())}")

        # Простое решение для коротких ответов - используем первое пустое строковое поле
        if self._looks_like_direct_field_answer(message):
            # Для коротких сообщений просто ищем первое пустое строковое поле
            first_empty_string_field = None
            first_string_field = None

            for field, schema_info in properties.items():
                # Ищем строковые поля
                if schema_info.get("type") == "string":
                    # Запоминаем первое строковое поле в любом случае
                    if first_string_field is None:
                        first_string_field = field

                    # И отдельно запоминаем первое ПУСТОЕ строковое поле
                    if field not in form_data or not form_data[field]:
                        first_empty_string_field = field
                        break

            # Приоритет - пустое поле, если нет - то первое строковое
            target_field = first_empty_string_field or first_string_field

            if target_field:
                if self.verbose:
                    print(f"[FormTools] ✅ Using field '{target_field}' for message: '{message}'")

                updated_data = form_data.copy()
                updated_data[target_field] = message.strip()

                if self.verbose:
                    print(f"[FormTools] ✅ Updated form data: {updated_data}")

                return updated_data

            # Если не нашли строковых полей совсем, продолжаем стандартную обработку

        # Original logic for complex vs simple forms remains unchanged
        # Check if form has nested models
        has_complex_structure = False
        for field_name, field_schema in properties.items():
            if field_schema.get("type") == "object" and "properties" in field_schema:
                has_complex_structure = True
                break

        # Use YAML for complex structures, JSON for simple
        if has_complex_structure:
            # Convert current data to YAML for better structure representation
            current_yaml = yaml.dump(form_data, sort_keys=False, default_flow_style=False)

            system_prompt = f"""
            Extract structured data from the user message to update a form with complex nested structure.

            CURRENT FORM DATA (YAML):
            ```yaml
            {current_yaml}
            ```

            FORM SCHEMA:
            ```json
            {json.dumps(properties, indent=2)}
            ```

            INSTRUCTIONS:
            1. Extract all relevant information from the user message
            2. Return ONLY the updated form data in YAML format
            3. Preserve existing values for fields not mentioned
            4. For arrays/lists, append new values instead of replacing
            5. Maintain the proper structure for nested objects
            6. For nested arrays of objects (like variants, locations, shipping_options),
               ensure each object has all required fields properly formatted
            7. Do not use references or aliases in the YAML output

            Example of proper array of objects format:
            ```yaml
            variants:
              - name: "Variant 1"
                sku: "V1"
                attributes:
                  color: "red"
              - name: "Variant 2"
                sku: "V2"
                attributes:
                  color: "blue"
            ```

            Return ONLY the YAML representation of the updated form data.
            """

            try:
                result = await self.provider.invoke(
                    system=system_prompt,
                    user=message,
                    temperature=0.1
                )

                yaml_result = result.choices[0].message.content.strip()
                updated_data = yaml.safe_load(yaml_result)

                if not isinstance(updated_data, dict):
                    if self.verbose:
                        print(f"Invalid result format: {yaml_result}")
                    return form_data

                # Recursive merge with special handling for lists
                updated_form_data = self._recursive_merge(form_data.copy(), updated_data)
                return updated_form_data

            except Exception as e:
                if self.verbose:
                    print(f"Error extracting data: {e}")
                return form_data
        else:
            # Use JSON for simple forms
            system_prompt = f"""
            Extract structured data from the user message to update a form.

            CURRENT FORM DATA:
            ```json
            {json.dumps(form_data, indent=2)}
            ```

            FORM SCHEMA:
            ```json
            {json.dumps(properties, indent=2)}
            ```

            INSTRUCTIONS:
            1. Extract all relevant information from the user message
            2. Return a JSON object with the updated form data
            3. Only include fields that should be updated

            Return ONLY a JSON object with the updated fields.
            """

            try:
                result = await self.provider.invoke(
                    system=system_prompt,
                    user=message,
                    temperature=0.1,
                    response_format={"type": "json_object"}
                )

                content = result.choices[0].message.content
                if isinstance(content, str):
                    updated_fields = json.loads(content)
                else:
                    updated_fields = content

                # Update only the fields that were extracted
                updated_form_data = form_data.copy()
                for key, value in updated_fields.items():
                    if key in form_data and isinstance(form_data[key], list) and isinstance(value, list):
                        # For lists, combine values but avoid set() for potentially unhashable elements
                        for item in value:
                            if item not in updated_form_data[key]:
                                updated_form_data[key].append(item)
                    else:
                        updated_form_data[key] = value

                return updated_form_data

            except Exception as e:
                if self.verbose:
                    print(f"Error extracting data: {e}")
                return form_data

    def _recursive_merge(self, target: Dict[str, Any], source: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively merge source dict into target dict.

        Args:
            target: Target dict to update
            source: Source dict with new values

        Returns:
            Merged dictionary
        """
        for key, value in source.items():
            if key in target:
                if isinstance(value, dict) and isinstance(target[key], dict):
                    # Recursively merge nested dicts
                    self._recursive_merge(target[key], value)
                elif isinstance(value, list) and isinstance(target[key], list):
                    # For lists, need special handling based on content type

                    # If list contains dictionaries (objects), merge by unique identifiers if possible
                    if value and isinstance(value[0], dict) and target[key] and isinstance(target[key][0], dict):
                        self._merge_object_lists(target[key], value)
                    else:
                        # For primitive lists, just append items that don't exist yet
                        for item in value:
                            if item not in target[key]:
                                target[key].append(item)
                else:
                    # Update value
                    target[key] = value
            else:
                # Add new key
                target[key] = value

        return target

    def _merge_object_lists(self, target_list: List[Dict[str, Any]], source_list: List[Dict[str, Any]]):
        """
        Merge lists of objects (dictionaries) intelligently.

        Args:
            target_list: Target list to update
            source_list: Source list with new dictionaries
        """

        for source_item in source_list:
            if source_item not in target_list:
                target_list.append(source_item)

    async def calculate_progress(
        self,
        form_data: Dict[str, Any],
        form_class: Type[BaseModel]
    ) -> int:
        """
        Calculate form completion progress.

        Args:
            form_data: Current form data
            form_class: Form class

        Returns:
            Progress percentage (0-100)
        """
        schema = await self.get_form_schema(form_class)

        system_prompt = f"""
        Calculate the completion percentage of a form.

        FORM DATA:
        ```json
        {json.dumps(form_data, indent=2)}
        ```

        FORM SCHEMA:
        ```json
        {json.dumps(schema.get("properties", {}), indent=2)}
        ```

        INSTRUCTIONS:
        1. Analyze how complete each field is
        2. Empty strings, empty lists, and null values are considered unfilled
        3. For fields with good quality content, assign higher completion
        4. Calculate an overall percentage from 0-100

        Return ONLY a number between 0 and 100 representing the completion percentage.
        """

        try:
            result = await self.provider.invoke(
                system=system_prompt,
                user="",
                temperature=0.1
            )

            # Extract progress value
            progress_text = result.choices[0].message.content.strip()
            import re
            progress_match = re.search(r'\d+', progress_text)

            if progress_match:
                progress = int(progress_match.group())
                return max(0, min(100, progress))

            # Fallback to heuristic calculation
            return self._calculate_progress_heuristic(form_data, schema)

        except Exception as e:
            if self.verbose:
                print(f"Error calculating progress: {e}")
            return self._calculate_progress_heuristic(form_data, schema)

    def _calculate_progress_heuristic(self, form_data: Dict[str, Any], schema: Dict[str, Any]) -> int:
        """
        Calculate progress using a simple heuristic.

        Args:
            form_data: Current form data
            schema: Form schema

        Returns:
            Progress percentage (0-100)
        """
        properties = schema.get("properties", {})
        total_fields = 0
        filled_fields = 0

        for field_name, field_schema in properties.items():
            if field_name in form_data:
                total_fields += 1
                value = form_data[field_name]

                # Check if field is filled based on type
                if isinstance(value, str) and value.strip():
                    filled_fields += 1
                elif isinstance(value, list) and value:
                    filled_fields += 1
                elif isinstance(value, dict) and value:
                    # For nested objects, calculate recursively
                    nested_props = field_schema.get("properties", {})
                    if nested_props:
                        nested_total = len(nested_props)
                        nested_filled = 0

                        for nested_field, nested_schema in nested_props.items():
                            if nested_field in value and value[nested_field]:
                                nested_filled += 1

                        filled_fields += (nested_filled / nested_total)
                    else:
                        filled_fields += 1
                elif value is not None and not isinstance(value, (str, list, dict)):
                    filled_fields += 1
            else:
                total_fields += 1

        if total_fields == 0:
            return 100

        return min(100, int((filled_fields / total_fields) * 100))

    async def generate_next_question(
        self,
        form_data: Dict[str, Any],
        form_class: Type[BaseModel],
        progress: int,
        message_history: List[Dict[str, Any]],
        user_language: str = "en"
    ) -> str:
        """
        Generate the next question based on form state.

        Args:
            form_data: Current form data
            form_class: Form class
            progress: Current progress percentage
            message_history: Message history
            user_language: User's language

        Returns:
            Next question to ask
        """
        # If form is complete, return completion message
        if progress >= 100:
            if user_language.lower().startswith("ru"):
                return "Форма заполнена! Хотите получить анализ данных?"
            else:
                return "The form is complete! Would you like to analyze the data?"

        # Get form schema
        schema = await self.get_form_schema(form_class)

        # Prepare recent message history
        recent_messages = message_history[-5:] if message_history else []
        formatted_history = "\n".join([
            f"{msg.get('role', 'unknown')}: {msg.get('content', '')}"
            for msg in recent_messages
        ])

        system_prompt = f"""
        Generate the next question to ask the user filling out a form.

        FORM DATA:
        ```json
        {json.dumps(form_data, indent=2)}
        ```

        FORM SCHEMA:
        ```json
        {json.dumps(schema.get("properties", {}), indent=2)}
        ```

        RECENT CONVERSATION:
        {formatted_history}

        INSTRUCTIONS:
        1. Focus on fields that are still empty or incomplete
        2. Ask one clear question at a time
        3. Be conversational and natural
        4. Use the user's language: {user_language}
        5. Don't repeat questions already answered

        Current completion progress: {progress}%

        Return ONLY the next question to ask the user.
        """

        try:
            result = await self.provider.invoke(
                system=system_prompt,
                user="",
                temperature=0.7
            )

            return result.choices[0].message.content.strip()

        except Exception as e:
            if self.verbose:
                print(f"Error generating question: {e}")

            # Fallback question
            if user_language.lower().startswith("ru"):
                return "Пожалуйста, расскажите больше о вашем проекте."
            else:
                return "Please tell me more about your project."

    async def detect_user_language(self, message: str) -> str:
        """
        Detect user language from message.

        Args:
            message: User message

        Returns:
            Language code (e.g., 'en', 'ru')
        """
        system_prompt = """
        Detect the language of the user's message.
        Return ONLY the two-letter language code (e.g., 'en', 'ru', 'es').
        """

        try:
            result = await self.provider.invoke(
                system=system_prompt,
                user=message,
                temperature=0.1
            )

            lang_code = result.choices[0].message.content.strip().lower()

            # Validate language code
            if len(lang_code) > 5:
                return "en"

            return lang_code

        except Exception as e:
            if self.verbose:
                print(f"Error detecting language: {e}")
            return "en"

    def _looks_like_direct_field_answer(self, message: str) -> bool:
        """Check if message appears to be a direct field answer"""
        # Trim and clean the message
        clean_msg = message.strip()
        # Short messages without punctuation likely direct answers
        return len(clean_msg.split()) <= 3 and not any(p in clean_msg for p in ['?', '!', ':', ';', ','])

    def _looks_like_name(self, message: str) -> bool:
        """Check if message appears to be a name"""
        # Trim and clean the message
        clean_msg = message.strip()
        # Names typically 1-3 words without numbers or special characters
        words = clean_msg.split()
        if len(words) > 0 and len(words) <= 3:
            # Check if any word contains digits
            if any(any(c.isdigit() for c in word) for word in words):
                return False
            # Typical name doesn't contain too many special characters
            special_chars = sum(1 for c in clean_msg if not c.isalnum() and not c.isspace())
            return special_chars <= 1
        return False
