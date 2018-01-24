# Load designs and libraries

set lib_name cb13fs120_tsmc_max

set tim_margin 1.0
set wr_clk_period  [expr 3 * $tim_margin]
set rd_clk_period  [expr 4 * $tim_margin]
# Area constraint

## Timing constraint
create_clock -name virtual_wr_clk -period ${wr_clk_period}
create_clock -name virtual_rd_clk -period ${rd_clk_period}

create_clock -period ${wr_clk_period} [get_ports wr_clk]
# uncertainty = jitter 0.04 + skew 0.03 + margin 0.05
set_clock_uncertainty  0.12 [get_ports wr_clk]  
set_clock_transition 0.12  [get_ports wr_clk]
set_clock_latency -source -max 0.7 [get_ports wr_clk]
set_clock_latency -max 0.3 [get_ports wr_clk]

create_clock -period ${rd_clk_period} [get_ports rd_clk]
# uncertainty = jitter 0.04 + skew 0.03 + margin 0.05
set_clock_uncertainty  0.12 [get_ports rd_clk]  
set_clock_transition 0.12  [get_ports rd_clk]
set_clock_latency -source -max 0.7 [get_ports rd_clk]
set_clock_latency -max 0.3 [get_ports rd_clk]

## Set constraints on input ports
#suppress_message UID-401
set_driving_cell -library $lib_name -lib_cell sdcfq1 [remove_from_collection [all_inputs] [get_ports *_clk]]
set_input_delay -max 1.0 -clock wr_clk [remove_from_collection [all_inputs] [get_ports "r* aempty* *_clk"] ]
set_input_delay -max 1.3 -clock rd_clk [remove_from_collection [all_inputs] [get_ports "w* afull*  *_clk"] ]
#
## Set constraints on output ports
set_output_delay -max 1.0 -clock wr_clk [remove_from_collection [all_outputs] [get_ports "r* underrun"] ]
set_output_delay -max 1.3 -clock rd_clk [remove_from_collection [all_outputs] [get_ports "w* overrun"]  ]
set_load [expr [load_of $lib_name/an02d0/A1] * 15] [all_outputs]

# Environmental attributes
set_clock_group -name afifo_clk_group -asynchronous -allow_path \
                -group "wr_clk" \
                -group "rd_clk"

#-------------------------------------------------------------------------
# below max_delay solved two issues:
# 1 Async FIFO data/control race check
# 2 Async FIFO gray-coded pointer bus skew check
#-------------------------------------------------------------------------
set_max_delay -from [get_clocks wr_clk] -to [get_clocks rd_clk] [expr ${rd_clk_period}]
set_max_delay -from [get_clocks rd_clk] -to [get_clocks wr_clk] [expr ${wr_clk_period}]

#set_max_delay -from VIRTCLK -through <marker> -to VIRTCLK <value>
#set_multicycle_path -from VIRTCLK -through <marker> -to VIRTCLK <value>


