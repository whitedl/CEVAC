#! /bin/bash
usage="Usage:
  -b BuildingSName
  -m Metric
	-a Age

  -h help
  -y run without asking
"
while getopts b:m:e:a:hy option; do
  case "${option}"
    in
    b) BuildingSName=${OPTARG};;
    m) Metric=${OPTARG};;
    a) Age=${OPTARG};;
    h) echo "$usage" && exit 1 ;;
    y) yes="yes";;
  esac
done
[ -z "$BuildingSName" ] && echo "BuildingSName  (e.g. WATT): " && read BuildingSName
[ -z "$Metric" ] && echo "Metric  (e.g. TEMP): " && read Metric
[ -z "$Age" ] && echo "Age     (e.g. HIST): " && read Age
if [ -z "$BuildingSName" ] || [ -z "$Metric" ] || [ -z "$Age" ]; then exit 1; fi
TableName="CEVAC_""$BuildingSName""_$Metric""_$Age"
dest_TableName=`python3 /cevac/python/name_shortener.py $TableName`

array=()
array+=("

/* Create metadata macro variables */
%let IOMServer      = %nrquote(SASApp);
%let metaPort       = %nrquote(8561);
%let metaSmeta     = %nrquote(wfic-sas-meta.clemson.edu);

LIBNAME LASRLIB SASIOLA  TAG=\"OPT.SASINSIDE.SASVA\"  PORT=10031 HOST=\"wfic-sas-im-hd\"  SIGNER=\"https://sas.clemson.edu:8343/SASLASRAuthorization\" ;
%LET AL_META_LASRLIB=Visual Analytics Public LASR;

/* Register Table Macro */
%macro registertable( REPOSITORY=, REPOSID=, LIBRARY=, TABLE=, FOLDER=, TABLEID=, PREFIX= );

/* Mask special characters */

   %let REPOSITORY=%superq(REPOSITORY);
   %let LIBRARY   =%superq(LIBRARY);

   %let FOLDER    =%superq(FOLDER);
   %let TABLE     =%superq(TABLE);

   %let REPOSARG=%str(REPNAME=\"&REPOSITORY.\");
   %if (\"&REPOSID.\" ne \"\") %THEN %LET REPOSARG=%str(REPID=\"&REPOSID.\");

   %if (\"&TABLEID.\" ne \"\") %THEN %LET SELECTOBJ=%str(&TABLEID.);
   %else                         %LET SELECTOBJ=&TABLE.;

   %if (\"&FOLDER.\" ne \"\") %THEN
      %PUT INFO: Registering &FOLDER./&SELECTOBJ. to &LIBRARY. library.;
   %else
      %PUT INFO: Registering &SELECTOBJ. to &LIBRARY. library.;

   proc metalib;
      omr (
         library=\"&LIBRARY.\" 
         %str(&REPOSARG.) 
          ); 
      %if (\"&TABLEID.\" eq \"\") %THEN %DO;
         %if (\"&FOLDER.\" ne \"\") %THEN %DO;
            folder=\"&FOLDER.\";
         %end;
      %end;
      %if (\"&PREFIX.\" ne \"\") %THEN %DO;
         prefix=\"&PREFIX.\";
      %end;
      select (\"&SELECTOBJ.\"); 
   run; 
   quit;

%mend;
/* Synchronize table registration */
/* %global AL_METAREPOSITORY; */
/* %let AL_METAREPOSITORY=%SYSFUNC(getoption(METAREPOSITORY)); */
%registerTable(
     LIBRARY=%nrstr(/Shared Data/SAS Visual Analytics/Public/Visual Analytics Public LASR)
     , REPOSITORY=%nrbquote(%SYSFUNC(getoption(METAREPOSITORY)))
   , TABLE=%nrstr($dest_TableName)
   , FOLDER=%nrstr(/Shared Data/SAS Visual Analytics/Public/LASR)
   );

")

array+=("
/* Generate the process id for job  */ 
%put Process ID: &SYSJOBID;

/* General macro variables  */ 
%let jobID = %quote(A5MJT3HI.BV0001NZ);
%let etls_jobName = %nrquote(load);
%let etls_userID = %nrquote(sas);

%global applName;
data _null_;
applName=\"SAS Data Integration Studio\";
call symput('applName',%nrstr(applName));
run;
/* Performance Statistics require ARM_PROC sub-system   */ 
%macro etls_startPerformanceStats;
   %log4sas();
   %log4sas_logger(Perf.ARM, 'level=info');
   options armagent=log4sas armsubsys=(ARM_PROC);
   %global _armexec;
   %let _armexec = 1;
   %perfinit(applname=\"&applName\");
   %global etls_recnt;
   %let etls_recnt=-1;
%mend;
%etls_startPerformanceStats;

%macro etls_setArmagent;
   %let armagentLength = %length(%sysfunc(getoption(armagent)));
   %if (&armagentLength eq 0) %then
      %do;
         %log4sas();
         %log4sas_logger(Perf.ARM, 'level=info');
         options armagent=log4sas armsubsys=(ARM_PROC);
      %end;
%mend etls_setArmagent;

%macro etls_setPerfInit;
   %if \"&_perfinit\" eq \"0\" %then 
      %do;
         %etls_setArmagent;
         %global _armexec;
         %let _armexec = 1;
         %perfinit(applname=\"&applName\");
      %end;
%mend etls_setPerfInit; 

/* Setup to capture return codes  */ 
%global job_rc trans_rc sqlrc;
%let sysrc = 0;
%let job_rc = 0;
%let trans_rc = 0;
%let sqlrc = 0;
%global etls_stepStartTime; 
/* initialize syserr to 0 */ 
data _null_; run;
"
)

array+=("
%macro rcSet(error); 
   %if (&error gt &trans_rc) %then 
      %let trans_rc = &error;
   %if (&error gt &job_rc) %then 
      %let job_rc = &error;
%mend rcSet; 

%macro rcSetDS(error); 
   if &error gt input(symget('trans_rc'),12.) then 
      call symput('trans_rc',trim(left(put(&error,12.))));
   if &error gt input(symget('job_rc'),12.) then 
      call symput('job_rc',trim(left(put(&error,12.))));
%mend rcSetDS; 

/* Create metadata macro variables */
%let IOMServer      = %nrquote(SASApp);
%let metaPort       = %nrquote(8561);
%let metaSmeta     = %nrquote(wfic-sas-meta.clemson.edu);

/* Setup for capturing job status  */ 
%let etls_startTime = %sysfunc(datetime(),datetime.);
%let etls_recordsBefore = 0;
%let etls_recordsAfter = 0;
%let etls_lib = 0;
%let etls_table = 0;

%global etls_debug; 
%macro etls_setDebug; 
   %if %str(&etls_debug) ne 0 %then 
      OPTIONS MPRINT%str(;); 
%mend; 
%etls_setDebug; 



%let transformID = %quote(A5MJT3HI.$0000039);
%let trans_rc = 0;
%let etls_stepStartTime = %sysfunc(datetime(), datetime20.); 

/* Access the data for SQL-CEVAC  */ 
libname CEVACDB odbc user=wficcm password=\"5wattcevacmaint$\" datasrc=WATTCEVAC;
/* LIBNAME CEVACDB SQLSVR  Datasrc=WATTCEVAC  SCHEMA=dbo  AUTHDOMAIN=\"cevac_db_auth\" ; */
%rcSet(&syslibrc); 

/* Access the data for Visual Analytics Public LASR  */ 
LIBNAME LASRLIB SASIOLA  TAG=\"OPT.SASINSIDE.SASVA\"  PORT=10031 HOST=\"wfic-sas-im-hd\"  SIGNER=\"https://sas.clemson.edu:8343/SASLASRAuthorization\" ;
%rcSet(&syslibrc); 


")

array+=("
%let etls_recnt = 0;
%macro etls_recordCheck; 
   %let etls_recCheckExist = %eval(%sysfunc(exist(CEVACDB.$TableName, DATA)) or 
         %sysfunc(exist(CEVACDB.$TableName, VIEW))); 
   
   %if (&etls_recCheckExist) %then
   %do;
      proc sql noprint;
         select count(*) into :etls_recnt from CEVACDB.$TableName;
      quit;
   %end;
%mend etls_recordCheck;
%etls_recordCheck;

%let SYSLAST = %nrquote(CEVACDB.$TableName); 

/* Runtime statistics macros  */ 
%etls_setPerfInit;
%perfstrt(txnname=%BQUOTE(_DISARM|&transformID|&syshostname|SAS LASR Analytic Server Loader), metrNam6=_DISROWCNT, metrDef6=Count32)   ;

proc datasets lib = LASRLIB nolist nowarn memtype = (data view);
   delete $dest_TableName;
quit;

data LASRLIB.$dest_TableName;
set CEVACDB.$TableName;
run;


proc metalib;
   omr (libid=\"BA000009\"
      repid=\"A5MJT3HI\");
   report(type = summary);
   update_rule = (noadd);
   select (A5MJT3HI.BE0004LB);
run;

%perfstop(metrVal6=%sysfunc(max(&etls_recnt,-1)));
%let etls_recnt=-1;



/** Step end SAS LASR Analytic Server Loader **/

%let etls_endTime = %sysfunc(datetime(),datetime.);

/* Turn off performance statistics collection  */ 
data _null_;
   if \"&_perfinit\" eq \"1\" then 
      call execute('%perfend;');
      
run;

")

echo "" > /cevac/cache/sas_scripts/$TableName.sas

for l in "${array[@]}"; do
  echo "${l}" >> /cevac/cache/sas_scripts/$TableName.sas
done
# echo "$script" > /cevac/cache/sas_scripts/$TableName.sas
# if ! rsync -vh --progress /cevac/cache/sas_scripts/$TableName.sas CEVAC@wfic-sas-im-hd.clemson.edu:~/scripts/$TableName.sas; then
if ! rsync -vh --progress /cevac/cache/sas_scripts/$TableName.sas sas@wfic-sas-im-hd.clemson.edu:~/CEVAC/$TableName.sas; then
# if ! rsync -vh --progress /cevac/cache/sas_scripts/$TableName.sas CEVAC@wfic-sas-meta.clemson.edu:~/scripts/$TableName.sas; then
  echo "error"
fi
