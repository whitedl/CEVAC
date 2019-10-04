CREATE FUNCTION ListTable (@text NVARCHAR(300))
RETURNS TABLE
AS

RETURN
SELECT Split.a.value('.', 'NVARCHAR(MAX)') items
FROM(SELECT CAST('<X>'+REPLACE(@text, ',', '</X><X>')+'</X>' AS XML) AS String) AS A
CROSS APPLY String.nodes('/X') AS Split(a)