#!/usr/bin/python3

# cmd_phyml.py

# Hsin-Ying Chang <hyhazelchang@gmail.com>
# v1 2023/10/02

# Usage: python3 /home/xinchang/pyscript/pyscript_xin/cmd_phyml.py --phyml_dir=/usr/local/bin/phyml --in_dir=/scratch/xinchang/cyano11/cyano11.12/cg_sweep/serial_phybreak/align/phy_split/phy_files/ --out_dir=/scratch/xinchang/cyano11/cyano11.12/cg_sweep/serial_phybreak/align/phy_split/phyml/ --sh_dir=/scratch/xinchang/cyano11/cyano11.12/cg_sweep/serial_phybreak/align/phy_split/sh --in_file_ext=phylip --opt="-q -m JC69 -f e -c 2 -a 0.022" --n_job=80


import argparse
import os
import glob

def main():
    parser = argparse.ArgumentParser(
        description=("Make the shscript for blast execution."),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--phyml_dir",
                        default=None,
                        type=str,
                        help="Phylip file directory. Please provide absolute path.")
    parser.add_argument("--in_dir",
                        default=None,
                        type=str,
                        help="Directory containing input files (the file should have fasta extension). Please provide absolute path.")
    parser.add_argument("--out_dir",
                        default=None,
                        type=str,
                        help="Output directory. Please provide absolute path.")
    parser.add_argument("--sh_dir",
                        default=None,
                        type=str,
                        help="Directory for shell scripts. Please provide absolute path.")
    parser.add_argument("--in_file_ext",
                        default="fasta",
                        type=str)
    parser.add_argument("--opt",
                        default=None,
                        type=str)    
    parser.add_argument("--n_job",
                        default=1,
                        type=int)

    args = parser.parse_args()
    phyml_dir = args.phyml_dir
    in_dir = args.in_dir
    out_dir = args.out_dir
    sh_dir = args.sh_dir
    in_file_ext = args.in_file_ext
    opt = args.opt
    n_job = args.n_job

    # Find the sequence files
    phyfiles = glob.glob(in_dir + "*." + in_file_ext)

    # Make output directory
    if not os.path.exists(out_dir):
        os.system("mkdir -p " + out_dir)

    # Get file names
    count = 0
    phyml_cmd = []
    for phy in phyfiles:
        count += 1
        phy_name = os.path.basename(phy).split(".")[0]
        phyml_cmd.append(phyml_dir + " --input " + phy + " " + opt + " > " + out_dir + phy_name + ".log 2>&1\nif [ -e " + phy + "_phyml_tree.txt ]; then\n\tmv " + phy + "_phyml_tree.txt " + out_dir + phy_name + ".tre\nfi;\nif [ -e " + phy + "_phyml_stats.txt ]; then\n\tmv " + phy + "_phyml_stats.txt " + out_dir + phy_name + ".stat\nfi;\nif [ -e " + phy + "_phyml_boot_trees.txt ]; then\n\tmv " + phy + "_phyml_boot_trees.txt " + out_dir + phy_name + ".boot.tre\nfi;\nif [ -e " + phy + "_phyml_boot_stats.txt ]; then\n\tmv " + phy + "_phyml_boot_stats.txt " + out_dir + phy_name + ".boot.stat\nfi;\nif [ -e " + phy + "_phyml_lk.txt ]; then\n\tmv " + phy + "_phyml_lk.txt " + out_dir + phy_name + ".lk\nfi;")

    # print out job scripts
    os.system("mkdir -p " + sh_dir)
    quo = int(count / n_job)
    mod = int(count % n_job)
    cmd_num = 0
    for n in range(n_job):
        job = open(sh_dir + "job" + str(n+1) + ".sh" , "w")
        if n + 1 <= mod:
            for num in range(quo + 1):
                job.write(phyml_cmd[cmd_num] + "\n")
                cmd_num += 1
            job.close()
        else:
            for num in range(quo):
                job.write(phyml_cmd[cmd_num] + "\n")
                cmd_num += 1
            job.close()

if __name__ == "__main__":
    main()
