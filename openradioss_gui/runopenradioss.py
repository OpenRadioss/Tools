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
import platform
import glob
import subprocess
import re

# Global variables
# --------------------------------------------------------------
# Determine the platform (Windows or Linux)
current_platform = platform.system()


# Tiny tool to get the runid from the file name
def get_deck_runid(file):
    jobname, extension = os.path.splitext(os.path.basename(file))
    if extension == ".rad":
      jobsuffix = jobname[-4:]  # Equivalent to %jobName:~-4%
      jobname = jobname[:-5]   # Equivalent to %jobName:~0,-5%
      run_id = int(jobsuffix)
    else:
       run_id = 0
    
    return run_id

class RunOpenRadioss():
    # Initialize the class, common variables are saved here
    def __init__(self, command,debug):
       file=command[0]
       jobname, extension = os.path.splitext(os.path.basename(file))

       if extension == ".rad":
          jobsuffix = jobname[-4:]  # Equivalent to %jobName:~-4%
          jobname = jobname[:-5]   # Equivalent to %jobName:~0,-5%
          run_id = int(jobsuffix)
       else:
          run_id = 0
    
       running_directory = os.path.dirname(file)

       script_directory = os.path.dirname(os.path.abspath(__file__))
       openradioss_path = os.path.abspath(os.path.join(script_directory, ".."))

       if current_platform == "Windows":
            self.arch="win64"
            self.bin_extension=".exe"
       else:
            self.arch="linux64_gf"
            self.bin_extension=""

       self.file              = file
       self.nt                = command[1]
       self.np                = command[2]
       self.precision         = command[3]
       self.jobname           = jobname
       self.extension         = extension
       self.run_id            = run_id
       self.running_directory = running_directory
       self.openradioss_path  = openradioss_path
       self.starter_only      = command[6]
       self.debug             = debug

       #print("RunOpenRadioss Class Initialized")
       #print("Command: ",command)
       #print("File: ",self.file)
       #print("NT: ",self.nt)
       #print("NP: ",self.np)
       #print("Jobname: ",self.jobname)
       #print("Extension: ",self.extension)
       #print("Run ID: ",self.run_id)
       #print("Running Directory: ",self.running_directory)
       #print("OpenRadioss Path: ",self.openradioss_path)

    # --------------------------------------------------------------
    # define the environment variables to execute OpenRadioss
    # --------------------------------------------------------------
    def environment(self):

        nt = self.nt
        OPENRADIOSS_PATH = self.openradioss_path
        RAD_H3D_PATH =  os.path.join(OPENRADIOSS_PATH, "extlib", "h3d", "lib", "win64")
        RAD_CFG_PATH = os.path.join(OPENRADIOSS_PATH, "hm_cfg_files")

        # Add paths to PATH environment variable for linux
 
        KMP_STACKSIZE = "400m"
        KMP_AFFINITY = "scatter"
        OMP_NUM_THREADS = nt
        I_MPI_PIN_DOMAIN = "auto"

        # Create a custom environment with all the variables you want to pass
        if current_platform == "Linux":
             LD_LIBRARY_PATH = ":".join([
                    os.path.join(OPENRADIOSS_PATH, "extlib", "h3d", "lib", "linux64"),
                    os.path.join(OPENRADIOSS_PATH, "extlib", "hm_reader", "linux64"),
                    os.path.join("/", "opt", "openmpi", "lib")   ])

             additional_paths_linux = [
                    os.path.join(OPENRADIOSS_PATH, "extlib", "hm_reader", "linux64"),
                    os.path.join(OPENRADIOSS_PATH, "extlib", "intelOneAPI_runtime", "linux64"),
                    os.path.join("/", "opt", "openmpi", "bin") ]

             custom_env = os.environ.copy()  # Start with a copy of the current environment
             custom_env["OPENRADIOSS_PATH"] = OPENRADIOSS_PATH
             custom_env["RAD_CFG_PATH"] = RAD_CFG_PATH
             custom_env["RAD_H3D_PATH"] = RAD_H3D_PATH
             custom_env["OMP_STACKSIZE"] = KMP_STACKSIZE
             custom_env["OMP_NUM_THREADS"] = OMP_NUM_THREADS
             custom_env["KMP_AFFINITY"] = KMP_AFFINITY
             custom_env["LD_LIBRARY_PATH"] = LD_LIBRARY_PATH

             # Add any additional paths to the existing PATH variable
             custom_env["PATH"] = os.pathsep.join([custom_env["PATH"]] + additional_paths_linux)

        if current_platform == "Windows":
                     
        # Add paths to PATH environment variable for windows
             additional_paths_win = [
                   os.path.join(OPENRADIOSS_PATH, "extlib", "hm_reader", "win64"),
                   os.path.join(OPENRADIOSS_PATH, "extlib", "intelOneAPI_runtime", "win64") ]

             custom_env = os.environ.copy()  # Start with a copy of the current environment
             custom_env["OPENRADIOSS_PATH"] = OPENRADIOSS_PATH
             custom_env["RAD_CFG_PATH"] = RAD_CFG_PATH
             custom_env["RAD_H3D_PATH"] = RAD_H3D_PATH
             custom_env["KMP_STACKSIZE"] = KMP_STACKSIZE
             custom_env["OMP_NUM_THREADS"] = OMP_NUM_THREADS
             custom_env["KMP_AFFINITY"] = KMP_AFFINITY
             custom_env["I_MPI_PIN_DOMAIN"] = I_MPI_PIN_DOMAIN

             # Add any additional paths to the existing PATH variable
             custom_env["PATH"] = os.pathsep.join(additional_paths_win + [custom_env["PATH"]]  )
        self.custom_env = custom_env
        return custom_env

    # --------------------------------------------------------------
    # Deletes previous results
    # --------------------------------------------------------------
    def delete_previous_results(self):
   
       extensions_to_delete = [".h3d", "_[0-9][0-9][0-9][0-9].out", "_[0-9][0-9][0-9][0-9].ctl", "_[0-9][0-9][0-9][0-9]_[0-9][0-9][0-9][0-9].rst",
                               "T[0-9][0-9]", "T[0-9][0-9].csv", "A[0-9][0-9][0-9]", "A[0-9][0-9][0-9][0-9]",
                               "A[0-9][0-9][0-9].vtk", "A[0-9][0-9][0-9][0-9].vtk", ".d3plot", ".d3plot[0-9][0-9]",
                               ".d3plot[0-9][0-9][0-9]", ".d3plot[0-9][0-9][0-9][0-9]",'.tmp']

       # Delete files with specified extensions
       for ext_pattern in extensions_to_delete:
          files_to_delete = os.path.join(self.running_directory, self.jobname + f"{ext_pattern}")
          matching_files = [file for file in glob.glob(files_to_delete) if re.match(self.jobname + ext_pattern + '$', os.path.basename(file))]
          #print(matching_files)
          for file in matching_files:
              os.remove(file)

    # --------------------------------------------------------------
    # Get jobname,runid,job,directory from the input file
    # --------------------------------------------------------------
    def get_jobname_runid_rundirectory(self):
       return self.jobname,self.run_id,self.running_directory

    # --------------------------------------------------------------
    # Get jobname,runid,job,directory from the input file
    # --------------------------------------------------------------
    def get_engine_input_file_list(self):
        engine_input_files = [ file for file in os.listdir(self.running_directory) if file.endswith(".rad") ]
        engine_input_files.sort()

        first_item = engine_input_files[0]
        run_id=get_deck_runid(first_item)
        if run_id == 0:
            del engine_input_files[0]

        return engine_input_files

# --------------------------------------------------------------
# Computes the command to run the starter
# --------------------------------------------------------------
    def get_starter_command(self):

        if self.precision == 'sp':
            starter_exec = os.path.join("exec","starter_" + self.arch + "_sp"+self.bin_extension)
        else:
            starter_exec = os.path.join("exec","starter_" + self.arch + self.bin_extension)

        starter_command = [os.path.join(self.openradioss_path, starter_exec), "-i", self.file, "-nt", self.nt, "-np", self.np]
        return starter_command

# --------------------------------------------------------------
# Computes the command to run the engine
# --------------------------------------------------------------
    def get_engine_command(self,engine_input):

        if current_platform == 'Windows':
            mpi='_impi'
        else:
            mpi='_ompi'
        if self.np=="1":
            if self.precision == 'sp':
                engine_exec = os.path.join("exec","engine_"+self.arch+"_sp"+self.bin_extension)
            else: 
                engine_exec = os.path.join("exec","engine_"+self.arch+self.bin_extension)
            engine_command =  [os.path.join(self.openradioss_path, engine_exec), "-i", engine_input]

        else:
            if self.precision == 'sp':
                engine_exec = os.path.join("exec","engine_"+self.arch+mpi+"_sp"+self.bin_extension)
            else:
                engine_exec = os.path.join("exec","engine_"+self.arch+mpi+self.bin_extension)
        
            if current_platform == "Windows":
               engine_command = ["mpiexec","-np",self.np,os.path.join(self.openradioss_path, engine_exec), "-i", engine_input]
            else:
               engine_command = ["mpirun","-np",self.np,os.path.join(self.openradioss_path, engine_exec), "-i", engine_input]
    
        return engine_command

# --------------------------------------------------------------
# Computes the command to run the anim to vtk converter
# --------------------------------------------------------------
    def get_animation_list(self):
        anim_pattern = self.jobname + "A[0-9]{3,}(?:[0-9])?$"  # Define the pattern
        anim_list = [ file for file in os.listdir(self.running_directory) if re.match(anim_pattern, file) ]
        return anim_list

# --------------------------------------------------------------
# Runs the anim to vtk converter
# --------------------------------------------------------------
    def convert_anim_to_vtk(self,anim_file):

        anim_to_vtk_exec = os.path.join("exec","anim_to_vtk_"+self.arch+self.bin_extension)
        animtovtk_output_name = os.path.join(self.running_directory, anim_file + ".vtk")

        with open(animtovtk_output_name, 'w') as animtovtk_output_file:
                animtovtk_command = [ os.path.join(self.openradioss_path, anim_to_vtk_exec), 
                                      os.path.join(self.running_directory, anim_file) ]
                # Redirect the output to the output file
                subprocess.run(animtovtk_command, env=self.custom_env, cwd=self.running_directory, stdout=animtovtk_output_file)

# --------------------------------------------------------------
# Get Time History files list
# --------------------------------------------------------------
    def get_th_list(self):
        th_pattern = self.jobname + "T[0-9][0-9]"  # Define the pattern
        prov_th_to_convert = [ file for file in os.listdir(self.running_directory) if re.match(th_pattern, file) ]
        th_to_convert = []
        # It is possible that .csv files are in the directory
        for file in prov_th_to_convert:
            if not file.endswith(".csv"):
                th_to_convert.append(file)
        return th_to_convert

# --------------------------------------------------------------
# Runs Time History to CSV converter
# --------------------------------------------------------------
    def convert_th_to_csv(self,th_file):
        th_to_csv_exec =os.path.join("exec","th_to_csv_"+self.arch+self.bin_extension)
    
        thtocsv_command = [ os.path.join(self.openradioss_path, th_to_csv_exec), 
                            os.path.join(self.running_directory, th_file)  ]
        # Redirect the output to the th-csv converter
        subprocess.run(thtocsv_command, env=self.custom_env, cwd=self.running_directory)
