SELECT *, dbo.ConvertUTCToLocal(time) AS ETDateTime FROM CEVAC_WATT_WAP_HIST_RAW AS r
INNER JOIN CEVAC_WATT_WAP_XREF as x ON x.WAP_Name = r.name
