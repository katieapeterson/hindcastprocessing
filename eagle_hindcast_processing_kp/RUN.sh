#!/bin/bash
#SBATCH --account=hindcastra
#SBATCH --time=4:00:00
#SBATCH --job-name=Hawaii2020raw
#SBATCH --nodes=1
#SBATCH --mem=128GB
#SBATCH --qos=high
#SBATCH --ntasks-per-node=1
#SBATCH --mail-user=katie.peterson@nrel.gov
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --output=output/output_%j.out
#SBATCH --error=error/error_%j.err

module load conda
conda activate processing
srun python /projects/hindcastra/filepurgatory/hindcastprocessing/eagle_hindcast_processing_kp/process_bulk_file.py $1
