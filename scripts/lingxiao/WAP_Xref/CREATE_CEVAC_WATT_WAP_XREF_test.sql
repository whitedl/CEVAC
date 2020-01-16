IF OBJECT_ID('CEVAC_WATT_WAP_XREF') IS NOT NULL DROP TABLE 'CEVAC_WATT_WAP_XREF';
 GO
 USE [WFIC-CEVAC]
 CREATE TABLE [dbo].[CEVAC_WATT_WAP_XREF](
 [WAP_ID] INT PRIMARY KEY, [WAP_Name] NVARCHAR (100) NOT NULL, [Room] NVARCHAR (50) NOT NULL, [Floor] NVARCHAR (50) NOT NULL, [Alias] NVARCHAR (50) NOT NULL )
 GO
 INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-1-108nw-ap2702i-34','108', '1st Floor','108 North West');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-1-108se-ap2702i-39','108', '1st Floor','108 South East');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-1-108sw-ap2702i-35','108', '1st Floor','108 South West');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-1-110-ap2702i-30','110', '1st Floor','110');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-2-203-ap2702i-48','203', '2nd Floor','203');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-3-300d-ap2702i-52','300', '3rd Floor','300 Corridor');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-3-308-ap2702i-60','308', '3rd Floor','308');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-3-310s-ap2702i-111','310', '3rd Floor','310');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-3-313-ap2702i-59','313', '3rd Floor','313');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-3-319-ap2702i-57','319', '3rd Floor','319');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-3-323-ap2702i-58','323', '3rd Floor','323');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-3-339e-ap2702i-51','339', '3rd Floor','339 Administration Area');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-3-344u-ap2702i-50','344', '3rd Floor','344 Corridor');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-4-401u-ap2802i-5','401', '4th Floor','401');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-4-416-ap2802i-8','416', '4th Floor','416');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-4-444-ap2802i-11','444', '4th Floor','444');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-1-102-ap2702i-33','102', '1st Floor','102');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-1-106se-ap2702i-37','106', '1st Floor','106 South East');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-1-112-ap2702i-31','112', '1st Floor','112');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-3-310n-ap2702i-56','310', '3rd Floor','310');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-3-333-ap2702i-53','333', '3rd Floor','33');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-4-408-ap2802i-6','408', '4th Floor','408');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-4-433-ap2802i-10','433', '4th Floor','433');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-3-329-ap2702i-54','329', '3rd Floor','329');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-4-418-ap2802i-9','418', '4th Floor','418');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-4-terrace-n-ap1562i-4','450', '4th Floor','450 North Terrace');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-2-200n-ap2702i-42','200', '2nd Floor','200 North Corridor');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-2-208nw-ap2702i-46','208', '2nd Floor','208 North West');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-2-218-ap2702i-41','218', '2nd Floor','218');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-3-344c-ap2702i-49','344', '3rd Floor','344 Conference Room');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-1-113-ap2702i-27','100N', '1st Floor','100N North Atrium');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-2-216-ap2702i-43','216', '2nd Floor','216');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-2-208sw-ap2702i-47','208', '2nd Floor','208 South West');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-3-303-ap2702i-61','303', '3rd Floor','303');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-4-terrace-s-ap1562i-3','450', '4th Floor','450 South Terrace');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-3-316n-ap2702i-112','316', '3rd Floor','316 North');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-1-100l-ap2702i-36','100', '1st Floor','100 Mid Atrium');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-1-106nw-ap2702i-38','106', '1st Floor','106 Rear Right');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-3-316s-ap2702i-55','316', '3rd Floor','316 South');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-1-101a-ap2702i-40','100', '1st Floor','100 South Atrium');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-4-413-ap2802i-7','413', '4th Floor','413 Teaming Area');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-2-200s-ap2702i-44','200', '2nd Floor','200 South Corridor');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-2-208se-ap2702i-45','208', '2nd Floor','208 South East');
 GO
INSERT INTO CEVAC_WATT_WAP_XREF (WAP_Name,Room,Floor,Alias) VALUES ('c-wfic-1-108ne-ap2702i-32','108', '1st Floor','108 North East');
 GO
