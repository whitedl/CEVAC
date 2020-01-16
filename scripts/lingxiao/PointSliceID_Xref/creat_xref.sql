IF OBJECT_ID('CEVAC_HOLMES_TEMP_XREF') DROP TABLE CEVAC_HOLMES_TEMP_XREF;
GO
USE [WFIC-CEVAC]
CREATE TABLE [dbo].[CEVAC_HOLMES_TEMP_XREF](
[PointSliceID] [int] NOT NULL,        [Room] [nvarchar](MAX) NULL,        [RoomType] [nvarchar](MAX) NULL,        [ObjectName] [nvarchar](MAX) NOT NULL,        [BLG] [nvarchar](50) NOT NULL,        [Floor] [nvarchar](50) NULL,        [ReadingType] [nvarchar](50) NOT NULL,        [Alias] [nvarchar](MAX) NOT NULL,        [Com] [datetime] NULL,        [DeCom] [datetime] NULL,
CONSTRAINT [PK_CEVAC_HOLMES_TEMP_XREF] PRIMARY KEY CLUSTERED
(
[PointSliceID] ASC
)
WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
)
 ON [PRIMARY]
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46399','301','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-301.ZN-T','HOLMES','3rd Floor','Temp','301 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46418','302','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-302.ZN-T','HOLMES','3rd Floor','Temp','302 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46473','303','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-303.ZN-T','HOLMES','3rd Floor','Temp','303 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46382','304','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-304.ZN-T','HOLMES','3rd Floor','Temp','304 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46437','305','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-305.ZN-T','HOLMES','3rd Floor','Temp','305 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46347','306','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-306.ZN-T','HOLMES','3rd Floor','Temp','306 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46402','307','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-307.ZN-T','HOLMES','3rd Floor','Temp','307 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46352','308','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-308.ZN-T','HOLMES','3rd Floor','Temp','308 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46406','309','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-309.ZN-T','HOLMES','3rd Floor','Temp','309 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46463','310','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-310.ZN-T','HOLMES','3rd Floor','Temp','310 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46369','311','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-311.ZN-T','HOLMES','3rd Floor','Temp','311 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46385','312','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-312.ZN-T','HOLMES','3rd Floor','Temp','312 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46479','313','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-313.ZN-T','HOLMES','3rd Floor','Temp','313 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46350','314','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-314.ZN-T','HOLMES','3rd Floor','Temp','314 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46440','315','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-315.ZN-T','HOLMES','3rd Floor','Temp','315 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46458','316','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-316.ZN-T','HOLMES','3rd Floor','Temp','316 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46367','317','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-317.ZN-T','HOLMES','3rd Floor','Temp','317 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46420','318','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-318.ZN-T','HOLMES','3rd Floor','Temp','318 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46478','319','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-319.ZN-T','HOLMES','3rd Floor','Temp','319 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46378','320','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-320.ZN-T','HOLMES','3rd Floor','Temp','320 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46430','321','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-321.ZN-T','HOLMES','3rd Floor','Temp','321 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46451','322','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-322.ZN-T','HOLMES','3rd Floor','Temp','322 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46417','323','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-323.ZN-T','HOLMES','3rd Floor','Temp','323 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46476','324','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-324.ZN-T','HOLMES','3rd Floor','Temp','324 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46383','325','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-325.ZN-T','HOLMES','3rd Floor','Temp','325 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46434','326','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-326.ZN-T','HOLMES','3rd Floor','Temp','326 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46373','327','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-327.ZN-T','HOLMES','3rd Floor','Temp','327 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46392','328','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-328.ZN-T','HOLMES','3rd Floor','Temp','328 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46448','329','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-329.ZN-T','HOLMES','3rd Floor','Temp','329 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46355','330','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-330.ZN-T','HOLMES','3rd Floor','Temp','330 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46408','331','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-331.ZN-T','HOLMES','3rd Floor','Temp','331 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46465','501','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-501.ZN-T','HOLMES','5th Floor','Temp','501 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46368','502','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-502.ZN-T','HOLMES','5th Floor','Temp','502 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46388','503','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-503.ZN-T','HOLMES','5th Floor','Temp','503 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46486','504','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-504.ZN-T','HOLMES','5th Floor','Temp','504 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46357','505','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-505.ZN-T','HOLMES','5th Floor','Temp','505 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46449','506','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-506.ZN-T','HOLMES','5th Floor','Temp','506 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46470','507','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-507.ZN-T','HOLMES','5th Floor','Temp','507 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46374','508','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-508.ZN-T','HOLMES','5th Floor','Temp','508 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46426','509','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-509.ZN-T','HOLMES','5th Floor','Temp','509 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46484','510','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-510.ZN-T','HOLMES','5th Floor','Temp','510 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46393','511','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-511.ZN-T','HOLMES','5th Floor','Temp','511 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46431','512','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-512.ZN-T','HOLMES','5th Floor','Temp','512 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46452','513','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-513.ZN-T','HOLMES','5th Floor','Temp','513 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46395','514','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-514.ZN-T','HOLMES','5th Floor','Temp','514 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46416','515','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-515.ZN-T','HOLMES','5th Floor','Temp','515 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'45459','516','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-516.ZN-T','HOLMES','5th Floor','Temp','516 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46364','517','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-517.ZN-T','HOLMES','5th Floor','Temp','517 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46380','518','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-518.ZN-T','HOLMES','5th Floor','Temp','518 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46436','519','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-519.ZN-T','HOLMES','5th Floor','Temp','519 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46346','520','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-520.ZN-T','HOLMES','5th Floor','Temp','520 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46401','521','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-521.ZN-T','HOLMES','5th Floor','Temp','521 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46459','522','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-522.ZN-T','HOLMES','5th Floor','Temp','522 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46370','523','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-523.ZN-T','HOLMES','5th Floor','Temp','523 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46390','524','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-524.ZN-T','HOLMES','5th Floor','Temp','524 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46481','525','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-525.ZN-T','HOLMES','5th Floor','Temp','525 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46353','526','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-526.ZN-T','HOLMES','5th Floor','Temp','526 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46442','527','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-527.ZN-T','HOLMES','5th Floor','Temp','527 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46464','528','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-528.ZN-T','HOLMES','5th Floor','Temp','528 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46349','529','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-529.ZN-T','HOLMES','5th Floor','Temp','529 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46438','530','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-530.ZN-T','HOLMES','5th Floor','Temp','530 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46461','531','Sleep/Study','HH-NAE-1/Field Bus 2.FCU-531.ZN-T','HOLMES','5th Floor','Temp','531 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46428','203','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 203 FCU.ZN-T','HOLMES','2nd Floor','Temp','203 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46376','204','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 204.ZN-T','HOLMES','2nd Floor','Temp','204 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46397','205','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 205 FCU.ZN-T','HOLMES','2nd Floor','Temp','205 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46454','206','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 206 FCU.ZN-T','HOLMES','2nd Floor','Temp','206 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46363','207','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 207.ZN-T','HOLMES','2nd Floor','Temp','207 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46475','208','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 208.ZN-T','HOLMES','2nd Floor','Temp','208 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46344','210','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 210 FCU.ZN-T','HOLMES','2nd Floor','Temp','210 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46435','211','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 211 FCU.ZN-T','HOLMES','2nd Floor','Temp','211 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46457','212','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 212 FCU.ZN-T','HOLMES','2nd Floor','Temp','212 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46356','213','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 213 FCU.ZN-T','HOLMES','2nd Floor','Temp','213 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46446','214','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 214 FCU.ZN-T','HOLMES','2nd Floor','Temp','214 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46466','215','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 215 FCU.ZN-T','HOLMES','2nd Floor','Temp','215 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46371','216','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 216 FCU.ZN-T','HOLMES','2nd Floor','Temp','216 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46423','217','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 217 FCU.ZN-T','HOLMES','2nd Floor','Temp','217 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46482','218','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 218 FCU.ZN-T','HOLMES','2nd Floor','Temp','218 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46389','219','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 219 FCU.ZN-T','HOLMES','2nd Floor','Temp','219 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46443','220','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 220 FCU.ZN-T','HOLMES','2nd Floor','Temp','220 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46460','221','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 221 FCU.ZN-T','HOLMES','2nd Floor','Temp','221 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46403','222','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 222 FCU.ZN-T','HOLMES','2nd Floor','Temp','222 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46365','223','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 223.ZN-T','HOLMES','2nd Floor','Temp','223 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46386','224','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 224.ZN-T','HOLMES','2nd Floor','Temp','224 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46441','225','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 225 FCU.ZN-T','HOLMES','2nd Floor','Temp','225 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46348','226','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 226 FCU.ZN-T','HOLMES','2nd Floor','Temp','226 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46404','227','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 227 FCU.ZN-T','HOLMES','2nd Floor','Temp','227 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46453','228','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 228 FCU.ZN-T','HOLMES','2nd Floor','Temp','228 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46360','229','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 229 FCU.ZN-T','HOLMES','2nd Floor','Temp','229 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46379','230','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 230 FCU.ZN-T','HOLMES','2nd Floor','Temp','230 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46471','231','Sleep/Study','HH-NAE-1/Field Bus1.HOLMES RM 231 FCU.ZN-T','HOLMES','2nd Floor','Temp','231 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46366','101','Sleep/Study','HH-NAE-1/Field Bus1.RM-101.ZN-T','HOLMES','1sr Floor','Temp','101 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46447','102','Sleep/Study','HH-NAE-1/Field Bus1.RM-102.ZN-T','HOLMES','1sr Floor','Temp','102 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46467','103','Sleep/Study','HH-NAE-1/Field Bus1.RM-103.ZN-T','HOLMES','1sr Floor','Temp','103 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46409','104','Sleep/Study','HH-NAE-1/Field Bus1.RM-104.ZN-T','HOLMES','1sr Floor','Temp','104 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46425','105','Sleep/Study','HH-NAE-1/Field Bus1.RM-105.ZN-T','HOLMES','1sr Floor','Temp','105 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46480','106','Sleep/Study','HH-NAE-1/Field Bus1.RM-106.ZN-T','HOLMES','1sr Floor','Temp','106 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46387','107','Sleep/Study','HH-NAE-1/Field Bus1.RM-107.ZN-T','HOLMES','1sr Floor','Temp','107 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46445','108','Sleep/Study','HH-NAE-1/Field Bus1.RM-108.ZN-T','HOLMES','1sr Floor','Temp','108 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46354','109','Sleep/Study','HH-NAE-1/Field Bus1.RM-109.ZN-T','HOLMES','1sr Floor','Temp','109 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46411','110','Sleep/Study','HH-NAE-1/Field Bus1.RM-110.ZN-T','HOLMES','1sr Floor','Temp','110 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'41590','111','Sleep/Study','HH-NAE-1/Field Bus1.RM-111.ZN-T','HOLMES','1sr Floor','Temp','111 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46429','112','Sleep/Study','HH-NAE-1/Field Bus1.RM-112.ZN-T','HOLMES','1sr Floor','Temp','112 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46375','113','Sleep/Study','HH-NAE-1/Field Bus1.RM-113.ZN-T','HOLMES','1sr Floor','Temp','113 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46391','114','Sleep/Study','HH-NAE-1/Field Bus1.RM-114.ZN-T','HOLMES','1sr Floor','Temp','114 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46487','115','Sleep/Study','HH-NAE-1/Field Bus1.RM-115.ZN-T','HOLMES','1sr Floor','Temp','115 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46359','116','Sleep/Study','HH-NAE-1/Field Bus1.RM-116.ZN-T','HOLMES','1sr Floor','Temp','116 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46412','117','Sleep/Study','HH-NAE-1/Field Bus1.RM-117.ZN-T','HOLMES','1sr Floor','Temp','117 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46469','118','Sleep/Study','HH-NAE-1/Field Bus1.RM-118.ZN-T','HOLMES','1sr Floor','Temp','118 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46361','119','Sleep/Study','HH-NAE-1/Field Bus1.RM-119.ZN-T','HOLMES','1sr Floor','Temp','119 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46415','120','Sleep/Study','HH-NAE-1/Field Bus1.RM-120.ZN-T','HOLMES','1sr Floor','Temp','120 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'36082','121','Sleep/Study','HH-NAE-1/Field Bus1.RM-121.ZN-T','HOLMES','1sr Floor','Temp','121 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46472','122','Sleep/Study','HH-NAE-1/Field Bus1.RM-122.ZN-T','HOLMES','1sr Floor','Temp','122 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46342','123','Sleep/Study','HH-NAE-1/Field Bus1.RM-123.ZN-T','HOLMES','1sr Floor','Temp','123 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46432','124','Sleep/Study','HH-NAE-1/Field Bus1.RM-124.ZN-T','HOLMES','1sr Floor','Temp','124 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46455','201','Sleep/Study','HH-NAE-1/Field Bus1.ROOM 201 FCU.ZN-T','HOLMES','2nd Floor','Temp','201 Temp', NULL , NULL );
GO
INSERT INTO XREF (PointSliceID, Room, RoomType, ObjectName, BLG, Floor, ReadingType, Alias, Com, DeCom) VALUES (
'46410','202','Sleep/Study','HH-NAE-1/Field Bus1.ROOM 202 FCU.ZN-T','HOLMES','2nd Floor','Temp','202 Temp', NULL , NULL );
GO
