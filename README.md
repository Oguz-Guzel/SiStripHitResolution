# SiStripHitResolution

Run the hit resolution analyser on slurm

```sh
slurm_submit -s slurmJob_hitresol_test.py
```

Run the (dummy) plotter script, the first part on slurm

```sh
slurm_submit -s dummy_analyzer_per_mod_part1.py --inputFile filesList.txt
```
