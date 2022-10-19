for i in $(seq 2011 1 2020)
do
	sbatch RUN.sh $i
	echo $i
done
