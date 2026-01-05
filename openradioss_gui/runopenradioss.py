# Copyright 1986-2026 Altair Engineering Inc.
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
import tkinter as tk
from tkinter import messagebox
# Inp2rad import
try:
    import inp2rad
    inp2rad_enabled=True
except ImportError:
    inp2rad_enabled=False
# VortexRadioss D3plot import
try:
    from vortex_radioss.animtod3plot.Anim_to_D3plot import readAndConvert
    vd3penabled = True
except ImportError:
    # If VortexRadioss Module not present disable d3plot options
    vd3penabled = False
try:
    from animtovtkhdf import AnimToVTKHDF
    vtkhdfenabled = True     
except ImportError:
    vtkhdfenabled = False        


# Global variables
# --------------------------------------------------------------
# Determine the platform (Windows or Linux)
current_platform = platform.system()
cpu=platform.machine()

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
          self.decktype = 'rad'
       elif extension == ".inp":
           jobname, extension = os.path.splitext(os.path.basename(command[0]))
           file = os.path.join(os.path.dirname(file), jobname + "_0000.rad")
           self.decktype = 'inp'
           run_id = 0
       elif extension == ".k" or extension == ".key":
           run_id = 0
           self.decktype = 'k'
       else:
           run_id = 0
           self.decktype = 'unknown'
    
       running_directory = os.path.dirname(file)
       if running_directory == "":
           running_directory = os.getcwd()

       script_directory = os.path.dirname(os.path.abspath(__file__))
       openradioss_path = os.path.abspath(os.path.join(script_directory, ".."))

       if current_platform == "Windows":
            self.arch="win64"
            self.bin_extension=".exe"
       else:
            if cpu =='aarch64':
                self.arch="linuxa64"
                self.bin_extension=""
            else:
                self.arch="linux64_gf"
                self.bin_extension=""

       self.initial_file      = command[0]
       self.deck              = command[0]
       self.file              = file
       try: 
           self.nt = str(max(int(command[1]),1))
       except:
           self.nt = "1"

       try: 
           self.np = str(max(int(command[2]),1))
       except:
           self.np = "1"

       self.precision         = command[3]
       self.anim_to_vtk       = command[4]
       self.th_to_csv         = command[5]
       self.jobname           = jobname
       self.extension         = extension
       self.run_id            = run_id
       self.running_directory = running_directory
       self.openradioss_path  = openradioss_path
       self.starter_only      = command[6]
       self.anim_to_d2plot    = command[7]
       self.anim_to_vtkhdf    = command[8]
       self.mpi_path          = command[9]
       self.debug             = debug
       self.inp2rad_enabled   = inp2rad_enabled

       if self.debug==1:
           print("RunOpenRadioss Class Initialized")
           print("Command: ",command)
           print("File: ",self.file)
           print("NT: ",self.nt)
           print("NP: ",self.np)
           print("Jobname: ",self.jobname)
           print("Decktype: ",self.decktype)
           print("Extension: ",self.extension)
           print("Run ID: ",self.run_id)
           print("Running Directory: ",self.running_directory)
           print("OpenRadioss Path: ",self.openradioss_path)
           print("MPI Path: ",self.mpi_path)
    # --------------------------------------------------------------
    # retrieve deck type & job name
    # --------------------------------------------------------------
    def get_decktype(self):
        return self.jobname,self.decktype
    # --------------------------------------------------------------
    # define the environment variables to execute OpenRadioss
    # --------------------------------------------------------------
    def environment(self):

        custom_env = os.environ.copy()  # Start with a copy of the current environment
        try:
            np=int (self.np)
        except:
            np=1

        if np > 1 and self.mpi_path != "":
            if self.arch == "win64":
                impi_root=self.mpi_path
                mpi_binpath = self.mpi_path + "\\bin"
                mpi_libpath = self.mpi_path + "\\lib"
                mpi_libfabric = self.mpi_path + "\\opt\\mpi\\libfabric\\bin"
                a_libfabric = self.mpi_path + "\\libfabric\\bin"
                custom_env["I_MPI_ROOT"] = impi_root
                custom_env["PATH"] = os.pathsep.join([mpi_binpath ,mpi_libpath, mpi_libfabric, a_libfabric, custom_env["PATH"] ] )
                custom_env["I_MPI_OFI_LIBRARY_INTERNAL"] = "1"
                # print("PATH=", custom_env["PATH"])
                
            else:
                ompi_root=self.mpi_path
                opal_prefix = ompi_root
                ompi_bin = ompi_root + "/bin"
                ompi_lib = ompi_root + "/lib"
                custom_env["PATH"] = os.pathsep.join([ompi_bin,custom_env["PATH"] ] )
                custom_env["OPAL_PREFIX"] = opal_prefix

                if "LD_LIBRARY_PATH" in custom_env : 
                   custom_env["LD_LIBRARY_PATH"] = os.pathsep.join([ompi_lib,custom_env["LD_LIBRARY_PATH"] ] )
                else:
                   custom_env["LD_LIBRARY_PATH"] = ompi_lib

        nt = self.nt
        OPENRADIOSS_PATH = self.openradioss_path
        RAD_H3D_PATH =  os.path.join(OPENRADIOSS_PATH, "extlib", "h3d", "lib", "win64")
        RAD_CFG_PATH = os.path.join(OPENRADIOSS_PATH, "hm_cfg_files")

        # Add environment
 
        KMP_STACKSIZE = "400m"
        OMP_NUM_THREADS = nt
        I_MPI_PIN_DOMAIN = "auto"

        # Create a custom environment with all the variables you want to pass
        if current_platform == "Linux" and cpu != 'aarch64':
             # linux64_gf / X86-64
             LD_LIBRARY_PATH = ":".join([
                    os.path.join(OPENRADIOSS_PATH, "extlib", "h3d", "lib", "linux64"),
                    os.path.join(OPENRADIOSS_PATH, "extlib", "hm_reader", "linux64") ])

             additional_paths_linux = [
                    os.path.join(OPENRADIOSS_PATH, "extlib", "hm_reader", "linux64"),
                    os.path.join("/", "opt", "openmpi", "bin") ]

             custom_env["OPENRADIOSS_PATH"] = OPENRADIOSS_PATH
             custom_env["RAD_CFG_PATH"] = RAD_CFG_PATH
             custom_env["RAD_H3D_PATH"] = RAD_H3D_PATH
             custom_env["OMP_STACKSIZE"] = KMP_STACKSIZE
             custom_env["OMP_NUM_THREADS"] = OMP_NUM_THREADS

             if "LD_LIBRARY_PATH" in custom_env :
                   custom_env["LD_LIBRARY_PATH"] = os.pathsep.join([LD_LIBRARY_PATH , custom_env["LD_LIBRARY_PATH"] ] )
             else:
                   custom_env["LD_LIBRARY_PATH"] = LD_LIBRARY_PATH

             # Add any additional paths to the existing PATH variable
             custom_env["PATH"] = os.pathsep.join([custom_env["PATH"]] + additional_paths_linux)

        if current_platform == "Linux" and cpu == 'aarch64':
             # linuxa64 / ARM64
             LD_LIBRARY_PATH = ":".join([
                    os.path.join(OPENRADIOSS_PATH, "extlib", "h3d", "lib", "linuxa64"),
                    os.path.join(OPENRADIOSS_PATH, "extlib", "hm_reader", "linuxa64"),
                    os.path.join(OPENRADIOSS_PATH, "extlib", "ArmFlang_runtime", "linuxa64") ])


             custom_env["OPENRADIOSS_PATH"] = OPENRADIOSS_PATH
             custom_env["RAD_CFG_PATH"] = RAD_CFG_PATH
             custom_env["RAD_H3D_PATH"] = RAD_H3D_PATH
             custom_env["OMP_NUM_THREADS"] = OMP_NUM_THREADS

             if "LD_LIBRARY_PATH" in custom_env :
                   custom_env["LD_LIBRARY_PATH"] = os.pathsep.join([LD_LIBRARY_PATH , custom_env["LD_LIBRARY_PATH"] ] )
             else:
                   custom_env["LD_LIBRARY_PATH"] = LD_LIBRARY_PATH


        if current_platform == "Windows":
             KMP_AFFINITY = "disabled"
        # Add paths to PATH environment variable for windows
             additional_paths_win = [
                   os.path.join(OPENRADIOSS_PATH, "extlib", "hm_reader", "win64"),
                   os.path.join(OPENRADIOSS_PATH, "extlib", "intelOneAPI_runtime", "win64") ]

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
        engine_input_files = [ file for file in os.listdir(self.running_directory) if file.startswith(self.jobname) and  file.endswith(".rad") and len(file) == len(self.jobname) + 9 ]
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
    def convert_anim_to_vtk(self):

        if self.anim_to_vtk !='yes':
            return
        animation_file_list = self.get_animation_list()
        if self.debug==1:print("Animation_file_list:",animation_file_list)
        if len(animation_file_list)>0:
            print("")
            print("")
            print(" ------------------------------------------------------")
            print(" Anim-vtk option selected, Converting Anim Files to vtk")
            print(" ------------------------------------------------------")
            print("")
            for anim_file in animation_file_list:
                print(" Anim File Being Converted is "+anim_file)
                anim_to_vtk_exec = os.path.join("exec","anim_to_vtk_"+self.arch+self.bin_extension)
                animtovtk_output_name = os.path.join(self.running_directory, anim_file + ".vtk")

                with open(animtovtk_output_name, 'w') as animtovtk_output_file:
                    animtovtk_command = [ os.path.join(self.openradioss_path, anim_to_vtk_exec), 
                                          os.path.join(self.running_directory, anim_file) ]
                    # Redirect the output to the output file
                    subprocess.run(animtovtk_command, env=self.custom_env, cwd=self.running_directory, stdout=animtovtk_output_file)
            print("")
            print(" ------------------------------------")
            print(" Anim file conversion to vtk complete")
            print(" ------------------------------------")

        else:
            print("")
            print("")
            print(" ----------------------------------------------------------------")
            print(" NB: Anim-vtk option selected, but no Anim files found to convert")
            print(" ----------------------------------------------------------------")



# --------------------------------------------------------------
# Get Time History files list
# --------------------------------------------------------------
    def get_th_list(self):
        th_pattern = self.jobname + "T[0-9][0-9]$"  # Define the pattern
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
    def convert_th_to_csv(self):
        if self.th_to_csv !='yes':
            return
        th_list=self.get_th_list()
        if self.debug==1:print("TH List: ",th_list)

        if len(th_list)>0:
            print("")
            print("")
            print(" ------------------------------------------------------")
            print(" TH-csv option selected, Converting TH Files to csv")
            print(" ------------------------------------------------------")
            print("")

            for th_file in th_list:
                print(" Time History File Being Converted is "+th_file)
                th_to_csv_exec =os.path.join("exec","th_to_csv_"+self.arch+self.bin_extension)
    
                thtocsv_command = [ os.path.join(self.openradioss_path, th_to_csv_exec), 
                                    os.path.join(self.running_directory, th_file)  ]
                # Redirect the output to the th-csv converter
                subprocess.run(thtocsv_command, env=self.custom_env, cwd=self.running_directory)

            print("")
            print(" ------------------------------------")
            print(" TH file conversion to csv complete")
            print(" ------------------------------------")
        else:
            print("")
            print("")
            print(" -------------------------------------------------------------")
            print(" NB: TH-csv option selected, but no TH files found to convert")
            print(" -------------------------------------------------------------")

    def convert_anim_to_vtkhdf(self):
        if self.anim_to_vtkhdf !='yes':
             return
        if not vtkhdfenabled:
                print(" ----------------------------------------------------------------------")
                print(" NB: Anim-vtkhdf option selected, but VortexRadioss module not found  ")
                print(" ----------------------------------------------------------------------")
                return
        animation_file_list = self.get_animation_list()
        if self.debug==1:print("Animation_file_list:",animation_file_list)
        if len(animation_file_list)>0:
            print("")
            print("")
            print(" ----------------------------------------------------------")
            print(" Anim-vtkhdf option selected, Converting Anim Files to vtkhdf")
            print(" ----------------------------------------------------------")
            print("")
            converter = AnimToVTKHDF(verbose=False, static=True)
            animation_files_for_vtkhdf = [os.path.join(self.running_directory, file) for file in animation_file_list]
            output_file_for_vtkhdf = os.path.join(self.running_directory, self.jobname+".vtkhdf")
            try:
                        converter.convert(inputf=animation_files_for_vtkhdf, outputf=output_file_for_vtkhdf)
            except Exception as e:
                    print(" *** Error during Anim to d3plot conversion: ", str(e))
                    print(" ----------------------------------------------------------------")

            print(" -----------------------------------------")
            print(" Anim file conversion to vtkhdf complete")
            print(" -----------------------------------------")
        else:
            print("")
            print("")
            print(" ----------------------------------------------------------------")
            print(" NB: Anim-vtkhdf option selected, but no Anim files found to convert")
            print(" ----------------------------------------------------------------")

    def d3plot_conversion(self):
         if self.anim_to_d2plot !='yes':
             return
         if not vd3penabled:
             print(" ----------------------------------------------------------------------")
             print(" NB: Anim-d3plot option selected, but VortexRadioss module not found  ")
             print(" ----------------------------------------------------------------------")
             return
         animation_file_list = self.get_animation_list()
         if self.debug==1:print("Animation_file_list:",animation_file_list)
         if len(animation_file_list)>0:
             print("")
             print("")
             print(" ------------------------------------------------------")
             print(" Anim-d3plot option selected, Converting Anim Files to d3plot")
             print(" ------------------------------------------------------")
             print("")
             file_stem = os.path.join(self.running_directory, self.jobname)
             try:
                    readAndConvert(file_stem,silent=True)
             except Exception as e:
                    print(" *** Error during Anim to d3plot conversion: ", str(e))
                    print(" ----------------------------------------------------------------")

             print("")
             print(" ---------------------------------------")
             print(" Anim file conversion to d3plot complete")
             print(" ---------------------------------------")

         else:
             print("")
             print("")
             print(" ----------------------------------------------------------------")
             print(" NB: Anim-d3plot option selected, but no Anim files found to convert")
             print(" ----------------------------------------------------------------")

    def inp2rad_conversion(self):
         if self.inp2rad_enabled:
           print(" --------------------------------------------------------")
           print(" Input file is an .inp file, Converting to Radioss format")
           print(" --------------------------------------------------------")
           print("")
           success = inp2rad.execute_gui(self.initial_file, True)
           if success:  
                print(" ------------------------------------------------------")
                print(" Conversion to Radioss format complete")
                print(" ------------------------------------------------------")
                print(" ")
                print(" ")
           else :
                print(" ------------------------------------------------------")
                print(" Conversion to Radioss format failed")
                print(" Please try debugging in standalone mode")
                print(" by running inp2rad from command line")
                print(" ------------------------------------------------------")
                success = False
         else:
                print(" ----------------------------------------------------------------------")
                print(" Input file is an .inp file, Conversion to Radioss format not possible ")
                print(" Check presence of inp2rad.py in the same directory              ")
                print(" ----------------------------------------------------------------------")
                success = False
         return success

    # -------------------------------------------------------------------------
    # Job Process : Run Starter and Engine(s) with environment / Stdout in GUI
    # -------------------------------------------------------------------------
    def job_process(self,starter_command_line,custom_env,exec_dir):
        if current_platform == 'Windows':
            self.process = subprocess.Popen(starter_command_line, env=custom_env,cwd=exec_dir,shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            self.process = subprocess.Popen(starter_command_line, env=custom_env,cwd=exec_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while True:
            line = self.process.stdout.readline().decode('utf8', 'replace')
            if line:
                print("  "+line.strip())
            if not line and self.process.poll() is not None:
                break

    def batch_run(self):
        custom_env = self.environment()
        self.job_name,self.decktype = self.get_decktype()
        self.jobname,self.run_id,self.exec_dir=self.get_jobname_runid_rundirectory()


        print("")
        print("")
        print(" JobName: "+self.jobname)
        print(" ----------------------------")
        print(" Number of MPI processes : "+self.np)
        print(" Number of OpenMP threads: "+self.nt)
        print("")

        if self.decktype == 'inp':
        # Decktype is inp : Run inp2rad conversion
        # -----------------------------------------------
           inp2rad_successful = False  # Flag to track success of conversion
           success = self.inp2rad_conversion()
           if success:  # Assuming `success` is a boolean or status code
                self.deck = self.jobname + '.rad'
                inp2rad_successful = True
           else:
                inp2rad_successful = False
                print(" ---------------------------------------------------------")
                print(" Stopping execution due to unsuccessful inp2rad conversion")
                print(" ---------------------------------------------------------")
                return  # Exit if inp2rad conversion failed


        # Starter Deck - execute Starter
        # -------------------------------
        self.run_number = self.run_id
        if self.run_id==0:

            # First Delete previous result in the directory"
            self.delete_previous_results()

            # Set Run Number to 0 (Starter)
            starter_command_line=self.get_starter_command()
            if self.debug==1:print("StarterCommand: ",starter_command_line)
            if self.debug==1:print("ExecDir: ",self.exec_dir)
            # Run Starter Command
            self.job_process(starter_command_line,custom_env,self.exec_dir)
            self.run_number = self.run_number + 1

        # Go to Engine : proceed or not
        if self.starter_only=='no' :

            # Execute Engine(s)
            # ------------------

            # Get Engine Input File List
            if self.run_id==0:
                engine_file_list = self.get_engine_input_file_list()
            else:
                engine_file_list=[self.deck]

            if self.debug==1:print("Engine_file_list:",engine_file_list)
            self.stop_after_engine = False
            for engine_file in engine_file_list:
                if self.stop_after_engine is True:
                    break
                engine_command_line = self.get_engine_command(engine_file)
                if self.debug==1:print("EngineCommand: ",engine_command_line)
                self.job_process(engine_command_line,custom_env,self.exec_dir)
                self.run_number = self.run_number + 1

            # Execute TH to CSV
            # --------------------
            self.convert_th_to_csv()

            # Execute Anim to VTK
            # --------------------
            self.convert_anim_to_vtk()

            # Execute Anim to D3Plot
            # ----------------------
            self.d3plot_conversion()

            # Execute Anim to VTKHDF
            # --------------------
            self.convert_anim_to_vtkhdf()

        # Job Finished
        # ------------
        print(" ")
        print(" ")
        print(" --------------------")
        print(" Job Finished")
        print(" --------------------")    
