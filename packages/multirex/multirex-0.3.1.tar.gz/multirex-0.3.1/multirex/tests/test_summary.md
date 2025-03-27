# MultiREx Test Suite Summary

This document provides an overview of the test suite for the MultiREx project, which is designed to ensure the reliability and correctness of the library's functionality for exoplanet atmosphere simulation.

## Test Categories

The test suite is organized into the following categories:

1. **Atmosphere Tests** - Verify the functionality of the `Atmosphere` class
2. **Planet Tests** - Verify the functionality of the `Planet` class
3. **Star Tests** - Verify the functionality of the `Star` class
4. **System Tests** - Verify the functionality of the `System` class
5. **Physics Tests** - Verify the physics calculations
6. **Utility Tests** - Verify utility functions

## Atmosphere Tests

### Basic Tests (`test_atmosphere.py`)

- **Atmosphere Validation** - Tests that an atmosphere with valid parameters passes validation
- **Invalid Pressure** - Tests that an error is raised when base pressure is lower than top pressure

### Extended Tests (`test_atmosphere_extended.py`)

- **Initialization with Ranges** - Tests that atmosphere parameters can be initialized with range values
- **Multiple Fill Gases** - Tests that an atmosphere can be created with multiple fill gases
- **Pressure Validation** - Tests various pressure validation scenarios:
  - Base pressure equal to top pressure (should fail)
  - Base pressure less than top pressure (should fail)
  - Negative pressures (should fail)
- **Temperature Validation** - Tests temperature validation:
  - Negative temperature (should fail)
  - Temperature range containing negative values (should fail)
- **Missing Attributes** - Tests validation with missing attributes:
  - Missing temperature
  - Missing base pressure
  - Missing top pressure
  - Missing fill gas
- **Reshuffle** - Tests that the reshuffle functionality works correctly

## Planet Tests (`test_planet_atmosphere.py`)

- **Planet Creation without Atmosphere** - Tests creating a planet without an atmosphere
- **Planet with Atmosphere** - Tests creating a planet with an atmosphere
- **Planet Setters** - Tests the setter methods for planet properties

## Star Tests (`test_star.py`)

- **Star Creation** - Tests creating a star with fixed parameters

## System Tests

### Basic Tests (`test_system.py`)

- **System Make Transmission Model** - Tests that the transmission model is generated correctly
- **Generate Spectrum** - Tests that a spectrum can be generated

### Extended Tests (`test_system_extended.py`)

- **System Initialization** - Tests system initialization and validation
- **System Validation with Invalid Components** - Tests system validation with invalid components
- **System Parameter Getters** - Tests system parameter getters
- **System Reshuffle** - Tests system reshuffle functionality
- **Generate Spectrum** - Tests spectrum generation
- **Generate Spectrum without Transmission Model** - Tests spectrum generation without making transmission model first
- **Generate Contributions** - Tests contributions generation
- **Generate Observations** - Tests observations generation
- **System with Phoenix Star** - Tests system with Phoenix stellar model
- **System with Invalid Parameters** - Tests system with invalid parameters
- **System with Range Parameters** - Tests system with range parameters

## Physics Tests (`test_physics.py`)

- **Wavenumber Grid** - Tests that a sorted array is generated for the wavenumber grid
- **Generate Value** - Tests the generate_value function with different input types:
  - Fixed value
  - Range case
  - List case
  - None case

## Utility Tests (`test_utils.py`)

- **Get Stellar Phoenix** - Tests the get_stellar_phoenix function:
  - When Phoenix directory already exists
  - When Phoenix directory doesn't exist and needs to be downloaded
- **Get Gases** - Tests the get_gases function:
  - When opacity database directory already exists
  - When opacity database directory doesn't exist and needs to be downloaded
- **List Gases** - Tests the list_gases function

## Test Coverage

The test suite provides comprehensive coverage of the MultiREx library's functionality, including:

- Object creation and validation
- Parameter validation
- Error handling
- Spectrum generation
- Observation simulation
- Integration with external models (Phoenix stellar model)

Most tests use mock objects to avoid actual downloads and external dependencies, ensuring that tests can run quickly and reliably in any environment.