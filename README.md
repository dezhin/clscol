# clscol #

Это простая утилита для импорта данных классификаторов в БД, на базе SQLAlchemy, т.е. может
использовать разнличные СУБД, будь то SQLite или PostgeSQL.

Для установки нужен Python 2.7 и, опционально, virtualenv. При помощи virtualenv установка будет
выглядеть следующим образом:

    ~ $ mkdir clscol
    ~ $ cd clscol
    ~/clscol $ virtualenv --no-site-packages env
    ~/clscol $ git clone git://github.com/dezhin/clscol.git
    ~/clscol $ env/bin/pip install -e clscol/

Загрузка данных:

    ~/clscol $ git clone git://github.com/dezhin/clscol-data.git

Список доступных классификаторов:

    ~/clscol $ env/bin/clscol classifiers
    okato  ОКАТО  Общероссийский классификатор объектов административно-территориального деления
    oktmo  ОКТМО  Общероссийский классификатор территорий муниципальных образований

Загрузка классификатора ОКАТО в БД SQLite:

    ~/clscol $ env/bin/clscol import --db sqlite:///test.db okato ../clscol-data/okato/okato-195.yaml
    ~/clscol $ sqlilte3 -column test.db "SELECT * FROM okato LIMIT 5"
    01000000|Алтайский край
    01200000|Районы Алтайского края/
    01201000|Алейский район
    01201800|Сельсоветы Алейского р-на/
    01201802|Алейский

Вместо указания параметра `--db` можно установить переменную окружения `CLSCOL_DB`. Список доспутных
драйверов SQLAlchemy доступен [тут](http://docs.sqlalchemy.org/en/rel_0_7/core/engines.html). SQLite
доступен "из-коробки", для остальных драйверов требует установка соответствующих пакетов через
`env/bin/pip install`, например для PostgreSQL нужно установть psycopg2. В этом случае строка
подключения будет иметь вид: `postgresql://username@host/dbname`.

В одной БД можно хранить несколько версий классификатора, в этом случае данные будут храниться в 
разных таблицах. Например:

    ~/clscol $ export CLSCOL_DB=sqlite:///test.db
    ~/clscol $ env/bin/clscol import --vk 195 okato ../clscol-data/okato/okato-195.yaml
    ~/clscol $ env/bin/clscol import --vk 176 okato ../clscol-data/okato/okato-176.yaml
    ~/clscol $ sqlilte3 -column test.db "SELECT * FROM okato_195 LIMIT 5"
    ~/clscol $ sqlilte3 -column test.db "SELECT * FROM okato_176 LIMIT 5"