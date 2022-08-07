
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
    In the MSYS2 shell, run:
      cd "A:/some kind of folder/source_directory"
      make -f makefile_win_mingw clear
      make -f makefile_win_mingw

### Thanks
I deeply appreciate the help of the following people.
- [Hornwitser](https://gist.github.com/Hornwitser/f291638024e7e3c0271b1f3a4723e05a#file-exchange_string_decoder-js)
