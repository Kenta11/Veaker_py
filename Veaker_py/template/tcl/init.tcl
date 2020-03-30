open_project $env(HLS_TARGET)

add_files $env(HLS_SOURCE) -cflags "-Iinclude/ -Itest/include/ -std=c++11"
add_files -tb $env(HLS_TEST) -cflags "-Iinclude/ -Itest/include/ -I/usr/local/include/ -std=c++11"
