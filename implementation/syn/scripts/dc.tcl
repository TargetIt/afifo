
printvar target_library
printvar link_library
alias
check_library
check_tlu_plus_files
analyze -library WORK -format verilog -vcs "-f ../filelist.vc"
elaborate async_fifo -architecture verilog -library DEFAULT
current_design async_fifo
link
write -hierarchy -f ddc -out unmapped/async_fifo.ddc
list_designs
list_libs
source afifo.tcl
compile_ultra
report_constraint -all
report_timing
report_area
write -hierarchy -format ddc -output ./mapped/async_fifo.ddc
remove_design -all
