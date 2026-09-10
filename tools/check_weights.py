from netCDF4 import Dataset
import numpy as np

old="/leonardo_scratch/fast/ICT26_ESP/ntilinin/INPUT/access-om2/remapping_weights/JRA55/global.1deg/2020.05.30/rmp_jra55_cice_1st_conserve.nc"
new="/leonardo/home/userexternal/ntilinin/COSIMA/access-om2/tools/JRA55_MOM1_conserve.nc"

a,b=Dataset(old),Dataset(new)

sa,da=a["src_address"][:],a["dst_address"][:]
sb,db=b["src_address"][:],b["dst_address"][:]

ia=np.lexsort((da,sa))
ib=np.lexsort((db,sb))

print("sorted src_address exact:", np.array_equal(sa[ia],sb[ib]))
print("sorted dst_address exact:", np.array_equal(da[ia],db[ib]))

wa=a["remap_matrix"][:,0]
wb=b["remap_matrix"][:,0]

print("weight max abs diff:", np.max(np.abs(wa[ia]-wb[ib])))
print("weight mean abs diff:", np.mean(np.abs(wa[ia]-wb[ib])))

a.close(); b.close()