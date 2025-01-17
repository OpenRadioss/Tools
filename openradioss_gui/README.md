# OpenRadioss GUI

OpenRadioss GUI is a graphical launcher for OpenRadioss on Linux and Windows.

It is a simple Python/tk based tool to execute OpenRadioss, queue jobs and convert OpenRadioss output files to csv, vtk, d3plot at the end of the run

The D3plot converter can be found at: [Vortex-CAE GitHub repository](https://github.com/Vortex-CAE/Vortex-Radioss)

## Installation

* Python3 must be installed on the system.

  Recommended Python3 version is 3.8 or higher.
  OpenRadioss_GUI was tested with Python 3.6.8, some features may not work.

  * On ***Windows***, install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/)
  * On ***Linux***, install python from your OS Repository.

    * On RedHat, CentOS, Rocky Linux

          dnf install python3
          dnf install python3-tkinter

    * On Debian, Ubuntu

          apt-get install python3
          apt install python3-tk

* Get latest [OpenRadioss Release](https://github.com/OpenRadioss/OpenRadioss/releases)

* Copy the contents of openradioss_gui folder in an OpenRadioss Release Download.

## Execution

* Launch the **OpenRadioss_gui.vbs** on Windows
* Launch the **OpenRadioss_gui.bash** on Linux

![image](./icon/OpenRadioss_gui.png)

### Launch a job

* **Select the Starter input Deck** in .rad, .k or .inp format

  * Click the folder Icon, a browser will appear
  * Browse to the Input deck Directory
  * Select Starter input Deck / Click on Open

* **Enter the number of thread for the job** in the -nt field
* **Enter the number of MPI Domains for the job** in the -np field
* **Click "Add Job"** Run Window apprears.

### Notes

* **Single Precision**  in Run Options dropdown enables the OpenRadioss single precision version
* **Run Starter Only** in Run Options dropdown executes Starter only.
* **Anim - vtk** in Run Options dropdown invokes the Animation to VTK converter at the end of OpenRadioss Engine simulation.
* **TH - csv** in Run Options dropdown invokes the TH to CSV converter at the end of OpenRadioss Engine simulation.
* **Show Queue** and **Clear Queue** buttons manage the run queue.
* The **info** menu has links to the downloads section of github and an ‘About’ credit to the script creators
* **In Windows version only**: On first attempt to submit an mpi run (-np > 1) you will be prompted to locate a suitable vars.bat file on your machine, once selected, this is remembered (to reset, delete the created ‘path_to_mpi_vars.txt’ file from the install directory, or edit its contents)
* ***Anim - d3plot** in Run Options dropdown appears only if Vortex-CAE D3plot converter is detected.
* ***Anim - vtkhdf** in Run Options dropdown appears only if Kitware animtovtkhdf converter is detected.

### The Run Window

The **Run Windows** has the OpenRadioss output.

![image](./icon/job_window.png)

Several buttons permits actions during job execution

* **Stop**: stops the job cleanly writing restart (.rst) file(s)
* **Kill**: kills the job (no restarts written)
* **Anim**: writes an Anim file at the current cycle
* **h3d**: writes/updates the h3d file at the current cycle
* **d3plot**: converts any Anim files present in the run folder to d3plot (always converts all anim files present)
* **Close**: becomes available when job is completed, and closes the run window

### The Queue manager

it is possible to submit further jobs from the submission gui after the first and they will be queued for running when the currently running job completes, the queue can be checked and edited, by clicking the ‘Show Queue’ button in the submission gui.

The Job Queue shows jobs queued along with the options chosen, with the buttons in the window it is possible to cancel the next or last job from the queue, or to manually start the next or last job from the queue (this happens in addition to the queue being processed, jobs will open another run window and run at same time as any running job, queue will continue to automatically run any remaining jobs only when 1st one finishes)

![image](./icon/queue_window.png)
