cmake_minimum_required(VERSION 3.20)
project(AED_Algoritmo_de_Kahn LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

if (MSVC)
    add_compile_options(/W4)
else()
    add_compile_options(-Wall -Wextra -Wpedantic)
endif()

add_library(kahn_core
        graph.cpp
        int_queue.cpp
        kahn.cpp
        trace.cpp
)
target_include_directories(kahn_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

add_executable(kahn main.cpp)
target_link_libraries(kahn PRIVATE kahn_core)

add_executable(tests tests.cpp)
target_link_libraries(tests PRIVATE kahn_core)

set_target_properties(kahn PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)
set_target_properties(tests PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)