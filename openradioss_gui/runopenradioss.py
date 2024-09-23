# Copyright 1986-2024 Altair Engineering Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
# IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import os
import shutil
import platform
import glob
import subprocess
import sys
import re

try:
    from vortex_radioss.animtod3plot.Anim_to_D3plot import readAndConvert
    vd3penabled = True
except ImportError:
    # If VortexRadioss Module not present disable d3plot options
    vd3penabled = False

# Input variables to runopenradioss

file = sys.argv[1]
nt = sys.argv[2]
np = sys.argv[3]
sp = sys.argv[4]
vtk = sys.argv[5]
csv = sys.argv[6]
starter = sys.argv[7]
d3plot = sys.argv[8]

# file = job_file_entry.get_input()
# nt = nt_entry.get_input('1')
# np = np_entry.get_input('1')
# sp = 'sp' if single_status.get() else 'dp'
# vtk = 'yes' if vtk_status.get() else 'no'
# csv = 'yes' if csv_status.get() else 'no'
# starter = 'yes' if starter_status.get() else 'no'
# d3plot = 'yes' if d3plot_status.get() else 'no'

# Determine the platform (Windows or Linux)
current_platform = platform.system()

# Get the current directory of the Python script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Calculate paths
REL_PATH = ".."
ABS_PATH = os.path.abspath(os.path.join(script_directory, REL_PATH))
OPENRADIOSS_PATH = ABS_PATH
RAD_CFG_PATH = os.path.join(OPENRADIOSS_PATH, "hm_cfg_files")
KMP_STACKSIZE = "400m"
KMP_AFFINITY = "scatter"
OMP_NUM_THREADS = nt
I_MPI_PIN_DOMAIN = "auto"
RAD_H3D_PATH_LINUX = os.path.join(OPENRADIOSS_PATH, "extlib", "h3d", "lib", "linux64")
RAD_H3D_PATH_WIN = os.path.join(OPENRADIOSS_PATH, "extlib", "h3d", "lib", "win64")
LD_LIBRARY_PATH = ":".join([
    os.path.join(OPENRADIOSS_PATH, "extlib", "h3d", "lib", "linux64"),
    os.path.join(OPENRADIOSS_PATH, "extlib", "hm_reader", "linux64"),
    os.path.join("/", "opt", "openmpi", "lib")
])

# Add paths to PATH environment variable for windows
additional_paths_win = [
    os.path.join(OPENRADIOSS_PATH, "extlib", "hm_reader", "win64"),
    os.path.join(OPENRADIOSS_PATH, "extlib", "intelOneAPI_runtime", "win64")
]

# Add paths to PATH environment variable for linux
additional_paths_linux = [
    os.path.join(OPENRADIOSS_PATH, "extlib", "hm_reader", "linux64"),
    os.path.join(OPENRADIOSS_PATH, "extlib", "intelOneAPI_runtime", "linux64"),
    os.path.join("/", "opt", "openmpi", "bin")
]

    
if current_platform == "Linux":
    # Create a custom environment with all the variables you want to pass
    custom_env = os.environ.copy()  # Start with a copy of the current environment
    custom_env["REL_PATH"] = REL_PATH
    custom_env["ABS_PATH"] = ABS_PATH
    custom_env["OPENRADIOSS_PATH"] = OPENRADIOSS_PATH
    custom_env["RAD_CFG_PATH"] = RAD_CFG_PATH
    custom_env["RAD_H3D_PATH"] = RAD_H3D_PATH_LINUX
    custom_env["OMP_STACKSIZE"] = KMP_STACKSIZE
    custom_env["OMP_NUM_THREADS"] = OMP_NUM_THREADS
    custom_env["KMP_AFFINITY"] = KMP_AFFINITY
    custom_env["LD_LIBRARY_PATH"] = LD_LIBRARY_PATH

    # Add any additional paths to the existing PATH variable
    custom_env["PATH"] = os.pathsep.join([custom_env["PATH"]] + additional_paths_linux)
    
    #print (custom_env)
    
if current_platform == "Windows":
    # Create a custom environment with all the variables you want to pass
    custom_env = os.environ.copy()  # Start with a copy of the current environment
    custom_env["REL_PATH"] = REL_PATH
    custom_env["ABS_PATH"] = ABS_PATH
    custom_env["OPENRADIOSS_PATH"] = OPENRADIOSS_PATH
    custom_env["RAD_CFG_PATH"] = RAD_CFG_PATH
    custom_env["RAD_H3D_PATH"] = RAD_H3D_PATH_WIN
    custom_env["KMP_STACKSIZE"] = KMP_STACKSIZE
    custom_env["OMP_NUM_THREADS"] = OMP_NUM_THREADS
    custom_env["KMP_AFFINITY"] = KMP_AFFINITY
    custom_env["I_MPI_PIN_DOMAIN"] = I_MPI_PIN_DOMAIN

    
    # Add any additional paths to the existing PATH variable
    custom_env["PATH"] = os.pathsep.join([custom_env["PATH"]] + additional_paths_win)
    
    mpi_path_file = "path_to_intel-mpi.txt"

    if os.path.exists(mpi_path_file):
        with open(mpi_path_file, "r") as mpipathfile:
            MPI_PATH = mpipathfile.readline().strip()
            MPI_PATH = MPI_PATH.replace("/", "\\").strip('"')
    else:
        MPI_PATH = ""

    # Ensure MPI_PATH is not empty or invalid
    if MPI_PATH:
        mpi_paths = [
            os.path.join(MPI_PATH, "libfabric\\bin"),
            os.path.join(MPI_PATH, "bin"),
            os.path.join(MPI_PATH, "bin\\release"),
            os.path.join(MPI_PATH, "libfabric\\bin\\utils"),
            os.path.join(MPI_PATH, "libfabric\\bin")
        ]
        custom_env["PATH"] = os.pathsep.join(mpi_paths + [custom_env["PATH"]])
        custom_env["I_MPI_ROOT"] = MPI_PATH
    else:
        print("MPI_PATH is empty or invalid")
        
# Join the additional paths with the existing PATH variable using the platform-specific path separator
#os.environ["PATH"] = os.pathsep.join([os.environ["PATH"]] + additional_paths)
# Extract information from the input file
running_directory = os.path.dirname(file)
jobname, extension = os.path.splitext(os.path.basename(file))

# Use the extracted information and environment variables as needed
if extension not in (".rad", ".k", ".key"):
    print("Check input file.")
    print("Error termination.")
    exit()  # exit() to terminate the script if filename invalid

if extension == ".rad":
    jobsuffix = jobname[-4:]  # Equivalent to %jobName:~-4%
    jobname = jobname[:-5]   # Equivalent to %jobName:~0,-5%

if extension == ".rad":
    run_id = int(jobsuffix)
    if not jobsuffix.isdigit() or len(jobsuffix) != 4:
        print("Check input file.")
        print("Error termination.")
        exit()  # You can use exit() to terminate the script

else:
    run_id = 0
# Define default values for Windows and Linux
anim_to_vtk_exec_windows = "exec\\anim_to_vtk_win64.exe"
th_to_csv_exec_windows = "exec\\th_to_csv_win64.exe"
single_starterexec_windows = "exec\\starter_win64_sp.exe"
single_engineexec_windows = "exec\\engine_win64_sp.exe"
single_enginempiexec_windows = "exec\\engine_win64_impi_sp.exe"
double_starterexec_windows = "exec\\starter_win64.exe"
double_engineexec_windows = "exec\\engine_win64.exe"
double_enginempiexec_windows = "exec\\engine_win64_impi.exe"

anim_to_vtk_exec_linux = "exec/anim_to_vtk_linux64_gf"
th_to_csv_exec_linux = "exec/th_to_csv_linux64_gf"
single_starterexec_linux = "exec/starter_linux64_gf_sp"
single_engineexec_linux = "exec/engine_linux64_gf_sp"
single_enginempiexec_linux = "exec/engine_linux64_gf_ompi_sp"
double_starterexec_linux = "exec/starter_linux64_gf"
double_engineexec_linux = "exec/engine_linux64_gf"
double_enginempiexec_linux = "exec/engine_linux64_gf_ompi"

# Check if the platform is Windows or Linux and set variables accordingly
if current_platform == "Windows":
    anim_to_vtk_exec = anim_to_vtk_exec_windows
    th_to_csv_exec = th_to_csv_exec_windows
    if sp == "sp":
        starterexec = single_starterexec_windows
        engineexec = single_engineexec_windows
        enginempiexec = single_enginempiexec_windows
    else:
        starterexec = double_starterexec_windows
        engineexec = double_engineexec_windows
        enginempiexec = double_enginempiexec_windows

elif current_platform == "Linux":
    anim_to_vtk_exec = anim_to_vtk_exec_linux
    th_to_csv_exec = th_to_csv_exec_linux
    if sp == "sp":
        starterexec = single_starterexec_linux
        engineexec = single_engineexec_linux
        enginempiexec = single_enginempiexec_linux
    else:
        starterexec = double_starterexec_linux
        engineexec = double_engineexec_linux
        enginempiexec = double_enginempiexec_linux

else:
    # Handle other platforms if needed
    print("Unsupported platform:", current_platform)
    exit()

# Set the filenames and patterns based on the platform
if run_id == 0:
    if current_platform == "Windows":
        extensions_to_delete = [".h3d", "_[0-9][0-9][0-9][0-9].out", "_[0-9][0-9][0-9][0-9].ctl", "_[0-9][0-9][0-9][0-9]_[0-9][0-9][0-9][0-9].rst",
                            "T[0-9][0-9]", "T[0-9][0-9].csv", "A[0-9][0-9][0-9]", "A[0-9][0-9][0-9][0-9]",
                            "A[0-9][0-9][0-9].vtk", "A[0-9][0-9][0-9][0-9].vtk", ".d3plot", ".d3plot[0-9][0-9]",
                            ".d3plot[0-9][0-9][0-9]", ".d3plot[0-9][0-9][0-9][0-9]"]
    else:
        extensions_to_delete = [".h3d", "_[0-9][0-9][0-9][0-9].out", "_[0-9][0-9][0-9][0-9].ctl", "_[0-9][0-9][0-9][0-9]_[0-9][0-9][0-9][0-9].rst",
                            "T[0-9][0-9]", "T[0-9][0-9].csv", "A[0-9][0-9][0-9]", "A[0-9][0-9][0-9][0-9]", 
                            "A[0-9][0-9][0-9].vtk", "A[0-9][0-9][0-9][0-9].vtk", ".d3plot", ".d3plot[0-9][0-9]",
                            ".d3plot[0-9][0-9][0-9]", ".d3plot[0-9][0-9][0-9][0-9]"]

    # Delete files with specified extensions
    for ext_pattern in extensions_to_delete:
        files_to_delete = os.path.join(running_directory, jobname + f"{ext_pattern}")
        matching_files = [file for file in glob.glob(files_to_delete) if re.match(jobname + ext_pattern + '$', os.path.basename(file))]
        #print(matching_files)
        for file in matching_files:
            os.remove(file)

    if extension == ".rad":
        if starter == "no":
            if current_platform == "Windows":
                with open(os.path.join(running_directory, "running_st_" + jobname), "w") as f:
                    f.write(jobname + "_" + f"{run_id:04}")
                jobfilefullpath = os.path.join(running_directory, jobname + "_" + f"{run_id:04}" + extension)
            else:
                with open(os.path.join(running_directory, "running_st_" + jobname), "w") as f:
                    f.write(jobname + "_" + f"{run_id:04}")
                jobfilefullpath = os.path.join(running_directory, jobname + "_" + f"{run_id:04}" + extension)
        else:
            if current_platform == "Windows":
                with open(os.path.join(running_directory, "stopping_st_" + jobname), "w") as f:
                    f.write(jobname + "_" + f"{run_id:04}")
                jobfilefullpath = os.path.join(running_directory, jobname + "_" + f"{run_id:04}" + extension)
            else:
                with open(os.path.join(running_directory, "stopping_st_" + jobname), "w") as f:
                    f.write(jobname + "_" + f"{run_id:04}")
                jobfilefullpath = os.path.join(running_directory, jobname + "_" + f"{run_id:04}" + extension)
    else:
        if starter == "no":
            if current_platform == "Windows":
                with open(os.path.join(running_directory, "running_st_" + jobname), "w") as f:
                    f.write(jobname + "_" + f"{run_id:04}")
                jobfilefullpath = os.path.join(running_directory, jobname + extension)
            else:
                with open(os.path.join(running_directory, "running_st_" + jobname), "w") as f:
                    f.write(jobname + "_" + f"{run_id:04}")
                jobfilefullpath = os.path.join(running_directory, jobname + extension)
        else:
            if current_platform == "Windows":
                with open(os.path.join(running_directory, "stopping_st_" + jobname), "w") as f:
                    f.write(jobname + "_" + f"{run_id:04}")
                jobfilefullpath = os.path.join(running_directory, jobname + extension)
            else:
                with open(os.path.join(running_directory, "stopping_st_" + jobname), "w") as f:
                    f.write(jobname + "_" + f"{run_id:04}")
                jobfilefullpath = os.path.join(running_directory, jobname + extension)

# run OpenRadioss
    starter_command = [os.path.join(OPENRADIOSS_PATH, starterexec), "-i", jobfilefullpath, "-nt", nt, "-np", np]
    subprocess.run(starter_command, env=custom_env, cwd=running_directory)
    
    # Check for the existence of running_st_jobname and delete it if found
    running_st_file = os.path.join(running_directory, "running_st_" + jobname)
    if os.path.exists(running_st_file):
        os.remove(running_st_file)

    # Check for .rad extension and .rst file
    if extension == ".rad":
        rst_pattern = jobname + "_" + jobsuffix + "_0001.rst"
    else:
        rst_pattern = jobname + "_0000_0001.rst"
    
    rst_files = glob.glob(os.path.join(running_directory, rst_pattern))
    if not rst_files:
        exit(1)  # Exit with a non-zero status code

    # Increment runID and update jobsuffix
    run_id += 1
    jobsuffix = "{:04d}".format(run_id)

    # Check for the existence of jobName_jobSuffix.rad
    rad_pattern = jobname + "_" + jobsuffix + ".rad"
    rad_files = glob.glob(os.path.join(running_directory, rad_pattern))

    if not rad_files:
        print("Starter complete, no engines found")
        exit(1)  # Exit with a non-zero status code if engines are not found

if starter == "no" and not run_id == 0:
    while True:
        with open(os.path.join(running_directory, "running_en_" + jobname), "w") as f:
            f.write(jobname + "_" + f"{run_id:04}")
        jobfilefullpath = os.path.join(running_directory, jobname + "_" + f"{run_id:04}" + ".rad")
        if np == "1":
            engine_command = [os.path.join(OPENRADIOSS_PATH, engineexec), "-i", jobfilefullpath, "-nt", nt]
            subprocess.run(engine_command, env=custom_env, cwd=running_directory)

        else:

            # Now, use the updated custom_env to run mpiexec
            if current_platform == "Windows":
                mpiexec_command = [
                    "mpiexec",
                    "-n", str(np),
                    os.path.join(OPENRADIOSS_PATH, enginempiexec),
                    "-i", jobfilefullpath,
                    "-nt", str(nt)
                ]
		
                # Run the mpiexec command with the updated custom_env
                subprocess.run(mpiexec_command, shell=True, env=custom_env, cwd=running_directory)
		

            if current_platform == "Linux":
                mpiexec_command = [
                    "mpirun",
                    "-n", str(np),
                    os.path.join(OPENRADIOSS_PATH, enginempiexec),
                    "-i", jobfilefullpath,
                    "-nt", str(nt)
                ]
  
                # Run the mpiexec command with the updated custom_env
                subprocess.run(mpiexec_command, env=custom_env, cwd=running_directory)

        os.remove(os.path.join(running_directory, "running_en_" + jobname))

        # Check for the .rst file and increment run_id as needed
        run_id += 1
        jobsuffix = "{:04d}".format(run_id)
        if not os.path.exists(os.path.join(running_directory, jobname + "_" + jobsuffix + ".rad")):
            
            break

########################################################################################################        

if vtk == "yes":
    anim_pattern = jobname + "A[0-9]{3,}(?:[0-9])?$"  # Define the pattern

    anim_to_convert = [
        file for file in os.listdir(running_directory) if re.match(anim_pattern, file)
    ]

    if anim_to_convert:
        print("") 
        print("")  
        print("------------------------------------------------------")
        print("Anim-vtk option selected, Converting Anim Files to vtk")
        print("------------------------------------------------------")
        print("")
        for anim_file in anim_to_convert:
            animtovtk_output_name = os.path.join(running_directory, anim_file + ".vtk")
            #print(animtovtk_output_name)
            with open(animtovtk_output_name, 'w') as animtovtk_output_file:
                animtovtk_command = [                    
                    os.path.join(OPENRADIOSS_PATH, anim_to_vtk_exec), 
                    os.path.join(running_directory, anim_file)
                ]
                # Redirect the output to the output file
                subprocess.run(animtovtk_command, env=custom_env, cwd=running_directory, stdout=animtovtk_output_file, text=True)
                #subprocess.run(f"{animtovtk_command} > {animtovtk_output_file}", shell=True, env=custom_env, cwd=running_directory)
                print(f"Anim File Being Converted is {anim_file}", flush=True)
        print("")  
        print("------------------------------------")
        print("Anim file conversion to vtk complete")
        print("------------------------------------")
    else:
        print("") 
        print("")  
        print("----------------------------------------------------------------")
        print("NB: Anim-vtk option selected, but no Anim files found to convert")
        print("----------------------------------------------------------------")

if d3plot == "yes":
    anim_pattern = jobname + "A[0-9]{3,}(?:[0-9])?$"  # Define the pattern

    anim_to_convert = [
        file for file in os.listdir(running_directory) if re.match(anim_pattern, file)
    ]

    if anim_to_convert:
        
        filestem = os.path.join(running_directory, jobname)
        
        print("") 
        print("")  
        print("------------------------------------------------------------")
        print("Anim-d3plot option selected, Converting Anim Files to d3plot")
        print("------------------------------------------------------------")
        print("")
        
        # Use the file stem to call readAndConvert
        readAndConvert(filestem,silent=True)
        
        
        print("")  
        print("---------------------------------------")
        print("Anim file conversion to d3plot complete")
        print("---------------------------------------")
    else:
        print("") 
        print("")  
        print("-------------------------------------------------------------------")
        print("NB: Anim-d3plot option selected, but no Anim files found to convert")
        print("-------------------------------------------------------------------")
        
if csv == "yes":
    th_pattern = jobname + "T[0-9][0-9]"  # Define the pattern

    th_to_convert = [
        file for file in os.listdir(running_directory) if re.match(th_pattern, file)
    ]

    if th_to_convert:
        print("") 
        print("")  
        print("--------------------------------------------------")
        print("TH-csv option selected, Converting TH Files to csv")
        print("--------------------------------------------------")
        print("")
        for th_file in th_to_convert:
            print(f"TH File Being Converted is {th_file}", flush=True)
            thtocsv_command = [                    
                    os.path.join(OPENRADIOSS_PATH, th_to_csv_exec), 
                    os.path.join(running_directory, th_file)
            ]
            # Redirect the output to the th-csv converter
            subprocess.run(thtocsv_command, env=custom_env, cwd=running_directory, text=True)
        print("")  
        print("----------------------------------")
        print("TH file conversion to csv complete")
        print("----------------------------------")
    else:
        print("") 
        print("")  
        print("----------------------------------------------------------------")
        print("NB: TH-csv option selected, but not run since no T files present")
        print("----------------------------------------------------------------")
        
