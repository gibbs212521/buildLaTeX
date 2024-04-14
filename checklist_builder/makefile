##
##### 
##
##### CONSTANT BOILER PLATE #######
BUILDPATH=.\tex_files
BINPATH=$(BUILDPATH)\bin
OBJPATH=$(BUILDPATH)\obj
TESTPATH=$(BUILDPATH)\test
OUTPUTPATH=$(BUILDPATH)\output
TEST_BINPATH=$(TESTPATH)\bin
TEST_OBJPATH=$(TESTPATH)\obj

#FILENAME=kata
FILENAME=output
TEX_FILENAME=$(FILENAME).tex
AUX_FILENAME=$(FILENAME).aux
LOG_FILENAME=$(FILENAME).log
OUT_FILENAME=$(FILENAME).out
PDF_FILENAME=$(FILENAME).pdf

BUILD_TEX=pdflatex
OUTPUT_CMD=--output-directory=

BUILDER_OUTPUT=$(OUTPUT_CMD)$(OUTPUTPATH)
BUILDER_OPTIONS=$(BUILDER_OUTPUT)

AUX_FILES=$(OUTPUTPATH)\$(AUX_FILENAME)
AUX_FILES=$(AUX_FILES) $(OUTPUTPATH)\$(LOG_FILENAME)
AUX_FILES=$(AUX_FILES) $(OUTPUTPATH)\$(OUT_FILENAME)

PDF_FILE=$(OUTPUTPATH)\$(PDF_FILENAME)


### app file ending ###
# $(MAKE_CALL) code here 
!ifndef 0 # \	
EXE_FILETYPE=.exe # \
!else
# Make code here 
EXE_FILETYPE=#
#
!endif

INCL= 
CC=gcc
CFLAGS= #-I $(INCL)



# Code below should allow $(MAKE_CALL) and make to operate successfully
# $(MAKE_CALL) code here \
!ifndef 0# \
MV = move # \
RM=del # \
RMDIR=rmdir # \
CP=copy # \
MAKE_CALL=nmake # \
!else
ifeq (0,0) #
# Make code here 
MV=mv -f # 
RM=rm -f #
RMDIR=rm -rf
CP=cp -f # 
MAKE_CALL=make #
endif #
# \
!endif 



##### CONSTANT BUILD #######
MAKE: pdf
	

build::
	$(CP) blankmake Makefile
	FOR %%i IN ($(TST_OBJBUILDS))\
		DO \
		@echo( $$(CC) $$(CFLAGS) -c $$(TST_OBJ%%iSRC) -o $$(TST_OBJ%%i) >> Makefile
	FOR %%i IN ($(OBJBUILDS))\
		DO \
		@echo( $$(CC) $$(CFLAGS) -c $$(OBJ%%iSRC) -o $$(OBJ%%i) >> Makefile

pdf:
	$(BUILD_TEX) $(BUILDER_OPTIONS) $(TEX_FILENAME) 
	$(MAKE_CALL) clean_up

show: 
	$(BUILD_TEX) $(BUILDER_OPTIONS) $(TEX_FILENAME) 
	$(MAKE_CALL) clean_up
	$(PDF_FILE)

run:
	($(FILE_EXE))

clean:
	$(RM) $(APPS)
	$(RMDIR) $(BINPATH) $(TEST_BINPATH)

clean_up:
	$(RM) $(AUX_FILES)
#	$(RM) $(FILEBIN) $(OBJECTS) $(TST_OBJECTS)
#	$(RMDIR) $(OBJPATH) $(TEST_OBJPATH)

clean_all:
	$(MAKE_CALL) clean_up
	$(MAKE_CALL) clean

BUILD_DIR:
	mkdir $(BINPATH)
	mkdir $(OBJPATH)
	mkdir $(TEST_BINPATH)
	mkdir $(TEST_OBJPATH)
	
BUILD_OBJ:
	@echo building...
#####	VARIABLE BUILD	#####
 $(CC) $(CFLAGS) -c $(OBJ1SRC) -o $(OBJ1) 
 $(CC) $(CFLAGS) -c $(OBJ2SRC) -o $(OBJ2) 
 $(CC) $(CFLAGS) -c $(OBJ3SRC) -o $(OBJ3) 
 $(CC) $(CFLAGS) -c $(OBJ4SRC) -o $(OBJ4) 
 $(CC) $(CFLAGS) -c $(OBJ5SRC) -o $(OBJ5) 
 $(CC) $(CFLAGS) -c $(OBJ6SRC) -o $(OBJ6) 
 $(CC) $(CFLAGS) -c $(OBJ7SRC) -o $(OBJ7) 
 $(CC) $(CFLAGS) -c $(OBJ8SRC) -o $(OBJ8) 
