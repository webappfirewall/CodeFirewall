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
    sub = bool(re.match(r".*(select\s+\*\s+from\s+)([a-zA-Z]+[a-zA-Z0-9]+)\s*;.*", cad, re.I))
    print(sub)
    return sub


# Busca: [CUALQUIER COSA]SELECT * FROM [algo] WHERE [ALGO][CUALQUIER COSA]
def sql3(cad):
    sub = bool(re.match(r".*\s*SELECT\s+\*\s+FROM\s+[a-zA-z]+[a-zA-z1-9]+\s+WHERE\s+[a-zA-z]+[a-zA-z1-9]+.*", cad, re.I))
    print(sub)
    return sub


# Busca borrado de tablas busca: [CUALQUIER COSA]'; DROP TABLE [algo];[CUALQUIER COSA]
def sql2(cad):
    sub = bool(re.match(r".*';\s*DROP\s+TABLE\s+[a-zA-z]+[a-zA-z1-9]+\s*.*", cad, re.I))
    print(sub)
    return sub


# Busca condiconales: [CUALQUIER COSA]' or|and [algo] = [algo][CUALQUIER COSA]
def sql4(cad):
    sub = bool(re.match(r".*'*\s*(OR|AND)\s*.*=.*'*", cad, re.I))
    print(sub)
    return sub


# Busca condiconales: [CUALQUIER COSA]SELECT * FROM [CUALQUIER COSA] WHERE [CUALQUIER COSA]
def sql5(cad):
    sub = bool(re.match(r".*SELECT\s+\*\s+FROM\s+.+\s*WHERE\s+.*", cad, re.I))
    print(sub)
    return sub


# sql1('SELECT * from monas;')
# sql2("Alicia'; DROP TABLE usuarios; SELECT * FROM datos WHERE nombre LIKE '%")
# sql3('consulta := "SELECT * FROM usuarios WHERE user')
#sql4("' and 1 = 1'")
sql5('; SELECT * FROM information_schema.tables WHERE table_name! = “')
