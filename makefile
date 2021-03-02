PORT = COM6
AMPY = ampy
AMPY_ARGS = -p $(PORT)

# To ensure files are only reuploaded when they have changed some sligtly odd stuff 
# had to be done. 

# When a file is uploaded to the board, a file is created in the upload_tokens directory.
# The upload-and-display recipe is dependant on the tokens of every file in src.
# Each token is dependant on its respective src file. 
# This means files are only reuploaded when the token is older than the src.

SRC_DIR = ./src/
UPLOAD_TOKEN_DIR = ./upload_tokens/

SRC_FILES = $(wildcard $(SRC_DIR)*.py)
SRC_UPLOAD_TOKENS = $(patsubst $(SRC_DIR)%.py, $(UPLOAD_TOKEN_DIR)%.py_uploaded, $(SRC_FILES))

BOARD_FILES = $(subst _uploaded, , $(subst $(UPLOAD_TOKEN_DIR), , $(wildcard $(UPLOAD_TOKEN_DIR)*.py_uploaded)))

blank :=
define newline

$(blank)
endef

upload-and-display: $(SRC_UPLOAD_TOKENS)
	make open-prompt

open-prompt:
	- PuTTY.exe -serial $(PORT) -sercfg 115200,8,n,1,N

# Upload the file and create the upload token
$(UPLOAD_TOKEN_DIR)%.py_uploaded: $(SRC_DIR)%.py
	$(AMPY) $(AMPY_ARGS) put $<
	echo Created > $@

clean:
	-$(foreach file, $(BOARD_FILES), $(AMPY) $(AMPY_ARGS) rm $(file) $(newline))
	cd $(UPLOAD_TOKEN_DIR)
	-del /S /Q *.py_uploaded

reset:
	$(AMPY) $(AMPY_ARGS) reset




