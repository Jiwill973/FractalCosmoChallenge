from astroquery.mast import Catalogs, Observations
from astroquery.gaia import Gaia
from astropy.coordinates import SkyCoord
import astropy.units as u
import pandas as pd
from datetime import datetime

# Coordonnées d'Andromède (modifiables)
coord = SkyCoord(ra=266.4168*u.deg, dec=-29.0078*u.deg, frame='icrs')  # Centre galactique
radius = 0.5 * u.deg  # Augmente à 0.5 degré pour tester

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Hubble avec pagination
print("Interrogation Hubble avec pagination...")
pagesize = 10000  # Résultats par page
page = 1
tous_les_resultats = []
while True:
    hsc = Catalogs.query_region(coord, radius=radius, catalog="HSC", pagesize=pagesize, page=page)
    if len(hsc) == 0:
        break
    tous_les_resultats.extend(hsc)
    page += 1
hsc_df = pd.DataFrame(tous_les_resultats)
hsc_df.to_csv(f"../data/cosmologie/hubble_{timestamp}.csv", index=False)
print("Hubble ok ! ({len(hsc)} objets trouvés)")

# Gaia DR3
print("Interrogation Gaia...")
Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"
gaia_job = Gaia.cone_search_async(
    coordinate=coord,
    radius=radius
)
gaia_results = gaia_job.get_results()
gaia = gaia_results.to_pandas()
gaia.to_csv(f"../data/cosmologie/gaia_{timestamp}.csv", index=False)
print(f"Gaia ok ! ({len(gaia)} objets trouvés)")

# TESS
print("Interrogation TESS...")
tess = Catalogs.query_region(coord, radius=radius, catalog="TIC")
tess_df = tess.to_pandas()
tess_df.to_csv(f"../data/cosmologie/tess_{timestamp}.csv", index=False)
print("TESS ok !")

# Pan-STARRS
print("Interrogation Pan-STARRS...")
panstarrs = Catalogs.query_region(coord, radius=radius, catalog="Panstarrs")
panstarrs_df = panstarrs.to_pandas()
panstarrs_df.to_csv(f"../data/cosmologie/panstarrs_{timestamp}.csv", index=False)
print("Pan-STARRS ok !")

# JWST : Vérification sans rayon
print("Interrogation JWST (toutes observations)...")
jwst_obs = Observations.query_criteria(obs_collection="JWST")
jwst_df = jwst_obs.to_pandas()
print(f"JWST : {len(jwst_df)} observations totales trouvées")

# JWST via MAST
print("Interrogation JWST...")
jwst_obs = Observations.query_criteria(
    coordinates=coord,
    radius=radius,
    obs_collection="JWST"
)
if len(jwst_obs) > 0:
    jwst_df = jwst_obs.to_pandas()
    jwst_df.to_csv(f"../data/cosmologie/jwst_{timestamp}.csv", index=False)
    print("JWST ok !")
else:
    print("JWST : pas d'observations trouvées.")

print("Collecte multi-catalogues terminée.")
