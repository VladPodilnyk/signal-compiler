NASM=nasm
NASMFLAGS= -f elf
LDFLAGS= -m elf_i386

% : %.o
	$(LD) $(LDFLAGS) $< -o $@

%.o: %.asm
	$(NASM) $(NASMFLAGS) $< -o $@

clean:
	rm *.o