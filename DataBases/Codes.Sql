use Taurus;

select * from users;
truncate users;

select * from accounts;
truncate accounts;

select * from transactions;
delete from transactions where acc_id = 'test';
truncate transactions;
 
select * from balance;

select acc_id, DATE(tra_date),
sum(sum(tra_value)) 
OVER (PARTITION BY acc_id
ORDER BY DATE(tra_date))  AS acc_bal
from transactions
group by acc_id,DATE(tra_date)
order by acc_id,DATE(tra_date);

SET SQL_SAFE_UPDATES = 0;