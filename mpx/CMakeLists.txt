cmake_minimum_required(VERSION 2.8)

PROJECT (mpx)

# Variables
set(SOURCE_ROOT Source/C++)
set(SOURCE_CODECS ${SOURCE_ROOT}/Codecs)
set(SOURCE_CORE ${SOURCE_ROOT}/Core)

# Compiler warning and optimization flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall")

if (EMSCRIPTEN)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-warn-absolute-paths")
endif()

# MPX Library
file(GLOB MPX_SOURCES
  ${SOURCE_CODECS}/*.cpp
  ${SOURCE_CORE}/*.cpp
)

add_library(mpx STATIC ${MPX_SOURCES})

# Includes
include_directories(
  ${SOURCE_CORE}
  ${SOURCE_CODECS}
)

# Apps
set(MPX_APPS "MpxInfo;MpxDump")
foreach(app ${MPX_APPS})
  string(TOLOWER ${app} binary_name)
  add_executable(${binary_name} ${SOURCE_ROOT}/Apps/${app}.cpp)
  target_link_libraries(${binary_name} mpx)
endforeach()