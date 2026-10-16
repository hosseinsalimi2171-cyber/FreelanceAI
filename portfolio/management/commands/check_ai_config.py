import os

from django.conf import settings
from django.core.management.base import BaseCommand

from portfolio.services.openai_client import OpenAIConfigurationError


class Command(BaseCommand):
    help = "Check AI configuration without sending an API request."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("FreelanceAI AI Configuration"))
        self.stdout.write(f"Configured model label: {settings.OPENAI_MODEL}")

        api_key_present = bool(
            os.getenv("OPENAI_API_KEY", "").strip()
        )

        self.stdout.write(
            "API key present: "
            + ("Yes" if api_key_present else "No")
        )

        try:
            from openai import OpenAI
            self.stdout.write(
                self.style.SUCCESS("OpenAI Python SDK: installed")
            )
        except ImportError:
            self.stdout.write(
                self.style.ERROR("OpenAI Python SDK: missing")
            )

        if not api_key_present:
            self.stdout.write(
                self.style.WARNING(
                    "Status: waiting for API credentials. "
                    "No network request was made."
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "Status: credentials detected, but not verified. "
                    "No network request was made."
                )
            )
