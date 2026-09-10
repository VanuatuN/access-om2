#!/usr/bin/env python3

from pathlib import Path

ACCESS_OM_DIR = Path.cwd()
CONFIG = ACCESS_OM_DIR / "control/1deg_jra55_ryf/config.yaml"

BASE = "/leonardo_scratch/fast/ICT26_ESP/ntilinin"
INPUT = f"{BASE}/INPUT/access-om2"
RYF = f"{BASE}/make_ryf"

text = CONFIG.read_text()

replacements = {


    # PBS -> SLURM
    "queue: normal": """scheduler: slurm
#queue: do not set for slurm""",

    "walltime: 3:00:00": "walltime: 03:00:00",

    "jobname: 1deg_jra55_ryf": "jobname: 1deg_jra55_ryf",

    "mem: 1000GB": """mem: 200G
account: ICT26_ESP
partition: dcgp_usr_prod
ncpus: 672
nnodes: 6""",

    

    # Common input
    "input: /g/data/ik11/inputs/access-om2/input_20201102/common_1deg_jra55": f"""input:
  - {INPUT}/remapping_weights/JRA55/global.1deg/2020.05.30/JRA55_MOM1_conserve2nd.nc
  - {INPUT}/remapping_weights/JRA55/global.1deg/2020.05.30/JRA55_MOM1_patch.nc
  - {INPUT}/remapping_weights/JRA55/global.1deg/2020.05.30/rmp_jra55_cice_1st_conserve.nc
  - {INPUT}/remapping_weights/JRA55/global.1deg/2020.05.30/rmp_jra55_cice_2nd_conserve.nc
  - {INPUT}/remapping_weights/JRA55/global.1deg/2020.05.30/rmp_jra55_cice_patch.nc""",

    "- /g/data/ik11/inputs/access-om2/input_20201102/yatm_1deg":
        f"- {INPUT}/remapping_weights/JRA55/global.1deg/2020.05.30/rmp_jrar_to_cict_CONSERV.nc",

    "- /g/data/ik11/inputs/JRA-55/RYF/v1-4":
        f"- {RYF}",

    "      input: /g/data/ik11/inputs/access-om2/input_20201102/mom_1deg": f"""      input:
          - {INPUT}/ocean/grids/mosaic/global.1deg/2020.05.30/grid_spec.nc
          - {INPUT}/ocean/grids/mosaic/global.1deg/2020.05.30/ocean_hgrid.nc
          - {INPUT}/ocean/grids/mosaic/global.1deg/2020.05.30/ocean_mosaic.nc
          - {INPUT}/ocean/grids/bathymetry/global.1deg/2020.10.22/topog.nc
          - {INPUT}/ocean/grids/bathymetry/global.1deg/2020.10.22/ocean_mask.nc
          - {INPUT}/ocean/grids/vertical/global.1deg/2020.10.22/ocean_vgrid.nc
          - {INPUT}/ocean/processor_masks/global.1deg/216.16x15/2020.05.30/ocean_mask_table
          - {INPUT}/ocean/chlorophyll/global.1deg/2020.05.30/chl.nc
          - {INPUT}/ocean/initial_conditions/global.1deg/2020.10.22/ocean_temp_salt.res.nc
          - {INPUT}/ocean/tides/global.1deg/2020.05.30/tideamp.nc
          - {INPUT}/ocean/tides/global.1deg/2020.05.30/roughness_amp.nc
          - {INPUT}/ocean/tides/global.1deg/2020.05.30/roughness_cdbot.nc
          - {INPUT}/ocean/surface_salt_restoring/global.1deg/2020.05.30/salt_sfc_restore.nc""",

    "      input: /g/data/ik11/inputs/access-om2/input_20201102/cice_1deg": f"""      input:
        - {INPUT}/ice/grids/global.1deg/2020.05.30/grid.nc
        - {INPUT}/ice/grids/global.1deg/2020.10.22/kmt.nc
        - {INPUT}/ice/initial_conditions/global.1deg/2020.05.30/i2o.nc
        - {INPUT}/ice/initial_conditions/global.1deg/2020.05.30/o2i.nc
        - {INPUT}/ice/initial_conditions/global.1deg/2020.05.30/u_star.nc
        - {INPUT}/ice/initial_conditions/global.1deg/2020.05.30/monthly_sstsss.nc""",
}

missing = []

for old, new in replacements.items():
    if old not in text:
        missing.append(old)
    text = text.replace(old, new)

if missing:
    print("WARNING: some patterns were not found:")
    for item in missing:
        print(f"  {item}")

CONFIG.write_text(text)
print(f"Updated {CONFIG}")