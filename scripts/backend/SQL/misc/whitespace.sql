SELECT DISTINCT
Alias,
space             = iif(charindex(char(32), Alias) > 0, 1, 0),
horizontal_tab    = iif(charindex(char(9), Alias) > 0, 1, 0),
vertical_tab      = iif(charindex(char(11), Alias) > 0, 1, 0),
backspace         = iif(charindex(char(8), Alias) > 0, 1, 0),
carriage_return   = iif(charindex(char(13), Alias) > 0, 1, 0),
newline           = iif(charindex(char(10), Alias) > 0, 1, 0),
formfeed          = iif(charindex(char(12), Alias) > 0, 1, 0),
nonbreakingspace  = iif(charindex(char(255), Alias) > 0, 1, 0)
FROM CEVAC_CAMPUS_ENERGY_HIST_RAW;
