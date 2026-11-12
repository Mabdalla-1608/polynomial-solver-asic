library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

use work.polynomial_cfg.all;


entity polynomial_top is
port (PAD_clock, PAD_valid_in, PAD_reset :in std_logic;
	PAD_valid_out : out std_logic;
	PAD_x :in unsigned(in_bits-1 downto 0);
	PAD_y :out unsigned(out_bits-1 downto 0));
end polynomial_top;

architecture Behavioral of polynomial_top is

    component polynomial is
    generic (
        a, b, c, d, in_bits, out_bits :positive -- polynomial coefficients
        );
    port (clock, valid_in, reset :in std_logic;
        valid_out : out std_logic;
        x :in unsigned(in_bits-1 downto 0);
        y :out unsigned(out_bits-1 downto 0));
    end component polynomial;

    component PADDO
        port(A     : in  std_logic;
            PAD   : out std_logic);
    end component;

    component PADDI
        port(Y     : out  std_logic;
            PAD   : in   std_logic);
    end component;

    signal clock_top : std_logic;
    signal valid_in_top : std_logic;
    signal reset_top : std_logic;
    signal valid_out_top : std_logic;
    signal x_top : unsigned(in_bits-1 downto 0);
    signal y_top : unsigned(out_bits-1 downto 0);

begin
-- Input x pad mapping
padxGen: for i in in_bits-1 downto 0 generate
    begin
		inpX: PADDI port map (Y => x_top(i), PAD => PAD_x(i));
end generate;

-- Output y pad mapping
padyGen: for i in out_bits-1 downto 0 generate
    begin
        outpY: PADDO port map (PAD => PAD_y(i), A => y_top(i));
end generate;

-- Clock and control signal pad pad mapping
padClock: PADDI port map (Y => clock_top, PAD => PAD_clock);
padValidIn: PADDI port map (Y => valid_in_top, PAD => PAD_valid_in);
padReset: PADDI port map (Y => reset_top, PAD => PAD_reset);
padValidOut: PADDO port map (PAD => PAD_valid_out, A => valid_out_top);

-- Instantiate polynomial core
polynomialCore : polynomial
            generic map (a => a, b => b, c => c, d => d, in_bits => in_bits, out_bits => out_bits)
            port map (clock => clock_top, valid_in => valid_in_top, reset => reset_top, valid_out => valid_out_top, x => x_top, y => y_top);



end Behavioral;
