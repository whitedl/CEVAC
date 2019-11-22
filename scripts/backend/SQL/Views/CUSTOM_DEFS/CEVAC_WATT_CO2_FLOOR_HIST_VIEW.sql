with h as(
select cevac_watt_co2_xref.PointSliceID, Floor, UTCDateTime, ETDateTime,ActualValue 
from CEVAC_WATT_CO2_HIST inner join CEVAC_WATT_CO2_XREF on CEVAC_WATT_CO2_HIST.PointSliceID = CEVAC_WATT_CO2_XREF.PointSliceID
)
select Floor, avg_value=avg(ActualValue), UTCDateTime,ETDateTime from h group by Floor, UTCDateTime, ETDateTime
