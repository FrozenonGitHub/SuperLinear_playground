cmake_minimum_required(VERSION 3.10)

# Set the project name and version
project(MyProject VERSION 1.0)

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Specify the output directory for build files
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY build)

# Add all .cpp files in the src directory as the source files for the project
file(GLOB_RECURSE SOURCES "*.cpp")

# Add the executable target
add_executable(hello_world hello_world.cpp)
