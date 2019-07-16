        Skrypt odpalamy w screenie: screen -S mojaNazwa

        Nalezy skonfigurowac rootdcmdir w skrypcie. Domyslnie --> rootdcmdir='/var/lib/expacs/ONLINE'

        Jako argumenty skryptu podaj:
        ./move_rsync_study.py rok miesiac dzien1 dzien2 dzien3 /katalog/docelowy
        /katalog/docelowy to miejsce gdzie zostanie stworzona struktura katalogow poczawszy od lat
        
            example: ./move_rsync_study.py 2016 4 6 24 30 /mnt/worek/BACK_ONLINE/
        
        --> przeniesie 6,25,30 kwietnia 2016 roku do /mnt/worek/BACK_ONLINE/
        stworzy drzewo katalogow:
        /mnt/worek/BACK_ONLINE/2016/4/6
        /mnt/worek/BACK_ONLINE/2016/4/24
        /mnt/worek/BACK_ONLINE/2016/4/30
        
        Jesli jako dni podamy 0, przeniesie caly miesiac

            example: ./move_rsync_study.py 2016 4 0 /mnt/worek/BACK_ONLINE/

        16.07.2019
        
        możliwość rsyncowania kilku miesięcy
        
        gdy ostatnia liczba jest równa 0 --> sys.argv[-2], to poprzedzające ją liczby sys.argv[2:-2],
        aż do roku sys.argv[1], są numerami miesięcy.
