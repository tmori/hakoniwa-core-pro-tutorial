cmake_minimum_required(VERSION 3.28)

project(hako-examples-hello_world
    LANGUAGES C CXX
)

find_package(hakoniwa-core CONFIG REQUIRED COMPONENTS assets conductor)

set(OS_TYPE "posix")
if(WIN32)
    set(OS_TYPE "win")
endif()
message(STATUS "OS_TYPE=${OS_TYPE}")

add_executable(hello_world src/hello_world.c)
target_include_directories(hello_world PRIVATE /usr/include/hakoniwa)
target_link_libraries(hello_world PRIVATE
    assets
    conductor
)
