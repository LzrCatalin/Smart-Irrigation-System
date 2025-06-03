SOIL_BASELINE_TARGET = {
	"Acrisol": 60,
	"Alisol": 60,
	"Andosol": 65,
	"Arenosol": 50,
	"Chernozem": 65,
	"Cambisol": 60,
	"Calcisol": 58,
	"Cryosol": 55, 
	"Ferralsol": 60,        
	"Fluvisol": 63,
	"Gleysol": 70,
	"Gypsisol": 55,
	"Histosol": 75,         
	"Leptosol": 52,         
	"Luvisol": 60, 
	"Phaeozem": 64,
	"Plinthosol": 58,      
	"Podzol": 57,  
	"Solonchak": 56, 
	"Solonetz": 55,
	"Vertisol": 66,         
	"Unknown type": 60,
	"Tip necunoscut": 60    
}

# Fetch specific value
def get_baseline_target_from_soil(soil_name: str) -> int:
	for key in SOIL_BASELINE_TARGET:
	
		if key.lower() in soil_name.lower():
			return SOIL_BASELINE_TARGET[key]
	
	return 60
