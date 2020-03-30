open_project $env(HLS_TARGET)
open_solution $env(HLS_SOLUTION)
csim_design -ldflags "-L/usr/local/lib/ -lfastcdr -lfastrtps -Wl,-rpath /usr/local/lib/" -argv $env(HLS_ARG)
