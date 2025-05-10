import os
import geopandas as gpd
from shapely.geometry import Point
from dotenv import load_dotenv

WRB_TRANSLATIONS = {
	"AC": ("Acrisol", "Acrisol"),
	"AL": ("Alisol", "Alisol"),
	"AN": ("Andosol", "Andosol"),
	"AR": ("Arenosol", "Arenosol"),
	"CH": ("Chernozem", "Cernoziom"),
	"CM": ("Cambisol", "Cambisol"),
	"CL": ("Calcisol", "Calcisol"),
	"CR": ("Cryosol", "Criosol"),
	"FR": ("Ferralsol", "Feralsol"),
	"FL": ("Fluvisol", "Fluvisol"),
	"GL": ("Gleysol", "Gleysol"),
	"GY": ("Gypsisol", "Gipsisol"),
	"HS": ("Histosol", "Histosol (Turbărie)"),
	"LP": ("Leptosol", "Leptosol"),
	"LV": ("Luvisol", "Luvisol"),
	"PH": ("Phaeozem", "Feozem"),
	"PL": ("Plinthosol", "Plintosol"),
	"PT": ("Podzol", "Podzol"),
	"SC": ("Solonchak", "Solonceac"),
	"SN": ("Solonetz", "Soloneț"),
	"VR": ("Vertisol", "Vertisol"),
}

WRB_QUALIFIERS = {
	"cr": ("Cutanic (clay illuviation)", "Cu orizont argilic (argiluvic)"),
	"lv": ("Luvi (clay accumulation)", "Cu orizont de acumulare a argilei"),
	"cl": ("Clayic", "Argilos"),
	"al": ("Albic", "Albit (orizont deschis, spălat)"),
	"rd": ("Rendzic", "Rendzinic"),
	"um": ("Umbric", "Umbric"),
	"gy": ("Gypsic", "Gipsic"),
	"sl": ("Siltic", "Siltic"),
	"st": ("Stagnic", "Stagnic"),
	"gl": ("Gleyic", "Gleic"),
	"nt": ("Natric", "Natric"),
	"ph": ("Phreatic", "Freatic"),
	"ch": ("Chernozemic", "Cernoziomic"),
	"pt": ("Petric", "Petric"),
	"hi": ("Histic", "Histosolic"),
	"vr": ("Vertic", "Vertic"),
}

# Load environment variables
load_dotenv()

# Load shapefile and attribute DBF
file_SGDBE = os.getenv('SGDBE4_0.SHP')
file_SMU_SGDBE = os.getenv('SMU_SGDBE.DBF')

# Load polygon geometries
soil_gdf = gpd.read_file(file_SGDBE).to_crs(epsg=4326)

# Load soil attributes and merge
smu_attr = gpd.read_file(file_SMU_SGDBE)
soil_gdf = soil_gdf.merge(smu_attr, how="left", left_on="SMU", right_on="SMU")

# Decode soil type returned by the data
def decode_soil_type(code: str, language: str = "ro") -> str:
    if not code or len(code) < 2:
        return "Necunoscut"

    ref_code = code[:2]
    qualifier_code = code[2:] if len(code) > 2 else ""

    ref_en, ref_ro = WRB_TRANSLATIONS.get(ref_code, ("Unknown type", "Tip necunoscut"))
    qual_en, qual_ro = WRB_QUALIFIERS.get(qualifier_code, ("", ""))

    ref_name = ref_ro if language == "ro" else ref_en
    qual_name = qual_ro if language == "ro" else qual_en

    if qual_name:
        return f"{ref_name} - {qual_name}"
    return ref_name


# Function to get soil type from coordinates
def get_soil_info(latitude: float, longitude: float) -> str:
	point = Point(longitude, latitude)  # Correct order: (x, y)
	match = soil_gdf[soil_gdf.geometry.contains(point)]

	if not match.empty:
		row = match.iloc[0]
		soil_type = (
			row.get("WRBFU") or
			row.get("WRBSPE1") or
			row.get("FAO85FU") or
			row.get("FAO90FU") or
			"Necunoscut"
		)
		return decode_soil_type(soil_type)

	return "Necunoscut"
