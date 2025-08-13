cmake_minimum_required(VERSION 3.28)

project(hako-examples-pdu-communication
    LANGUAGES C CXX
)

find_package(hakoniwa-core CONFIG REQUIRED COMPONENTS assets conductor)

set(OS_TYPE "posix")
if(WIN32)
    set(OS_TYPE "win")
endif()
message(STATUS "OS_TYPE=${OS_TYPE}")

add_executable(asset_plant src/asset_plant.c)
target_include_directories(asset_plant 
    PRIVATE /usr/include/hakoniwa
    PRIVATE /usr/include/hakoniwa/pdu
)
target_link_libraries(asset_plant PRIVATE
    assets
    conductor
)

add_executable(asset_controller src/asset_controller.c)
target_include_directories(asset_controller 
    PRIVATE /usr/include/hakoniwa
    PRIVATE /usr/include/hakoniwa/pdu
)
target_link_libraries(asset_controller PRIVATE
    assets
)
