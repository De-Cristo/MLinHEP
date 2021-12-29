import subprocess
import random
import glob
import time
import jug
import os


################################################################# Submitter ###
sge_job_conf = """#!/bin/bash
#$ -l os=sld6
#$ -l site=hh
#$ -cwd
#$ -V
#$ -l h_rt=00:59:00
#$ -l h_vmem=8G
#$ -l mem_free=22G
#$ -l h_fsize=8G
#$ -pe local 4
#$ -j y
#$ -o {log_dir}/
#$ -t 1-{num_sge_jobs}
source /usr/share/Modules/init/sh
export -f module
JOBTMP=/scratch/tmp/$JOB_NAME.$JOB_ID
echo "+++++++++" free -mh
free -mh
echo "+++++++++" $SPARK_HOME/bin/spark-class org.apache.spark.deploy.worker.Worker -d $JOBTMP -m 16G -c 4 $@
$SPARK_HOME/bin/spark-class org.apache.spark.deploy.worker.Worker -d $JOBTMP -m 16G -c 4 $@
"""


class SGESubmitter(object):
    def __init__(self, n_jobs_max, spark_master):
        self.n_jobs_max = n_jobs_max
        self.log_dir = os.path.join(os.getcwd(), 'sge_logs')
        self.spark_master = spark_master

        # prepare dirs
        if not os.path.exists(self.log_dir):
            os.mkdir(self.log_dir)

    @staticmethod
    def parse_num_jobs(qstat_line):
        if not qstat_line.strip():  # empty line
            return 0
        token = qstat_line.split()[-1]  # get last column
        if ':' in token:  #
            running, tot = token.split(':')[0].split('-')
            return int(tot) - int(running)
        else:
            return 1

    def submit(self):
        # how many are needed?
        qstat_cmd = ['qstat | grep spark_wrkr']
        proc = subprocess.Popen(qstat_cmd, shell=True, stdout=subprocess.PIPE)
        res = proc.communicate()[0]
        res = (self.parse_num_jobs(line) for line in res.split('\n'))
        n_workers = sum(res)
        n_workers_needed = self.n_jobs_max - n_workers

        # only submit if at least 5 workers are needed
        if n_workers_needed < 5:
            return

        # prepare sge config
        job_sh = os.path.join(self.log_dir, 'spark_wrkr.sh')
        with open(job_sh, 'w') as f:
            f.write(sge_job_conf.format(
                log_dir=self.log_dir,
                num_sge_jobs=n_workers_needed,
            ))

        qsub_cmd = ['qsub %s %s' % (job_sh, self.spark_master)]
        proc = subprocess.Popen(qsub_cmd, shell=True, stdout=subprocess.PIPE)
        res = proc.communicate()[0]
        if not res.strip():
            raise RuntimeError('Job submission failed.')

    def start(self, every_x_mins=5):
        try:
            while True:
                self.submit()
                time.sleep(60*every_x_mins)
        except KeyboardInterrupt:
            time.sleep(.2)
            exit(0)  # exit gracefully
