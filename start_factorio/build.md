
### start_factorio.exe does the following:
    - sets the process (factorio.exe) priority to HIGH
    - sets the affinity for the process
    - the output redirects to a file "temp"

### Usage:
    start_factorio.exe argList affinity_mask
    Where:
       argList - 'factorio.exe --benchmark "save" --benchmark-ticks 100 --disable-audio'
       affinity_mask - 3 https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setprocessaffinitymask");

### Building (Win)
    Install MSYS2.
    Install packages in MSYS2:
      pacman -S mingw-w64-x86_64-gcc
      pacman -S mingw-w64-x86_64-make
      pacman -S mingw-w64-x86_64-gdb
    In the "MSYS2 MinGW 64-bit" shell, run:
      cd "A:/some kind of folder/source_directory"
      make -f makefile_win_mingw clear
      make -f makefile_win_mingw

### Building (Linux)
    I don't have Linux, so you have to write the code yourself.
