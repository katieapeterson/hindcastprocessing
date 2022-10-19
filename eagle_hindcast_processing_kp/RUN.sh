#!/bin/bash
#SBATCH --account=hindcastra
#SBATCH --time=4:00:00
#SBATCH --job-name=Ak2020raw
#SBATCH --nodes=1
#SBATCH --mem=128GB
#SBATCH --qos=high
#SBATCH --ntasks-per-node=1
#SBATCH --mail-user=Aidan.Bharath@nrel.gov
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --output=output/output_%j.out
#SBATCH --error=error/error_%j.err


srun python /projects/hindcastra/cloud_wave_data/process_raw/alaska/process_nc/process_bulk_file.py $1
