all:
	@ echo "To launch a script call:\nmake run script=script_name"

run:
	@ python3 ./Python/$(script)/$(script).py
