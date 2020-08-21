import re, os, sys
import subprocess
from functools import reduce
import logging
import arrow 
# import mysql.connector as sql

# logging.basicConfig(filename='/var/log/pihole-blocker.log',
#                     filemode='a',
#                     format="[%(asctime)-15s]  %(message)s",
#                     level=logging.INFO)

class SQL:
    def __init__(self):
        pass 

    def _connect(self):
        return sql.connect(host='localhost', user='apeman')
    
    def insert_item(self, ip, domain):
        '''Add a new record to pihole.blacklist'''
        db = self._connect_mysql()
        cursor = db.cursor()

        query = "insert into pihole.blacklist (date, ip, domain) value (%s, %s, %s)"
        date = arrow.now().format("YYYY-MM-DD")

        cursor.execute(query, (date, ip, domain))
        db.commit()


def block_ip(ip):
    os.system(f"/usr/sbin/ufw insert 1 deny from {ip}")


def _read_queries():
    res = subprocess.check_output(
        'cat /var/log/pihole.log|grep query |tail -n 1000',
        shell=True).decode('utf8').split('\n')
    res.remove('')

    queries = []
    for q in res:
        info = q.strip().split(' ')
        query_time = int(info[1]) * 3600 + reduce(
            lambda a, b: a * 60 + b, map(int, info[2].split(':')), 0)
        # 5 for domain, 7 for client ip
        queries.append((query_time, info[5], info[7]))
    return queries


def _block_by_frequency(rate=100):
    # Block all IPs querying on a domain with rate larger than rate(default 100) per minute
    # Domain rate is defined by queried frequency per minute
    blacklists = set()
    from collections import defaultdict, deque
    cc = defaultdict(deque)
    for i, q in enumerate(_read_queries()):
        t, domain, ip = q
        cc[domain].append((t, ip))
        if len(cc[domain]) >= rate:
            if cc[domain][-1][0] - cc[domain][0][0] <= 60:
                # print(domain, ip)
                blacklists.update(map(lambda e: (e[1], domain), cc[domain]))
            cc[domain].popleft()

    for dd in blacklists:
        block_ip(dd[0])
        msg = "{:<16} is blocked for attacking {:<16}".format(dd[0], dd[1])
        logging.info(msg)

    if blacklists:
        os.system('/usr/sbin/ufw deny 80')
        os.system('/usr/sbin/ufw deny 53')
        os.system('echo "" > /var/log/pihole.log ')
    else:
        os.system('/usr/sbin/ufw allow 80')
        os.system('/usr/sbin/ufw allow 80')


if __name__ == "__main__":
    _block_by_frequency()
    
