import aiohttp
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from .const import CONF_API_KEY, CONF_ORG_ID


class OpenAIClient:
    """Client for OpenAI API to fetch token usage."""

    BASE_URL = "https://api.openai.com/v1"

    def __init__(self, api_key: str, org_id: Optional[str] = None):
        self.api_key = api_key
        self.org_id = org_id
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        if self.org_id:
            self.headers["OpenAI-Organization"] = self.org_id

    async def fetch_usage(self) -> Dict[str, Any]:
        """Fetch aggregated token usage for the last 24 hours."""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=1)

        params = {
            "date_start": start_date.strftime("%Y-%m-%d"),
            "date_end": end_date.strftime("%Y-%m-%d"),
            "group_by": "model",  # Group by model for breakdowns
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.BASE_URL}/organization/usage/completions",
                headers=self.headers,
                params=params,
            ) as response:
                if response.status != 200:
                    raise aiohttp.ClientError(
                        f"API error: {response.status} - {await response.text()}"
                    )

                data = await response.json()
                # Aggregate totals
                total_input = sum(
                    item.get("n_context_tokens_total", 0)
                    for item in data.get("data", [])
                )
                total_output = sum(
                    item.get("n_generated_tokens_total", 0)
                    for item in data.get("data", [])
                )

                return {
                    "input_tokens": total_input,
                    "output_tokens": total_output,
                    "total_tokens": total_input + total_output,
                    "last_updated": datetime.utcnow().isoformat(),
                    "details": data.get("data", []),  # For attributes
                }
