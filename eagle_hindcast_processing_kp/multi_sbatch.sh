for i in $(seq 1979 1 2020)
do
	sbatch /projects/hindcastra/filepurgatory/hindcastprocessing/eagle_hindcast_processing_kp/RUN.sh $i
	echo $i
done
