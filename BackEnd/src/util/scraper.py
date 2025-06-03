import json
import requests
from bs4 import BeautifulSoup
from googletrans import Translator, constants

# Website URL
URL = "https://www.fao.org/3/x0490e/x0490e0b.htm"

def scrape_crop_coefficients():
	"""
		Scraping in search of retriving Kc values for 
		specific crops.

		Kc => indicates the water need of a crop based on evapotranspiration
	"""
	response = requests.get(URL)
	soup = BeautifulSoup(response.content, "html.parser")

	kc_table = soup.find("table")

	crop_data = {}

	if not kc_table:
		print("Table not found on the page.")
		return crop_data

	rows = kc_table.find_all("tr")[1:] 

	for row in rows:
		cols = [col.get_text(strip=True) for col in row.find_all("td")]

		# Skip invalid rows
		if len(cols) < 4:
			continue

		crop_name = cols[0].lower()
		try:
			kc_init = float(cols[1])
			kc_mid = float(cols[2])
			kc_end = float(cols[3])

			crop_data[crop_name] = {
				"initial": kc_init,
				"mid": kc_mid,
				"end": kc_end
			}
		except ValueError:
			continue

	return crop_data

# Translate crop name into english word
def translate_to_eng(crop_name: str) -> str:
    translator = Translator()
    translation = translator.translate(crop_name.lower(), src='ro', dest='en')
    return translation.text

# Get crop coeficient
def get_crop_coefficient(crop_name: str) -> float:
	# Open json of scraped data
	with open("src/util/data/crop_coefficients.json", "r", encoding="utf-8") as f:
		CROP_DATA = json.load(f)

	crop = CROP_DATA.get(crop_name.lower())
	if not crop:
		return 1.0  # choose default
	return crop.get("mid", 1.0)  # use only middle values

"""
	Run this block to fetch and update the crop coefficients dataset.
It scrapes the website for updated Kc values for various crops and 
saves them into a local JSON file (crop_coefficients.json).
"""

# if __name__ == "__main__":
# 	crop_coeffs = scrape_crop_coefficients()
# 	with open("src/util/data/crop_coefficients.json", "w", encoding="utf-8") as f:
# 		json.dump(crop_coeffs, f, indent=2, ensure_ascii=False)
