# finacneWeb
the finance Web application

#
select ID,DATETIME, case CHECKED when 1 then `ACCOUNT_ID` else '' end as 'check', case CHECKED when 0 then `ACCOUNT_ID` else '' end as 'uncheck' from FINANCIAL_BALANCE group by DATETIME;