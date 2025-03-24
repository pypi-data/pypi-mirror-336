import os
from openai import OpenAI


class LLMSummarizer:
    def __init__(self, model="gpt-4"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OpenAI API key not found in environment variables.")
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def create_summary(self, data, context=None, excluded_keys=None, language="english"):
        cleaned_data = self._remove_excluded_keys(data, excluded_keys)
        prompt = self._build_prompt(cleaned_data, context, language)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Take in the data and summarize it  \
                  based on the information with the data object."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

    def _build_prompt(self, data, context=None, language="english"):
        prompt = (
            "You are a specialized data summarizer focused on converting structured data into clear, natural language summaries. "
            "Follow these guidelines:\n"
            "1. Create a coherent narrative from the key-value pairs\n"
            "2. Prioritize important fields and their relationships\n"
            "3. Use natural sentences without bullet points or technical formatting\n"
            "4. Maintain a professional, objective tone\n"
            "5. Keep the summary concise but informative\n\n"
            "6. The summary should be in the " + language + " language\n\n"
            "Structured data to summarize:\n"
        )
        prompt += f"{data}\n"
        if context:
            prompt += "\nAdditional context for specific fields:\n"
            for key, explanation in context.items():
                if key in data:
                    prompt += f"- {key} ({data[key]}): {explanation}\n"
        return prompt

    def _remove_excluded_keys(self, data, excluded_keys):
        if not excluded_keys:
            return data
        return {k: v for k, v in data.items() if k not in excluded_keys}
