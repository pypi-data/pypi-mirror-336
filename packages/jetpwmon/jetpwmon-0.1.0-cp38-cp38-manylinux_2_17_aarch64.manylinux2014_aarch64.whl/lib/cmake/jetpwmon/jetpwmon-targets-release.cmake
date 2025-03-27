#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "jetpwmon::jetpwmon" for configuration "Release"
set_property(TARGET jetpwmon::jetpwmon APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(jetpwmon::jetpwmon PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libjetpwmon.so"
  IMPORTED_SONAME_RELEASE "libjetpwmon.so"
  )

list(APPEND _cmake_import_check_targets jetpwmon::jetpwmon )
list(APPEND _cmake_import_check_files_for_jetpwmon::jetpwmon "${_IMPORT_PREFIX}/lib/libjetpwmon.so" )

# Import target "jetpwmon::jetpwmon_static" for configuration "Release"
set_property(TARGET jetpwmon::jetpwmon_static APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(jetpwmon::jetpwmon_static PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "C"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libjetpwmon_static.a"
  )

list(APPEND _cmake_import_check_targets jetpwmon::jetpwmon_static )
list(APPEND _cmake_import_check_files_for_jetpwmon::jetpwmon_static "${_IMPORT_PREFIX}/lib/libjetpwmon_static.a" )

# Import target "jetpwmon::jetpwmon_cpp" for configuration "Release"
set_property(TARGET jetpwmon::jetpwmon_cpp APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(jetpwmon::jetpwmon_cpp PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libjetpwmon_cpp.so"
  IMPORTED_SONAME_RELEASE "libjetpwmon_cpp.so"
  )

list(APPEND _cmake_import_check_targets jetpwmon::jetpwmon_cpp )
list(APPEND _cmake_import_check_files_for_jetpwmon::jetpwmon_cpp "${_IMPORT_PREFIX}/lib/libjetpwmon_cpp.so" )

# Import target "jetpwmon::jetpwmon_static_cpp" for configuration "Release"
set_property(TARGET jetpwmon::jetpwmon_static_cpp APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(jetpwmon::jetpwmon_static_cpp PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libjetpwmon_static_cpp.a"
  )

list(APPEND _cmake_import_check_targets jetpwmon::jetpwmon_static_cpp )
list(APPEND _cmake_import_check_files_for_jetpwmon::jetpwmon_static_cpp "${_IMPORT_PREFIX}/lib/libjetpwmon_static_cpp.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
