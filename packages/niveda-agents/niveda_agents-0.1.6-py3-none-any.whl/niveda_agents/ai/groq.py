import os
import logging
from groq import Groq
from niveda_agents.utils.logger import setup_logger

# Initialize logger
logger = setup_logger()


class GroqClient:
    def __init__(self, api_key=None):
        """Initialize the Groq API client using the official library."""
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            logger.error(
                "❌ GROQ_API_KEY is missing. Provide it via an environment variable or argument.")
            raise ValueError("GROQ_API_KEY is not set.")

        self.client = Groq(api_key=self.api_key)
        logger.info("✅ GroqClient Initialized with official SDK")

    def generate_text(self, prompt, model="llama-3.3-70b-versatile"):
        """Generate text using Groq's AI models based only on the given prompt."""
        logger.info(
            f"📝 Generating text using {model} | Prompt: {prompt[:50]}...")

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model
            )
            result = chat_completion.choices[0].message.content
            logger.info(f"✅ Groq Response: {result[:100]}...")
            return result
        except Exception as e:
            logger.error(f"❌ Error in Groq API: {str(e)}")
            return f"Error: {str(e)}"

    def generate_text_with_query(self, prompt, query, model="llama-3.3-70b-versatile"):
        """Generate text using Groq's AI models considering both prompt and user query."""
        logger.info(
            f"📝 Generating response using {model} | Prompt: {prompt[:50]}... | Query: {query[:50]}...")

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Use the following prompt as context."},
                    {"role": "user", "content": prompt},
                    {"role": "user", "content": query}
                ],
                model=model
            )
            result = chat_completion.choices[0].message.content
            logger.info(f"✅ Groq Response: {result[:100]}...")
            return result
        except Exception as e:
            logger.error(f"❌ Error in Groq API: {str(e)}")
            return f"Error: {str(e)}"
