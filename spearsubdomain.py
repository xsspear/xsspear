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
import random
import string

def main():
    print("\033[96m[!] Gathering Subdomains...")
    random_tmp_fn = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
    try:
        subdomains = subprocess.getoutput("assetfinder --subs-only {} | httprobe | grep -i 'https' | awk -F '://' '!seen[$2]++'".format(args["target"]))
        print("\033[96m[!] Subdomains: \033[33m%s\n" %len(subdomains.splitlines()))
        count = 0
        for subdomain in subdomains.splitlines():
            print("\033[96m[!] Gathering Subdomain URLs: \033[33m%s" %subdomain[8:])
            getURLs = subprocess.getoutput("wget -O - \"https://web.archive.org/cdx/search/cdx?url=%s&matchType=domain&fl=original&collapse=urlkey\" | grep -v \"\.gif\|\.jpg\|\.js\|\.png\|\.css\|\.zip\|\.rar\|\.apk\|\.exe\|\.tar\|\.gz\|\.eot\|\.ttf\|\.woff\|\.svg\" | awk -F '?' '!seen[$1]++' | awk -F '/' '!seen[$5]++' > /tmp/%s.txt" %(subdomain[8:],random_tmp_fn))

            count += 1

            urls = open('/tmp/'+random_tmp_fn+'.txt','r').read().splitlines()

            print("\033[96m[!] URLs: \033[33m%s" %len(urls))

            counter = 0

            for endpoint in urls:
                prs = set()

                try:
                    r = requests.get(endpoint, timeout=60)
                    mimetype = r.headers['content-type']
                    if mimetype == "text/html; charset=utf-8" or mimetype == "text/html; charset=\"utf-8\"" or mimetype != True:

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

                        q = "=xss<>&"
                        parameters = iter(prs)
                        username = args["output"]
                        results = open(username+'.txt', 'a+')
                        counter += 1

                        print("\n\033[96m[!] Requests: \033[33m%s" %math.trunc(len(prs)/7))
                        print("\033[96m[!] Scanning: \033[33m%s" %endpoint)

                        with tqdm(total=math.trunc(len(prs)/7), desc="\033[96m[!] Progress", bar_format="\033[33m{l_bar}{bar}") as pbar:
                            o = set()
                            async def main(prs):
                                async def get(parameter, session):
                                    try:
                                        async with session.get(parameter, headers=headers, timeout=60) as response:
                                            html = await response.text()
                                            if "xss<>" in html:
                                                o.add(parameter)
                                                results.write("%s\n" %parameter)
                                            pbar.update(1)
                                    except:
                                            pbar.update(1)
                                async with aiohttp.ClientSession() as session:
                                    ret = await asyncio.gather(*[get(endpoint + "?&" + p1 + q + p2 + q + p3 + q + p4 + q + p5 + q + p6 + q + p7 + q, session) for p1, p2, p3, p4, p5, p6, p7 in zip(parameters, parameters, parameters, parameters, parameters, parameters, parameters)])
                            start = time.time()
                            asyncio.run(main(parameters))
                            end = time.time()
                        results.close()

                        print("\033[96m[!] Subdomain: \033[96m%s\033[33m/\033[96m%s" %(count,len(subdomains.splitlines())))
                        print("\033[96m[!] URLs: \033[96m%s\033[33m/\033[96m%s" %(counter,len(urls)))
                        print("\033[96m[!] Duration: \033[33m%s\033[96ms"%math.trunc(end - start))
                        print("\033[96m[!] Reflections: \033[31m%s" % str(len(open(username+'.txt','r').readlines())))
                        os.system("sed -i '1d' /tmp/%s.txt" %random_tmp_fn)

                        if len(o) == 0:
                            print("\033[96m[!] \033[33mSecure")
                        else:
                            print("\033[96m[+] \033[31mInsecure")
                    else:
                        print("\n\033[96m[-] Skipping \033[33m%s \033[96m[Invalid Mime-Type]" %endpoint)
                        pass

                except requests.exceptions.RequestException:
                    print("\n\033[96m[-] Skipping \033[33m%s \033[96m[Couldn't Connect]" %endpoint)
                    pass
                except urllib3.exceptions.LocationParseError:
                    print("\n\033[96m[-] Skipping \033[33m%s \033[96m[Invalid URL]" %endpoint)
                    pass
                except KeyError:
                    print("\n\033[96m[-] Skipping \033[33m%s \033[96m[Undefined Mime-Type]" %endpoint)
                    pass

    except IndexError:
        pass

if __name__ == "__main__":
    try:
        ap = argparse.ArgumentParser()
        ap.add_argument("-t", "--target", required=True, help="Target")
        ap.add_argument("-a", "--agent", required=False, help="User Agent", nargs='?', const=1, default="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20120101 Firefox/33.0")
        ap.add_argument("-c", "--cookies", required=False, help="Cookies", nargs='?', const=1, default="NULL")
        ap.add_argument("-o", "--output", required=True, help="Output", nargs='?', const=1, default="spear.out")
        args = vars(ap.parse_args())
        headers = {'User-Agent': args["agent"], 'Cookie': args["cookies"]}
    except IndexError:
        sys.exit(-1)

main()
