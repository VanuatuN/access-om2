OLD=/leonardo_scratch/fast/ICT26_ESP/ntilinin/INPUT/access-om2/remapping_weights/JRA55/global.1deg/2020.05.30/rmp_jra55_cice_1st_conserve.nc
NEW=/leonardo/home/userexternal/ntilinin/COSIMA/access-om2/tools/JRA55_MOM1_conserve.nc

ls -lh "$OLD" "$NEW"
ncdump -h "$NEW" | head -80
ncdump -h "$OLD" | head -80