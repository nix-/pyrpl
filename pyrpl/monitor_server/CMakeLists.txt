# Specify the minimum required version of CMake
cmake_minimum_required(VERSION 3.10)

# Set the project name
project(4rp_server)

# Specify the cross-compiler
set(CMAKE_C_COMPILER arm-linux-gnueabihf-gcc)

# Set the target executable name
set(EXECUTABLE_NAME 4rp_server)

# Add the source file to the project
add_executable(${EXECUTABLE_NAME} monitor_server.c)

# Headers location
target_include_directories(${EXECUTABLE_NAME} PRIVATE 
    ${CMAKE_SOURCE_DIR}
    # list of headers locations
)
