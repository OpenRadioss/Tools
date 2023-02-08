# What is OpenRadioss?

**Altair® Radioss®** is an industry-proven analysis solution that helps users evaluate and optimize product performance for highly nonlinear problems under dynamic loading. For more than 30 years, organizations have used Altair Radioss to streamline and optimize the digital design process, replace costly physical tests with quick and efficient simulation, and speed up design optimization iterations.

**OpenRadioss** is the publicly available open-source code base that a worldwide community of researchers, software developers, and industry leaders are enhancing every day. OpenRadioss is changing the game by empowering users to make rapid contributions that tackle the latest challenges brought on by rapidly evolving technologies like battery development, lightweight materials and composites, human body models and biomaterials, autonomous driving and flight, as well as the desire to give passengers the safest environment possible via virtual testing.

With OpenRadioss, scientists and technologists can focus their research on a stable code base under professional maintenance that benefits from the large library of existing finite element capabilities and the continuous integration and continuous development tools provided to contributors.

For more information on OpenRadioss project, please visit the OpenRadioss GitHub at [https://github.com/OpenRadioss/OpenRadioss](https://github.com/OpenRadioss/OpenRadioss) or the OpenRadioss web page [www.openradioss.org](https://www.openradioss.org)
If you have any questions about OpenRadioss, please feel free to contact <webmaster@openradioss.org>. 


# What is OpenRadioss userlib_sdk

**Altair® Radioss®** and **OpenRadioss** have a user interface to create subroutines and use them in Radioss. 
The user library is generated using the userlib_sdk. The userlib_sdk is a collection of different platforms and compilers to create libraries.
Each platform/compiler set has a `build_script`, a static library and Fortran Module files. Those will permit to generate the user library.

User subroutines can be used to develop the following options:

* User material laws for solids and shells
* User failure models
* User sensors
* User spring elements
* User window (general interface for external code)
* User solid elements (may be degenerated to shell or beam elements)

# Repository layout

            source            : SDK Interface source code & Modules ti 
            userlib_routines  : Collection of user routines which can be use to develop the code.
            userlib_sdk       : Userlib SDK this directory hosts the scripts, library & modules files.
                                library, modules files are generated with the build scripts.
            build_script      : script to build the sdk for a platform & a compiler.
            examples          : Example directory with User code and input deck example.
            
# How to build OpenRadioss userlib_sdk

Following page give instructions how to build the userlib_sdk.

[How to Build the userlib_sdk](Howto.md)

# How to use OpenRadioss userlib_sdk

Following page give instructions how to use the userlib_sdk.

[How to use the userlib_sdk](Install.md)

# How to contribute in the Userlib_SDK

[How to contribute in the userlib_sdk](Contributing.md)

