# Compiler
CXX = g++
CXXFLAGS = -std=c++14 -Wall -g -O0

# Source files and executables
SRC_DIR = .
BUILD_DIR = build

SRCS = $(wildcard $(SRC_DIR)/*.cpp)
EXES = $(patsubst $(SRC_DIR)/%.cpp, $(BUILD_DIR)/%, $(SRCS))

# Make all executables
all: $(BUILD_DIR) $(EXES)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Compile each executable
$(BUILD_DIR)/%: $(SRC_DIR)/%.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

clean:
	rm -f $(EXES)

.PHONY: all clean