complier=g++
target=clib

source=$(target).cc
obj=$(target).o
shared_obj=$(target).so

.PHONY: all
all: $(obj) $(shared_obj)

$(shared_obj): $(obj)
	$(complier) -shared -o $(shared_obj) $(obj)

$(obj): $(source)
	$(complier) -c -fPIC -o $(obj) $(source)

.PHONY: clean
clean:
	rm $(obj) $(shared_obj)
