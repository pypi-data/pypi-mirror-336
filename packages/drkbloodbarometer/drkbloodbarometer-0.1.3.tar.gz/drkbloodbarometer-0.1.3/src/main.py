import logging
import json
from datetime import datetime as dt

import requests
from bs4 import BeautifulSoup

from const import bloodtypes, ratings, states

logger = logging.getLogger()

class DRKBloodBarometer:
    """A library to extract the blood barometer data from the states DRK blood donation website."""
    def __init__(self, state):
        self.state = state
        self.base_url = None
        self.raw_data = ""
        self.bloodlevels = {}
        self.lastChange = ""
        self._get_data(state)

    def _get_data(self, state):
        """Main method """
        self._get_base_url(state)
        if not self.base_url:
            return
        self._get_page()
        self._parse_data()

    def _get_base_url(self, state):
        """Get the right url for a given state, print an error if none ist available."""
        if "url" in states[state]:
            self.base_url = states[state]["url"]
        else:
            logger.error(f"State {state} is currently not support due to unavailablity of raw data.")

    def _get_page(self):
        """Fetch the HTML page and store it."""
        if not self.base_url:
            return
        try:
            response = requests.get(self.base_url, timeout=5)
            response.raise_for_status()
            self.raw_data = response.text
        except requests.exceptions.RequestException as e:
            self.raw_data = ""
            logger.error(f"Error fetching page {self.base_url}: {e}")

    @staticmethod
    def _get_rating(level):
        """Get the right level description for a given level."""
        return max(
            (name for name, threshold in ratings.items() if level >= threshold),
            default="Kritisch",
        )

    def _parse_data(self):
        """Parse the raw HTML page, extract the JSON data and parse the blood level data."""
        if not self.raw_data:
            logger.error("No raw data to parse.")
            return
    
        try:
            soup = BeautifulSoup(self.raw_data, "html.parser")
            script = soup.find("script", attrs={"data-drupal-selector": True})
            
            if not script:
                logger.error("No script tag with 'data-drupal-selector' found.")
                return

            data = json.loads(script.text)

            if "blutgruppen" not in data:
                logger.error("Expected key 'blutgruppen' not found in JSON data.")
                return

            for k, v in bloodtypes.items():
                self.bloodlevels[v] = {}

                try:
                    if "default" in data["blutgruppen"]:
                        self.bloodlevels[v]["level"] = (
                            int(data["blutgruppen"]["default"][f"blood_barometer_{k}"]) * 12
                        ) + 11
                    else:
                        self.bloodlevels[v]["level"] = (
                            float(data["blutgruppen"][f"blood_barometer_{k}"]) * 0.60
                        )

                    self.bloodlevels[v]["warning"] = (
                        self.bloodlevels[v]["level"] < ratings.get("Bedrohlich", 0)
                    )
                    self.bloodlevels[v]["rating"] = self._get_rating(
                        self.bloodlevels[v]["level"]
                    )

                except (KeyError, ValueError, TypeError) as e:
                    logger.error(f"Error processing blood level data for {v}: {e}")
                    self.bloodlevels[v] = {"level": None, "warning": None, "rating": None}

            try:
                self.lastChange = dt.strptime(
                    data["blutgruppen"]["blood_barometer_changed"], "%Y-%m-%d"
                )
            except (KeyError, ValueError) as e:
                logger.error(f"Error parsing last change date: {e}")
                self.lastChange = None

        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON data: {e}")


if __name__ == "__main__":
    bb = DRKBloodBarometer("Baden-Würtemberg")
    print(bb.bloodlevels)
    print(bb.lastChange)
