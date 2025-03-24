cmake_minimum_required(VERSION 3.4...3.18)
project(aethermark)

# Read version from the VERSION file
file(READ "${CMAKE_SOURCE_DIR}/VERSION" VERSION_INFO)
string(STRIP ${VERSION_INFO} VERSION_INFO)  # Remove any extra spaces/newlines

add_subdirectory(pybind11)
pybind11_add_module(aethermark src/main.cpp)

# Define VERSION_INFO using the version from the file without extra quotes
target_compile_definitions(aethermark PRIVATE VERSION_INFO=${VERSION_INFO})