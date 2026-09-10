#!/bin/bash
#SBATCH --job-name=speedy_weights
##SBATCH --job-name=jra_weights_test
#SBATCH --account=ICT26_ESP
#SBATCH --partition=dcgp_usr_prod
#SBATCH --nodes=1
#SBATCH --ntasks=112
#SBATCH --time=01:00:00
#SBATCH --mem=200G
#SBATCH --output=slurm-speedy-weights-%j.out
#SBATCH --error=slurm-speedy-weights-%j.err

set -euo pipefail

module purge
# module load openmpi
# module load nco
# module load esmf

source /leonardo/prod/spack/03/install/0.19/linux-rhel8-icelake/gcc-8.5.0/anaconda3-2022.05-e7262poa2u2i3rurf3cdt6a5r6dqieik/etc/profile.d/conda.sh
conda activate esmf81
export PATH="$PATH:/leonardo/prod/spack/06/install/0.22/linux-rhel8-icelake/gcc-12.2.0/nco-5.1.9-6mdruevgje4ejl4h4g2cg4xb3y4vb43u/bin"
#module load nco
export PATH="$CONDA_PREFIX/bin:$PATH"
hash -r

export PYTHONHOME=$CONDA_PREFIX
export PYTHONNOUSERSITE=1
unset PYTHONPATH
unset PYTHONUSERBASE
hash -r


TOOLS=/leonardo/home/userexternal/ntilinin/COSIMA/access-om2/tools
ACCESS_INPUT=/leonardo_scratch/fast/ICT26_ESP/ntilinin/INPUT/access-om2
JRA_INPUT=/leonardo_scratch/fast/ICT26_ESP/ntilinin/make_ryf
SPEEDY_INPUT=/leonardo_scratch/fast/ICT26_ESP/ntilinin/SPEEDY_access/access_forcing

# This argument is required by the old script, but is not used for --atm SPEEDY
CORE_INPUT=$ACCESS_INPUT

cd "$TOOLS"

echo "Python:"
which python
python --version

echo "MPI:"
which mpirun
mpirun --version | head

echo "ESMF:"
which ESMF_RegridWeightGen

echo "NCO:"
which ncrename

echo "SPEEDY input:"
ls -lh "$SPEEDY_INPUT/tas_SPEEDY_1990.nc"



# time ./make_remap_weights.py \
#     "$ACCESS_INPUT" \
#     "$JRA_INPUT" \
#     "$SPEEDY_INPUT" \
#     "$CORE_INPUT" \
#     --atm JRA55 \
#     --ocean MOM1 \
#     --method conserve \
#     --npes 1


# # ============================================================
# # SPEEDY T30 -> MOM1/CICE 1 degree
# # ============================================================

# echo
# echo "============================================================"
# echo "Generating first-order conservative weights"
# echo "============================================================"

time ./make_remap_weights.py \
    "$ACCESS_INPUT" \
    "$JRA_INPUT" \
    "$SPEEDY_INPUT" \
    "$CORE_INPUT" \
    --atm SPEEDY \
    --ocean MOM1 \
    --method conserve \
    --npes 1

echo
echo "============================================================"
echo "Generating higher-order patch weights"
echo "============================================================"

time ./make_remap_weights.py \
    "$ACCESS_INPUT" \
    "$JRA_INPUT" \
    "$SPEEDY_INPUT" \
    "$CORE_INPUT" \
    --atm SPEEDY \
    --ocean MOM1 \
    --method patch \
    --npes 1

# ============================================================
# Check output
# ============================================================

echo
echo "Generated files:"
ls -lh SPEEDY_MOM1_conserve.nc SPEEDY_MOM1_patch.nc

echo
echo "Conservative grid dimensions:"
ncdump -v src_grid_dims,dst_grid_dims SPEEDY_MOM1_conserve.nc | tail -10

echo
echo "Patch grid dimensions:"
ncdump -v src_grid_dims,dst_grid_dims SPEEDY_MOM1_patch.nc | tail -10

echo
echo "DONE"