import re

reservadas = ['or']
sql_keywords = [
    'ADD', 'ADD CONSTRAINT', 'ALTER', 'ALTER COLUMN', 'ALTER TABLE', 'ALL', 'AND', 'ANY', 'AS', 'ASC',
    'BACKUP DATABASE', 'BETWEEN', 'CASE', 'COLUMN',
    'CONSTRAINT', 'CREATE', 'CREATE DATABASE', 'CREATE INDEX', 'CREATE OR REPLACE VIEW', 'CREATE TABLE',
    'CREATE PROCEDURE', 'CREATE UNIQUE INDEX',
    'CREATE VIEW', 'DATABASE', 'DEFAULT', 'DELETE', 'DESC', 'DISTINCT', 'DROP', 'DROP COLUMN', 'DROP CONSTRAINT',
    'DROP DATABASE', 'DROP DEFAULT',
    'DROP INDEX', 'DROP TABLE', 'DROP VIEW', 'EXEC', 'EXISTS', 'FOREIGN KEY', 'FROM', 'FULL OUTER JOIN', 'GROUP BY',
    'HAVING', 'IN', 'INDEX',
    'INNER JOIN', 'INSERT INTO', 'INSERT INTO SELECT', 'IS NULL', 'IS NOT NULL', 'JOIN', 'LEFT JOIN', 'LIKE', 'LIMIT',
    'NOT', 'NOT NULL', 'OR',
    'ORDER BY', 'OUTER JOIN', 'PRIMARY KEY', 'PROCEDURE', 'RIGHT JOIN', 'ROWNUM', 'SELECT', 'SELECT DISTINCT',
    'SELECT INTO', 'SELECT TOP', 'SET',
    'TABLE', 'TOP', 'TRUNCATE TABLE', 'UNION', 'UNION ALL', 'UNIQUE', 'UPDATE', 'VALUES', 'VIEW', 'WHERE', 'CAST',
    'COALESCE', 'CONVERT', 'CURRENT_USER',
    'IIF', 'ISNULL', 'ISNUMERIC', 'NULLIF', 'SESSION_USER', 'SESSIONPROPERTY', 'SYSTEM_USER', 'USER_NAME'
]
javas_keywords = [
    'abstract', 'break', 'char', 'debugger', 'double', 'export*', 'export*', 'goto', 'in', 'let*', 'null', 'public',
    'super*', 'throw', 'try', 'volatile',
    'arguments', 'byte', 'class*', 'default', 'else', 'extends*', 'float', 'if', 'instanceof', 'long', 'package',
    'return', 'switch', 'throws', 'typeof',
    'while', 'await*', 'case', 'const', 'delete', 'enum*', 'false', 'for', 'implements', 'int', 'native', 'private',
    'short', 'synchronized', 'transient',
    'var', 'with', 'boolean', 'catch', 'continue', 'do', 'eval', 'final', 'function', 'import*', 'interface', 'new',
    'protected', 'static', 'this', 'true',
    'void', 'yield', 'alert'
]
html_keywords = [
    '<', '>'
]
php_keywords = [
    '__halt_compiler', 'abstract', 'and', 'array', 'as', 'break', 'callable', 'case', 'catch', 'class', 'clone',
    'const', 'continue', 'declare', 'default',
    'die', 'do', 'echo', 'else', 'elseif', 'empty', 'enddeclare', 'endfor', 'endforeach', 'endif', 'endswitch',
    'endwhile', 'eval', 'exit', 'extends',
    'final', 'for', 'foreach', 'function', 'global', 'goto', 'if', 'implements', 'include', 'include_once',
    'instanceof', 'insteadof', 'interface',
    'isset', 'list', 'namespace', 'new', 'or', 'print', 'private', 'protected', 'public', 'require', 'require_once',
    'return', 'static', 'switch', 'throw',
    'trait', 'try', 'unset', 'use', 'var', 'while', 'xor', '__CLASS__', '__DIR__', '__FILE__', '__FUNCTION__',
    '__LINE__', '__METHOD__', '__NAMESPACE__',
    '__TRAIT__'
]


# Busca select, busca: [CUALQUIER COSA]select from [algo];[CUALQUIER COSA]
def sql1(cad):
    sub = bool(re.match(r".*(select\s+(DISTINCT\s+)?(\*|.+\s+)from\s+(ORDER\s+BY\s+.*(ASC|DESC))?).*", cad, re.I))
    #print(sub)
    return sub


# Busca: [CUALQUIER COSA]SELECT * FROM [algo] WHERE [ALGO][CUALQUIER COSA]
def sql3(cad):
    sub = bool(
        re.match(r".*\s*SELECT\s+(DISTINCT\s+)?(\*|.+\s+)FROM\s+.+\s+WHERE\s+(ORDER\s+BY\s+.*(ASC|DESC))?.+.*", cad,re.I))
    #print(sub)
    return sub


# Busca borrado de tablas busca: [CUALQUIER COSA]'; DROP TABLE [algo];[CUALQUIER COSA]
def sql2(cad):
    sub = bool(re.match(r".*';\s*DROP\s+TABLE\s+[a-zA-z]+[a-zA-z1-9]+\s*.*", cad, re.I))
    #print(sub)
    return sub


# Busca condiconales: [CUALQUIER COSA]' or|and [algo] = [algo][CUALQUIER COSA]
def sql4(cad):
    sub = bool(re.match(r".*(OR|AND)\s+.*=.*", cad, re.I))
    #print(sub)
    return sub


# Busca condiconales: [CUALQUIER COSA]SELECT * FROM [CUALQUIER COSA] WHERE [CUALQUIER COSA]
def sql5(cad):
    sub = bool(re.match(r".*SELECT\s+\*\s+FROM\s+.+\s*WHERE\s+.*", cad, re.I))
    #print(sub)
    return sub


# Busca update: [cualquier cosa] UPDATE [cualquier cosa] SET [cualquier cosa] WHERE
def sql6(cad):
    sub = bool(re.match(r".*UPDATE\s+.*\s+SET\s+.*=.*(WHERE\s+)?.*", cad, re.I))
    #print(sub)
    return sub


def sql7(cad):
    sub = bool(re.match(r".*INSERT\s+INTO\s+.*(\(.*\)\s+)?VALUES\s+\(.*\).*", cad, re.I))
    #print(sub)
    return sub


def sql8(cad):
    sub = bool(re.match(r".*DELETE\s+FROM\s+.+\s+(WHERE\s+)?.*", cad, re.I))
    #print(sub)
    return sub


def sql9(cad):
    sub = bool(re.match(r".*SELECT\s+.+\s+FROM\s+.+\s+(UNION\s+|UNION\s+ALL\s+)SELECT\s+.+\s+FROM\s+.*", cad, re.I))
    #print(sub)
    return sub


def sql10(cad):
    sub = bool(re.match(r".*INSERT\s+INTO\s+.*(\(.*\)\s+)?SELECT\s+.*\s+FROM\s+.*", cad, re.I))
    #print(sub)
    return sub


def sql11(cad):
    sub = bool(re.match(r".*(CREATE\s+PROCEDURE\s.+\s+AS\s+|EXEC\s+).*", cad, re.I))
    #print(sub)
    return sub


def sql12(cad):
    sub = bool(re.match(r".*(CREATE|DROP|BACKUP)\s+DATABASE\s+.*", cad, re.I))
    #print(sub)
    return sub


def sql13(cad):
    sub = bool(re.match(r".*CREATE\s+TABLE\s+.+\(.+\).*", cad, re.I))
    #print(sub)
    return sub


def sql14(cad):
    sub = bool(re.match(r".*(DROP|TRUNCATE)\s+TABLE\s+.+\s", cad, re.I))
    #print(sub)
    return sub


def sql15(cad):
    sub = bool(re.match(r".*ALTER\s+TABLE\s.+\s(ADD|DROP\sCOLUMN|ALTER\sCOLUMN|MODIFY\sCOLUMN|MODIFY)\s+.*", cad, re.I))
    #print(sub)
    return sub


def sql16(cad):
    sub = bool(re.match(r".*(CREATE|DROP)\s+(UNIQUE\s+)?INDEX\s.+(ON\s)?.+", cad, re.I))
    #print(sub)
    return sub


# expresiones regulares para detectar xss
def sql17(cad):
    sub = bool(re.match(r".*<script.*>.*</script>.*", cad, re.I))
    #print(sub)
    return sub


# sql1('SELECT OrderID, Quantity, CASE WHEN Quantity > 30 THEN "The quantity is greater than 30" WHEN Quantity = 30 THEN "The quantity is 30" ELSE "The quantity is under 30" END AS QuantityText FROM OrderDetails;')
# sql2("Alicia'; DROP TABLE usuarios; SELECT * FROM datos WHERE nombre LIKE '%")
# sql3('SELECT * FROM Users WHERE UserId = 105 OR 1=1;')
#sql4("' and 1 = ' 1")
# sql5('; SELECT * FROM information_schema.tables WHERE table_name! = “')
# sql6('UPDATE Customers SET Contacts = "alfred", city= "frank" WHERE customerid = 1; ')
# sql10("INSERT INTO Customers (CustomerName, City, Country) SELECT SupplierName, City, Country FROM Suppliers WHERE perro = gato;")
# sql8('DELETE FROM Customers SET Contacts WHERE customerid = 1;')
# sql9("SELECT perro FROM Customers UNION  SELECT perro FROM Customers;")
# sql11('CREATE PROCEDURE SelectAllCustomers AS SELECT * FROM Customers GO;')
# sql13('CREATE TABLE Persons ( PersonID int, LastName varchar(255), FirstName varchar(255), Address varchar(255), City varchar(255));')
# sql17('<script type="text/javascript"> //<![CDATA[ var i = 10; if (i < 5) {// some code } //]]></script>')
