SELECT
  UTCDateTime,
  dbo.ConvertUTCToLocal(UTCDateTime) AS ETDateTime,
  floor,
  guest_count,
  clemson_count,
  (guest_count + clemson_count) AS total_count
FROM
  CEVAC_COOPER_WAP_FLOOR_HIST_RAW
