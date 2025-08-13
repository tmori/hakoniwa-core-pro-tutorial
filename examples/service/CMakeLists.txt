cmake_minimum_required(VERSION 3.28)

project(hako-examples-service
    LANGUAGES C CXX
)

find_package(hakoniwa-core CONFIG REQUIRED COMPONENTS assets conductor)

set(OS_TYPE "posix")
if(WIN32)
    set(OS_TYPE "win")
endif()
message(STATUS "OS_TYPE=${OS_TYPE}")

add_executable(asset_server src/asset_server.cpp)
target_include_directories(asset_server 
    PRIVATE /usr/include/hakoniwa
    PRIVATE /usr/include/hakoniwa/pdu
)
target_link_libraries(asset_server PRIVATE
    assets
    conductor
)

add_executable(asset_client src/asset_client.cpp)
target_include_directories(asset_client 
    PRIVATE /usr/include/hakoniwa
    PRIVATE /usr/include/hakoniwa/pdu
)
target_link_libraries(asset_client PRIVATE
    assets
)
