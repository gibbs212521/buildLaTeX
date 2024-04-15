##
##### 
##
##### CONSTANT BOILER PLATE #######
OUTPUTPATH=.\tex_files


BUILD_TEX=pdflatex
OUTPUT_CMD=--output-directory=

BUILDER_OUTPUT=$(OUTPUT_CMD)$(OUTPUTPATH)
BUILDER_OPTIONS=$(BUILDER_OUTPUT)



PYTHON_FILENAME = .\py_files\src\tex_writer.py 

PYTHON_CMD = python 
PYTHON_CMD = $(PYTHON_CMD)  $(PYTHON_FILENAME) -f 


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
MAKE:: 
	$(MAKE_CALL) BUILD_DIR
	$(MAKE_CALL) build
	$(MAKE_CALL) clean_up
	

build:: .\csv_files\*.csv
	IF EXIST %|pfeF ( \
	@echo %|pfeF %|fF \
	)
	IF EXIST %|pfeF ( \
	$(PYTHON_CMD) %|pfeF\
	)
	IF EXIST %|pfeF ( \
		$(MV) %|pfeF .\tex_files\%|feF \
	) ELSE ( \
		@echo build is finished \
	)
	IF EXIST %|pF\*.csv ( \
		$(MAKE_CALL) build \
		) ELSE ( \
		$(MAKE_CALL) return_csv_files \
	)


return_csv_files: .\tex_files\*.csv
	IF EXIST %|pfF.csv ( \
		$(BUILD_TEX) $(BUILDER_OPTIONS) %|pfF.tex \
	)
	IF EXIST %|pfF.aux ( \
		$(RM) %|pfF.aux \
	)
	IF EXIST %|pfF.log ( \
		$(RM) %|pfF.log \
	)
	IF EXIST %|pfF.out ( \
		$(RM) %|pfF.out \
	)
	IF EXIST %|pfF.csv ( \
		$(MV) %|pfeF .\csv_files\%|feF \
	)	
	IF EXIST %|pF\*.csv ( \
		$(MAKE_CALL) return_csv_files \
		) ELSE ( \
		@echo it is finished \
	)
	


show: .\csv_files\*.csv
	IF EXIST %|pF\*.csv ( \
	@echo %|pfeF %|fF \
	)
	IF EXIST %|pF\*.csv ( \
	$(PYTHON_CMD) %|pfeF\
	)
	IF EXIST %|pF\*.csv ( \
		$(MV) %|pfeF .\tex_files\%|feF \
	) ELSE ( \
		@echo build is finished \
	)
	IF EXIST %|pF\*.csv ( \
		$(MAKE_CALL) show \
		) ELSE ( \
		$(MAKE_CALL) show_csv_files \
	)


show_csv_files: .\tex_files\*.csv
	IF EXIST %|pfF.csv ( \
		$(BUILD_TEX) $(BUILDER_OPTIONS) %|pfF.tex \
	)
	IF EXIST %|pfF.aux ( \
		$(RM) %|pfF.aux \
	)	
	IF EXIST %|pfF.log ( \
		$(RM) %|pfF.log \
	)	
	IF EXIST %|pfF.out ( \
		$(RM) %|pfF.out \
	)	
	IF EXIST %|pF\*.csv ( \
		%|pfF.tex \
	)	
	IF EXIST %|pF\*.csv ( \
		$(MV) %|pfeF .\csv_files\%|feF \
	)	
	IF EXIST %|pF\*.csv ( \
		$(MAKE_CALL) show_csv_files \
		) ELSE ( \
		@echo it is finished \
	)


OPEN_PDF:
	FOR %%i IN (.\tex_files\*.pdf) \
		DO \
		%i

BUILD_DIR:
	IF EXIST .\tex_files\* ( \
		@echo no directory required \
	) ELSE ( \
		mkdir .\tex_files \
	)
	
BUILD_OBJ:
	@echo building...
#####	VARIABLE BUILD	#####

