/cevac/scripts/exec_sql.sh "EXEC CEVAC_UPDATE_STATS @BuildingSName = 'WATT', @Metric = 'ebrtb'"

if [ $? -eq 0 ]; then
  echo "Success"
else
  echo "Fail"
fi

