import random
from wsgiref import headers
from bs4 import BeautifulSoup
import time 
import os
from typing import List, Dict
import xlsxwriter
import re
import logging
import os 

en_cookies = {
    'ih-experiment': 'eyJzcGVjaWFsc0xhbmRpbmdQYWdlIjp7IkNob3NlblZhcmlhbnQiOjAsIkVuZERhdGUiOiIyMDIzLTAxLTAxVDAwOjAwOjAwIn0sImF1dG9TaGlwQW5kU2F2ZU1lc3NhZ2UiOnsiQ2hvc2VuVmFyaWFudCI6MSwiRW5kRGF0ZSI6IjIwMjMtMDEtMDFUMDA6MDA6MDAifSwidWdjLXRhZ3MtZWN0amEiOnsiQ2hvc2VuVmFyaWFudCI6MCwiRW5kRGF0ZSI6IjIwMjMtMDktMDFUMDA6MDA6MDAifSwidWdjLWtleXdvcmQtZSI6eyJDaG9zZW5WYXJpYW50IjoxLCJFbmREYXRlIjoiMjAyMi0xMi0wMVQwMDowMDowMCJ9fQ==',
    'ih-cc-pref': 'eyJmdW5jdGlvbmFsIjowLCJhbmFseXRpY3MiOjB9',
    'transactionIds': 'undefined',
    'ForceTrafficSplitType': 'A',
    'dscid': 'd6d8c0f4-e115-471e-9b1c-706cbdf19796',
    '_gid': 'GA1.2.1589508374.1662350583',
    '_gcl_au': '1.1.4489372.1662350584',
    '_scid': '179a3172-f951-4d1d-84cd-4b98b9de7db1',
    '_fbp': 'fb.1.1662350584502.1272128199',
    '_tt_enable_cookie': '1',
    '_ttp': '6c39b938-4f36-40be-8801-c05d7bb8b488',
    '_sctr': '1|1662303600000',
    '_pin_unauth': 'dWlkPVpHWXhabVk1Wm1VdFlqZG1NUzAwT1RFMExXSTVOekF0TmprMllXTXdNR1kwTVRJMQ',
    'FPID': 'FPID2.2.J6G7x3zDM5nEePQxuBpuYmRfyqgsV7C5Z%2Fy3b8Fqtcc%3D.1662350582',
    '_pxvid': '6fe1d590-2d2a-11ed-a3e5-734d744f7a45',
    '_wp_uid': '2-a26c41fd33b3f7cc9980fbcb85fa9721-s1639705101.2228|windows_10|chrome-xm0ra6',
    'ih-hp-vp': '15',
    'ih-hp-view': '1',
    'ihr-session-id1': 'aid=8293839f-2d09-4d21-a375-2df47f0bc4e5',
    'ihr-ocid1': '8293839f-2d09-4d21-a375-2df47f0bc4e5',
    '__pxvid': '9b359a63-2e87-11ed-9b88-0242ac120002',
    'pxcts': '7ea7532c-2ec1-11ed-a193-64586f717045',
    'notice_behavior': 'implied,eu',
    'FPAU': '1.1.4489372.1662350584',
    '_lr_uf_-enxord': 'a9bba88e-ef57-4e0a-9e2c-406f953b93ec',
    'ihr-ds-vps': '102552,82704,61864,64903,62118,95098,96984,96268,95852,97009',
    'notice_preferences': '3:',
    'notice_gdpr_prefs': '0,1,2,3:',
    'cmapi_gtm_bl': '',
    'cmapi_cookie_privacy': 'permit 1,2,3,4',
    'FPLC': '1gGtIaeDg2JAxx13WR%2B1xxQ5jkqYiqxIS7k0ncRb%2Fo2WWhuht2Blyln8OB6nZQCgSoMY8cW8f0mGFOmVD0T1f0jDTUCW1U1Jq5GmXGvZY6SsZALUyjw1R6fTQ5Ezgg%3D%3D',
    '_pxhd': 'hddCJozI8d5k8NehOnPnHP8zdhBNgQr8nxHUgAn1Ngwx2wIlEDGLF5s4e8CXgc3suT9qhq2l9JQ9fbdrK1/q7A',
    'ih-preference': 'store=0&country=KR&language=en-US&currency=KRW',
    'pref-saved': '2',
    'iher-pref1': 'storeid=0&sccode=KR&lan=en-US&scurcode=KRW&wp=2&lchg=1&ifv=1&accsave=0&bi=1',
    '__cf_bm': '2.T1OwoGbP3Br7kCao_G9p1ocui2CSKqs7ThSufPG7U-1662647185-0-AVbSeooPx7wht16PnlNkyZmE7mhA1xLcAtg8JjTDqJjlXBgDmjWtoB9BZQr36gi6Tk/3yTFlqf1375EuNGDYpOPA5C4XPnyh2xOrO10okFF0',
    'ihr-temse': 'expires=08%20Oct%202022%2015:26:26Z',
    'user-related': '{"HasNavigatedSite":{"timestamp":1662647186337}}',
    '_lr_tabs_-enxord%2Fiherb': '{%22sessionID%22:0%2C%22recordingID%22:%225-199bb21e-58f8-4653-9349-e24f40b06441%22%2C%22lastActivity%22:1662647186895}',
    '_lr_hb_-enxord%2Fiherb': '{%22heartbeat%22:1662647307053}',
    'iher-vps': '38964.46874.64903.62118.61864.99740.96229.96236.89210.64009.96231.96323.71031.77593.70316.101714.70317.84569.102552.82704.95098.96984.96268.95852.97009.106898.100012.99178.96982.106892',
    '_pxff_cc': 'U2FtZVNpdGU9TGF4Ow==',
    '_pxff_tm': '1',
    '_ga': 'GA1.2.638579261.1662350582',
    '_px3': '77088c992f6d768f647414e1078fcc0c176abee9edab442e59b641fb77cae669:D8o18qocRr/V4qcVtQ7n1b/xn9OPiRwCJ/oisrYe2PTWh0qwJAD6opNfyOGeUYvb15dYDI4yCXmkm6sQhZ/YYA==:1000:zlvMFxCMRyx3YbNg5yR0wALlr5sfdKZ+71wEAk2C64e0EwccW5Ykapxj1+rqraESW/IvPPpBsE8vkzABiXZ2EytZq3u7FS47cD75SkWMiBNZrroYxZehFvE5Xa2PGATmds9zczNPNjTxsQ4p6Xyo3fXd+bO7SKjeivNMzQVb3tM/Lc/sa45UKWmoVuIC8FqHJLivYIrwXIXzdsDS2whnuw==',
    '_dc_gtm_UA-229961-54': '1',
    'cto_bundle': 'RJ26MV9nekt3dEMxcUpqNCUyQnVzSkZrZWFpeGFxVHM1SmZ5VWV6NlBYSldIaU94SnUxWU8wQWl2TUtVUnFEWUNOa3ZVWFl6SXVGSFJPeEtDWkJIakNZSmlvbEgwbjRhUXhTbENrc2NJVHJ0SjJoelRwNXBhazZLU3NxSkIlMkZPUWRqSGtQNGIwcW9DTmhpeiUyQmZqb1h2NWY2RCUyQmYxdyUzRCUzRA',
    '__CG': 'u%3A1013410594315477000%2Cs%3A1540379607%2Ct%3A1662648073222%2Cc%3A4%2Ck%3Akr.iherb.com%2F108%2F108%2F2485%2Cf%3A1%2Ci%3A1',
    '_uetsid': 'a42388102ccf11ed98d5751fe5162f62',
    '_uetvid': 'a423a2302ccf11ed9b9487245d8e689e',
    '_ga_SW3NJP516F': 'GS1.1.1662647184.16.1.1662648085.46.0.0',
    '_gali': 'product-summary-header',
}

en_headers = {
    'authority': 'kr.iherb.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'ko,ko-KR;q=0.9,en;q=0.8,en-US;q=0.7,ja;q=0.6',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'ih-experiment=eyJzcGVjaWFsc0xhbmRpbmdQYWdlIjp7IkNob3NlblZhcmlhbnQiOjAsIkVuZERhdGUiOiIyMDIzLTAxLTAxVDAwOjAwOjAwIn0sImF1dG9TaGlwQW5kU2F2ZU1lc3NhZ2UiOnsiQ2hvc2VuVmFyaWFudCI6MSwiRW5kRGF0ZSI6IjIwMjMtMDEtMDFUMDA6MDA6MDAifSwidWdjLXRhZ3MtZWN0amEiOnsiQ2hvc2VuVmFyaWFudCI6MCwiRW5kRGF0ZSI6IjIwMjMtMDktMDFUMDA6MDA6MDAifSwidWdjLWtleXdvcmQtZSI6eyJDaG9zZW5WYXJpYW50IjoxLCJFbmREYXRlIjoiMjAyMi0xMi0wMVQwMDowMDowMCJ9fQ==; ih-cc-pref=eyJmdW5jdGlvbmFsIjowLCJhbmFseXRpY3MiOjB9; transactionIds=undefined; ForceTrafficSplitType=A; dscid=d6d8c0f4-e115-471e-9b1c-706cbdf19796; _gid=GA1.2.1589508374.1662350583; _gcl_au=1.1.4489372.1662350584; _scid=179a3172-f951-4d1d-84cd-4b98b9de7db1; _fbp=fb.1.1662350584502.1272128199; _tt_enable_cookie=1; _ttp=6c39b938-4f36-40be-8801-c05d7bb8b488; _sctr=1|1662303600000; _pin_unauth=dWlkPVpHWXhabVk1Wm1VdFlqZG1NUzAwT1RFMExXSTVOekF0TmprMllXTXdNR1kwTVRJMQ; FPID=FPID2.2.J6G7x3zDM5nEePQxuBpuYmRfyqgsV7C5Z%2Fy3b8Fqtcc%3D.1662350582; _pxvid=6fe1d590-2d2a-11ed-a3e5-734d744f7a45; _wp_uid=2-a26c41fd33b3f7cc9980fbcb85fa9721-s1639705101.2228|windows_10|chrome-xm0ra6; ih-hp-vp=15; ih-hp-view=1; ihr-session-id1=aid=8293839f-2d09-4d21-a375-2df47f0bc4e5; ihr-ocid1=8293839f-2d09-4d21-a375-2df47f0bc4e5; __pxvid=9b359a63-2e87-11ed-9b88-0242ac120002; pxcts=7ea7532c-2ec1-11ed-a193-64586f717045; notice_behavior=implied,eu; FPAU=1.1.4489372.1662350584; _lr_uf_-enxord=a9bba88e-ef57-4e0a-9e2c-406f953b93ec; ihr-ds-vps=102552,82704,61864,64903,62118,95098,96984,96268,95852,97009; notice_preferences=3:; notice_gdpr_prefs=0,1,2,3:; cmapi_gtm_bl=; cmapi_cookie_privacy=permit 1,2,3,4; FPLC=1gGtIaeDg2JAxx13WR%2B1xxQ5jkqYiqxIS7k0ncRb%2Fo2WWhuht2Blyln8OB6nZQCgSoMY8cW8f0mGFOmVD0T1f0jDTUCW1U1Jq5GmXGvZY6SsZALUyjw1R6fTQ5Ezgg%3D%3D; _pxhd=hddCJozI8d5k8NehOnPnHP8zdhBNgQr8nxHUgAn1Ngwx2wIlEDGLF5s4e8CXgc3suT9qhq2l9JQ9fbdrK1/q7A; ih-preference=store=0&country=KR&language=en-US&currency=KRW; pref-saved=2; iher-pref1=storeid=0&sccode=KR&lan=en-US&scurcode=KRW&wp=2&lchg=1&ifv=1&accsave=0&bi=1; __cf_bm=2.T1OwoGbP3Br7kCao_G9p1ocui2CSKqs7ThSufPG7U-1662647185-0-AVbSeooPx7wht16PnlNkyZmE7mhA1xLcAtg8JjTDqJjlXBgDmjWtoB9BZQr36gi6Tk/3yTFlqf1375EuNGDYpOPA5C4XPnyh2xOrO10okFF0; ihr-temse=expires=08%20Sep%202022%2015:26:26Z; user-related={"HasNavigatedSite":{"timestamp":1662647186337}}; _lr_tabs_-enxord%2Fiherb={%22sessionID%22:0%2C%22recordingID%22:%225-199bb21e-58f8-4653-9349-e24f40b06441%22%2C%22lastActivity%22:1662647186895}; _lr_hb_-enxord%2Fiherb={%22heartbeat%22:1662647307053}; iher-vps=38964.46874.64903.62118.61864.99740.96229.96236.89210.64009.96231.96323.71031.77593.70316.101714.70317.84569.102552.82704.95098.96984.96268.95852.97009.106898.100012.99178.96982.106892; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; _pxff_tm=1; _ga=GA1.2.638579261.1662350582; _px3=77088c992f6d768f647414e1078fcc0c176abee9edab442e59b641fb77cae669:D8o18qocRr/V4qcVtQ7n1b/xn9OPiRwCJ/oisrYe2PTWh0qwJAD6opNfyOGeUYvb15dYDI4yCXmkm6sQhZ/YYA==:1000:zlvMFxCMRyx3YbNg5yR0wALlr5sfdKZ+71wEAk2C64e0EwccW5Ykapxj1+rqraESW/IvPPpBsE8vkzABiXZ2EytZq3u7FS47cD75SkWMiBNZrroYxZehFvE5Xa2PGATmds9zczNPNjTxsQ4p6Xyo3fXd+bO7SKjeivNMzQVb3tM/Lc/sa45UKWmoVuIC8FqHJLivYIrwXIXzdsDS2whnuw==; _dc_gtm_UA-229961-54=1; cto_bundle=RJ26MV9nekt3dEMxcUpqNCUyQnVzSkZrZWFpeGFxVHM1SmZ5VWV6NlBYSldIaU94SnUxWU8wQWl2TUtVUnFEWUNOa3ZVWFl6SXVGSFJPeEtDWkJIakNZSmlvbEgwbjRhUXhTbENrc2NJVHJ0SjJoelRwNXBhazZLU3NxSkIlMkZPUWRqSGtQNGIwcW9DTmhpeiUyQmZqb1h2NWY2RCUyQmYxdyUzRCUzRA; __CG=u%3A1013410594315477000%2Cs%3A1540379607%2Ct%3A1662648073222%2Cc%3A4%2Ck%3Akr.iherb.com%2F108%2F108%2F2485%2Cf%3A1%2Ci%3A1; _uetsid=a42388102ccf11ed98d5751fe5162f62; _uetvid=a423a2302ccf11ed9b9487245d8e689e; _ga_SW3NJP516F=GS1.1.1662647184.16.1.1662648085.46.0.0; _gali=product-summary-header',
    'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}


cookies = {
    'ih-experiment': 'eyJzcGVjaWFsc0xhbmRpbmdQYWdlIjp7IkNob3NlblZhcmlhbnQiOjAsIkVuZERhdGUiOiIyMDIzLTAxLTAxVDAwOjAwOjAwIn0sImF1dG9TaGlwQW5kU2F2ZU1lc3NhZ2UiOnsiQ2hvc2VuVmFyaWFudCI6MSwiRW5kRGF0ZSI6IjIwMjMtMDEtMDFUMDA6MDA6MDAifSwidWdjLXRhZ3MtZWN0amEiOnsiQ2hvc2VuVmFyaWFudCI6MCwiRW5kRGF0ZSI6IjIwMjMtMDktMDFUMDA6MDA6MDAifSwidWdjLWtleXdvcmQtZSI6eyJDaG9zZW5WYXJpYW50IjoxLCJFbmREYXRlIjoiMjAyMi0xMi0wMVQwMDowMDowMCJ9fQ==',
    'ih-cc-pref': 'eyJmdW5jdGlvbmFsIjowLCJhbmFseXRpY3MiOjB9',
    'transactionIds': 'undefined',
    'ForceTrafficSplitType': 'A',
    'dscid': 'd6d8c0f4-e115-471e-9b1c-706cbdf19796',
    '_gid': 'GA1.2.1589508374.1662350583',
    '_gcl_au': '1.1.4489372.1662350584',
    '_scid': '179a3172-f951-4d1d-84cd-4b98b9de7db1',
    '_fbp': 'fb.1.1662350584502.1272128199',
    '_tt_enable_cookie': '1',
    '_ttp': '6c39b938-4f36-40be-8801-c05d7bb8b488',
    '_sctr': '1|1662303600000',
    '_pin_unauth': 'dWlkPVpHWXhabVk1Wm1VdFlqZG1NUzAwT1RFMExXSTVOekF0TmprMllXTXdNR1kwTVRJMQ',
    'FPID': 'FPID2.2.J6G7x3zDM5nEePQxuBpuYmRfyqgsV7C5Z%2Fy3b8Fqtcc%3D.1662350582',
    '_pxvid': '6fe1d590-2d2a-11ed-a3e5-734d744f7a45',
    '_wp_uid': '2-a26c41fd33b3f7cc9980fbcb85fa9721-s1639705101.2228|windows_10|chrome-xm0ra6',
    'ih-hp-vp': '15',
    'ih-hp-view': '1',
    'ihr-session-id1': 'aid=8293839f-2d09-4d21-a375-2df47f0bc4e5',
    'ihr-ocid1': '8293839f-2d09-4d21-a375-2df47f0bc4e5',
    '__pxvid': '9b359a63-2e87-11ed-9b88-0242ac120002',
    'FPLC': 'saggmjBf416t6q8HWAZCbVjXV%2FqaOYBU1rXF8ULm3qQcZi%2BSkWhHaBcGC6z7DVHcFtASWwEmu1L2sxdnCzUZOSU6SLjPIRFKMC1lnhO38qg%2F2bIXe%2F1Hr3Bkuyiieg%3D%3D',
    'ih-preference': 'store=0&country=KR&language=ko-KR&currency=KRW',
    'iher-pref1': 'storeid=0&sccode=KR&lan=ko-KR&scurcode=KRW&wp=2&lchg=1&ifv=1&accsave=0&bi=1',
    'pxcts': '7ea7532c-2ec1-11ed-a193-64586f717045',
    'notice_behavior': 'implied,eu',
    'FPAU': '1.1.4489372.1662350584',
    '_pxhd': 'USNWQGRj4Ebg6iCh2vlGZVdJuy2XRW2SGPiy41I3Db3Dc8vV37DwLJ4mNGyRNyDCpIeTPxYFeTq8k/L8aHKFeA',
    '_lr_uf_-enxord': 'a9bba88e-ef57-4e0a-9e2c-406f953b93ec',
    'ihr-ds-vps': '102552,82704,61864,64903,62118,95098,96984,96268,95852,97009',
    'notice_preferences': '3:',
    'notice_gdpr_prefs': '0,1,2,3:',
    'cmapi_gtm_bl': '',
    'cmapi_cookie_privacy': 'permit 1,2,3,4',
    'ihr-temse': 'expires=08%20Oct%202022%2002:49:44Z',
    '__cf_bm': '7qooc0I_38iB1BIfdCWnzEYWMlTZ3WcPMZEIhb6UIUE-1662601785-0-Aa3HC7+Us47hCR1p2Ngk1mcetua9vhXv2w3zlKjl0QCbZ2wka2Dssq+OjbryZTyo15qmThu29XQ+E7k2NugzvWsvyWG13thqFCxrdHN6wDKe',
    'user-related': '{"HasNavigatedSite":{"timestamp":1662602176003}}',
    'iher-vps': '64009.64903.62118.96231.96229.96236.89210.96323.71031.77593.70316.101714.70317.84569.61864.102552.82704.95098.96984.96268.95852.97009.106898.100012.99178.96982.106892.113871.96321.108261',
    '_ga_SW3NJP516F': 'GS1.1.1662597996.12.1.1662602176.28.0.0',
    '_lr_tabs_-enxord%2Fiherb': '{%22sessionID%22:0%2C%22recordingID%22:%225-67b27d44-f8b5-458f-a934-7ea325450a2b%22%2C%22lastActivity%22:1662602177102}',
    '_ga': 'GA1.2.638579261.1662350582',
    'cto_bundle': 'LC3cBF9nekt3dEMxcUpqNCUyQnVzSkZrZWFpeFhCcEpkTUYyS1hIaTZJRTl5WkNwSzlhbUtCQ0tkcUJTbUwlMkJCd3ZxZkZDclE5OSUyRmZPTkM3ZEZQb1doVWNnTU13ZHJzczNQemhnZXhVS2ppRUJ1TE9IdjIlMkZYYk1zZWNVell2N1BzMVAxeE5ad1UxUTUxWldPeXgxY1pObTlwenc3USUzRCUzRA',
    '__CG': 'u%3A1013410594315477000%2Cs%3A308867702%2Ct%3A1662602180489%2Cc%3A44%2Ck%3Akr.iherb.com%2F109%2F109%2F2609%2Cf%3A1%2Ci%3A1',
    '_uetsid': 'a42388102ccf11ed98d5751fe5162f62',
    '_uetvid': 'a423a2302ccf11ed9b9487245d8e689e',
    '_lr_hb_-enxord%2Fiherb': '{%22heartbeat%22:1662602297876}',
    '_px3': '099231f0f969aad9be09c42755e5b891ddd8744a33c71d7e721d61bec15a1b2d:VrqfgdE0Ex94PGeu/9fCf5gIer+aFzRIXMlUyV38IousOepdbsWgjIrL5+13//vP9KC9qEJnPU0VuKdue4vAVw==:1000:QR7BIq+hCOE0WjfdxfHayR3fYViIr1AaXyn2XFA65ryxLcL34VBmO3JFLXpBqWvbL3nd86X4X8P1/LS2Q9CikEZlqCEktx0E+3ukMbU4k1pVpQ3zHwYbmpBd9Bo6LdHEeBp4xy/ZiORo1Zmm/AXBUCgnbDsNPViQBakZnS+6gTqMOsp0CbuHB95vSp7KKSaByvkNDpPv3aV6C0ooBhb0Ew==',
}

headers = {
    'authority': 'kr.iherb.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'ko,ko-KR;q=0.9,en;q=0.8,en-US;q=0.7,ja;q=0.6',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'ih-experiment=eyJzcGVjaWFsc0xhbmRpbmdQYWdlIjp7IkNob3NlblZhcmlhbnQiOjAsIkVuZERhdGUiOiIyMDIzLTAxLTAxVDAwOjAwOjAwIn0sImF1dG9TaGlwQW5kU2F2ZU1lc3NhZ2UiOnsiQ2hvc2VuVmFyaWFudCI6MSwiRW5kRGF0ZSI6IjIwMjMtMDEtMDFUMDA6MDA6MDAifSwidWdjLXRhZ3MtZWN0amEiOnsiQ2hvc2VuVmFyaWFudCI6MCwiRW5kRGF0ZSI6IjIwMjMtMDktMDFUMDA6MDA6MDAifSwidWdjLWtleXdvcmQtZSI6eyJDaG9zZW5WYXJpYW50IjoxLCJFbmREYXRlIjoiMjAyMi0xMi0wMVQwMDowMDowMCJ9fQ==; ih-cc-pref=eyJmdW5jdGlvbmFsIjowLCJhbmFseXRpY3MiOjB9; transactionIds=undefined; ForceTrafficSplitType=A; dscid=d6d8c0f4-e115-471e-9b1c-706cbdf19796; _gid=GA1.2.1589508374.1662350583; _gcl_au=1.1.4489372.1662350584; _scid=179a3172-f951-4d1d-84cd-4b98b9de7db1; _fbp=fb.1.1662350584502.1272128199; _tt_enable_cookie=1; _ttp=6c39b938-4f36-40be-8801-c05d7bb8b488; _sctr=1|1662303600000; _pin_unauth=dWlkPVpHWXhabVk1Wm1VdFlqZG1NUzAwT1RFMExXSTVOekF0TmprMllXTXdNR1kwTVRJMQ; FPID=FPID2.2.J6G7x3zDM5nEePQxuBpuYmRfyqgsV7C5Z%2Fy3b8Fqtcc%3D.1662350582; _pxvid=6fe1d590-2d2a-11ed-a3e5-734d744f7a45; _wp_uid=2-a26c41fd33b3f7cc9980fbcb85fa9721-s1639705101.2228|windows_10|chrome-xm0ra6; ih-hp-vp=15; ih-hp-view=1; ihr-session-id1=aid=8293839f-2d09-4d21-a375-2df47f0bc4e5; ihr-ocid1=8293839f-2d09-4d21-a375-2df47f0bc4e5; __pxvid=9b359a63-2e87-11ed-9b88-0242ac120002; FPLC=saggmjBf416t6q8HWAZCbVjXV%2FqaOYBU1rXF8ULm3qQcZi%2BSkWhHaBcGC6z7DVHcFtASWwEmu1L2sxdnCzUZOSU6SLjPIRFKMC1lnhO38qg%2F2bIXe%2F1Hr3Bkuyiieg%3D%3D; ih-preference=store=0&country=KR&language=ko-KR&currency=KRW; iher-pref1=storeid=0&sccode=KR&lan=ko-KR&scurcode=KRW&wp=2&lchg=1&ifv=1&accsave=0&bi=1; pxcts=7ea7532c-2ec1-11ed-a193-64586f717045; notice_behavior=implied,eu; FPAU=1.1.4489372.1662350584; _pxhd=USNWQGRj4Ebg6iCh2vlGZVdJuy2XRW2SGPiy41I3Db3Dc8vV37DwLJ4mNGyRNyDCpIeTPxYFeTq8k/L8aHKFeA; _lr_uf_-enxord=a9bba88e-ef57-4e0a-9e2c-406f953b93ec; ihr-ds-vps=102552,82704,61864,64903,62118,95098,96984,96268,95852,97009; notice_preferences=3:; notice_gdpr_prefs=0,1,2,3:; cmapi_gtm_bl=; cmapi_cookie_privacy=permit 1,2,3,4; ihr-temse=expires=08%20Sep%202022%2002:49:44Z; __cf_bm=7qooc0I_38iB1BIfdCWnzEYWMlTZ3WcPMZEIhb6UIUE-1662601785-0-Aa3HC7+Us47hCR1p2Ngk1mcetua9vhXv2w3zlKjl0QCbZ2wka2Dssq+OjbryZTyo15qmThu29XQ+E7k2NugzvWsvyWG13thqFCxrdHN6wDKe; user-related={"HasNavigatedSite":{"timestamp":1662602176003}}; iher-vps=64009.64903.62118.96231.96229.96236.89210.96323.71031.77593.70316.101714.70317.84569.61864.102552.82704.95098.96984.96268.95852.97009.106898.100012.99178.96982.106892.113871.96321.108261; _ga_SW3NJP516F=GS1.1.1662597996.12.1.1662602176.28.0.0; _lr_tabs_-enxord%2Fiherb={%22sessionID%22:0%2C%22recordingID%22:%225-67b27d44-f8b5-458f-a934-7ea325450a2b%22%2C%22lastActivity%22:1662602177102}; _ga=GA1.2.638579261.1662350582; cto_bundle=LC3cBF9nekt3dEMxcUpqNCUyQnVzSkZrZWFpeFhCcEpkTUYyS1hIaTZJRTl5WkNwSzlhbUtCQ0tkcUJTbUwlMkJCd3ZxZkZDclE5OSUyRmZPTkM3ZEZQb1doVWNnTU13ZHJzczNQemhnZXhVS2ppRUJ1TE9IdjIlMkZYYk1zZWNVell2N1BzMVAxeE5ad1UxUTUxWldPeXgxY1pObTlwenc3USUzRCUzRA; __CG=u%3A1013410594315477000%2Cs%3A308867702%2Ct%3A1662602180489%2Cc%3A44%2Ck%3Akr.iherb.com%2F109%2F109%2F2609%2Cf%3A1%2Ci%3A1; _uetsid=a42388102ccf11ed98d5751fe5162f62; _uetvid=a423a2302ccf11ed9b9487245d8e689e; _lr_hb_-enxord%2Fiherb={%22heartbeat%22:1662602297876}; _px3=099231f0f969aad9be09c42755e5b891ddd8744a33c71d7e721d61bec15a1b2d:VrqfgdE0Ex94PGeu/9fCf5gIer+aFzRIXMlUyV38IousOepdbsWgjIrL5+13//vP9KC9qEJnPU0VuKdue4vAVw==:1000:QR7BIq+hCOE0WjfdxfHayR3fYViIr1AaXyn2XFA65ryxLcL34VBmO3JFLXpBqWvbL3nd86X4X8P1/LS2Q9CikEZlqCEktx0E+3ukMbU4k1pVpQ3zHwYbmpBd9Bo6LdHEeBp4xy/ZiORo1Zmm/AXBUCgnbDsNPViQBakZnS+6gTqMOsp0CbuHB95vSp7KKSaByvkNDpPv3aV6C0ooBhb0Ew==',
    'referer': 'https://kr.iherb.com/pr/california-gold-nutrition-collagenup-hydrolyzed-marine-collagen-peptides-with-hyaluronic-acid-and-vitamin-c-unflavored-7-26-oz-206-g/64903',
    'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
}

import chromedriver_autoinstaller
import httpx, asyncio
import sys
import traceback
import requests
from itertools import islice
from googletrans import Translator  
import requests

translator = Translator()

py_ver = int(f"{sys.version_info.major}{sys.version_info.minor}")
if py_ver > 37 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logging.basicConfig(handlers=[logging.FileHandler(filename="log_records.txt", 
                                                 encoding='utf-8', mode='a+'),
                              logging.StreamHandler()],
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt="%F %A %T", 
                    level=logging.INFO)

# Check if chrome driver is installed or not
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
driver_path = f'./{chrome_ver}/chromedriver.exe'
if os.path.exists(driver_path):
    print(f"chrom driver is insatlled: {driver_path}")
else:
    print(f"install the chrome driver(ver: {chrome_ver})")
    chromedriver_autoinstaller.install(True)

class NutrientInfo:
    iherb_id: str
    nutrient: str 
    nutrient_kr: str
    amount: str 
    unit: str
    
    def get_data(self):
        return self.__dict__

class Product:
    iherb_id: str
    link: str
    product_name: str
    take_en: str
    take_kr: str
    serving_size: str
    count: str
    original_price: str
    sale_price: str
    img: str
    nutrient_info: List[NutrientInfo]

    def __str__(self):
        return str(self.__dict__.items())


    def get_data_for_excel_type_1(self):
        tmp = dict(self.__dict__)
        tmp.pop("nutrient_info")
        return tmp

    def get_data_for_excel_type_2(self):
        tmp = dict(self.__dict__)
        n_infos = tmp.pop("nutrient_info")
        n_infos = [i.get_data() for i in n_infos]            
        return n_infos

class ExcelExporter:
    def __init__(self, data: List[Dict[str, str]], file_name: str ) -> None:
        self.data = data
        self.workbook = xlsxwriter.Workbook(file_name)
        self.worksheet = self.workbook.add_worksheet('')

    def export_excel(self):
        self._set_columns()

        for row_idx, product in enumerate(self.data):
            for key, value in product.items():
                col_idx = self.col_data[key]
                self.worksheet.write(row_idx+1, col_idx, value)

        self.workbook.close()

    def _set_columns(self):
        cols_len = len(list(self.data[0].keys()))
        # print(self.data[0].keys())
        if cols_len == 10: # type1
            columns = ["iherb_id", "link", "product_name", "take_en", "take_kr", "serving_size", "count", "original_price", "sale_price", "img"]
        else: # type2
            columns = ["iherb_id", "nutrient", "nutrient_kr", "amount", "unit"]
        
        self.col_data = {}
        for col_idx, col in enumerate(columns):
            self.worksheet.write(0, col_idx, col)
            self.col_data[col] = col_idx     

def parse_product_detail_kr_data(kr_dict:dict) -> Dict:
    result_data = {}
    result_data["original_price"] = kr_dict["listPrice"].replace("₩", "").replace(",", "")

    result_data["sale_price"] = ""
    if kr_dict["listPrice"] != kr_dict["discountPrice"]:
        result_data["sale_price"] = kr_dict["discountPrice"].replace("₩", "").replace(",","")

    result_data["iherb_id"] = kr_dict["id"]
    soup = BeautifulSoup(kr_dict["suggestedUse"], 'html.parser')
    result_data["take_kr"] = soup.text 

    soup = BeautifulSoup(kr_dict["supplementFacts"], 'html.parser')

    rows = []
    table = soup.find("table")

    if table is not None:
        rows = table.find_all("tr")

    nutrient_row_start = False
    nutrient_list = []
    # print("len rows.....")
    # print(len(rows))
    for r in rows:
        if nutrient_row_start:
            tds = r.find_all("td")
            if len(tds) == 3:
                # n_info = {}
                nutrient, amount_with_unit, _ = tds
                # amount_with_unit = amount_with_unit.text
                nutrient = nutrient.text
                # print(nutrient)
                if nutrient.strip() != "":
                #     splitted_data = amount_with_unit.split(" ")
                #     if len(splitted_data) == 2:
                #         amount, unit = splitted_data
                #     elif len(splitted_data) == 1:
                #         # print(splitted_data)
                #         amount = splitted_data[0]
                #         unit = ""
                #     else:
                #         amount = splitted_data[0]
                #         unit = "".join(splitted_data[1:])
                        
                    # n_info = {
                    #     "nutrient": nutrient,
                    #     "iherb_id": en_dict["id"],
                    #     "nutrient_kr": translator.translate(nutrient, dest="ko").text,
                    #     "amount": amount,
                    #     "unit": unit
                    # }
                    # time.sleep(0.5)

                    nutrient_list.append(nutrient)

        elif "영양 성분 정보" in r.text:
            nutrient_row_start = True

    result_data["nutrient_list"] = nutrient_list
    
    return result_data

def parse_product_detail_en_data(en_dict: dict) -> Dict:
    result_data = {}
    result_data["product_name"] = en_dict["displayName"]

    result_data["count"] = en_dict["packageQuantity"].split(" ")[0]
    if result_data["count"] == "Approx":
        result_data["count"] = en_dict["packageQuantity"].split(" ")[1]

    result_data["link"] = en_dict["productUrl"]
    result_data["img"] = preprocess_img_path(en_dict["productImageUrl"])

    soup = BeautifulSoup(en_dict["suggestedUse"], 'html.parser')
    result_data["take_en"] = soup.text


    soup = BeautifulSoup(en_dict["supplementFacts"], 'html.parser')
    nutrient_row_start = False
    serving_size = None
  
    rows = []
    table = soup.find("table")

    if table is not None:
        rows = table.find_all("tr")

    try:
        serving_size = rows[1].text.replace("Serving Size: ", "").strip()
        serving_size = re.findall(r'\d+', serving_size)[0]
    except:
        logging.info("no serving size")
        # print("no serving size")

    result_data["serving_size"] = serving_size
    nutrient_list = []
    for r in rows:
        if nutrient_row_start:
            tds = r.find_all("td")
            if len(tds) == 3:
                n_info = {}
                nutrient, amount_with_unit, _ = tds
                amount_with_unit = amount_with_unit.text
                nutrient = nutrient.text
                # print(nutrient)
                if nutrient.strip() != "":
                    splitted_data = amount_with_unit.split(" ")
                    if len(splitted_data) == 2:
                        amount, unit = splitted_data
                    elif len(splitted_data) == 1:
                        # print(splitted_data)
                        amount = splitted_data[0]
                        unit = ""
                    else:
                        amount = splitted_data[0]
                        unit = "".join(splitted_data[1:])
                        
                    n_info = {
                        "nutrient": nutrient,
                        "iherb_id": en_dict["id"],
                        # "nutrient_kr": translator.translate(nutrient, dest="ko").text,
                        "amount": amount,
                        "unit": unit
                    }
                    time.sleep(0.3)

                    nutrient_list.append(n_info)

        elif "Supplement Facts" in r.text:
            nutrient_row_start = True

    result_data["nutrient_list"] = nutrient_list
    
    return result_data

def parse_product_detail_data(product_id: str, kr_dict: dict, en_dict: dict) -> Dict:
    logging.info(f"Parsing product id: {product_id}")
    kr_data = None
    en_data = None
    try:
        kr_data = parse_product_detail_kr_data(kr_dict)
        logging.info(f"Parsing korean data completed for product id {product_id}")
    except:
        logging.error(f"Error While Parsing product id {product_id} \n {traceback.format_exc()}")

    try:
        en_data = parse_product_detail_en_data(en_dict)
        logging.info(f"Parsing English data completed for product id {product_id}")
    except:
        logging.error(f"Error While Parsing product id {product_id} \n {traceback.format_exc()}")

    
    if kr_data is not None and en_data is not None:
        kr_nutrient_info = kr_data.pop("nutrient_list")
        en_nutrient_info = en_data["nutrient_list"]
        if len(kr_nutrient_info) == len(en_data["nutrient_list"]):
            for idx, info in enumerate(kr_nutrient_info):
                en_nutrient_info[idx]['nutrient_kr'] = info
        else:
            logging.info(f"kr_nutrient_info len {len(kr_nutrient_info)} and en_nutrient_info len {len(en_nutrient_info)} is not equal")
            logging.info("using google translate apis instead...")
            for idx, nutrient in enumerate(en_nutrient_info):
                try:
                    nutrient_ko = translator.translate(nutrient["nutrient"], dest="ko").text
                    en_nutrient_info[idx]["nutrient_kr"] = nutrient_ko
                    time.sleep(0.3)
                except:
                    logging.error("Error while translating..")
                    en_nutrient_info[idx]["nutrient_kr"] = "FAILED"       

        product_data = dict(kr_data, **en_data)
        return product_data
    else:
        logging.error("Error While Parsing product data")
        return None

def parse_raw(product_raw_data: List):
    product_data = []
    failed_list = []
    for raw_data in product_raw_data:
        p_id = list(raw_data.keys())[0]
        en_dict = list(raw_data.values())[0][0]
        kr_dict = list(raw_data.values())[0][1]

        data = parse_product_detail_data(p_id, kr_dict=kr_dict, en_dict=en_dict)

        if data is None:
            failed_list.append(p_id)
        else:
            product_data.append(data)

    return product_data, failed_list

idx = 1
async def get_product(results: List, p_id: int, failed_list: List):
    async with httpx.AsyncClient(timeout=15.0, verify=False) as client:

        en_url = f"https://catalog.app.iherb.com/product/{p_id}"
        img_and_product_url = f"http://52.82.86.146/ugc/api/product/{p_id}"
        ko_url = f"https://catalog.app.iherb.com/product/{p_id}"


        timeout = httpx.Timeout(10.0, read_timeout=None)
        product_data = {
            p_id: []
        }
        res_en = await client.get(en_url, timeout=timeout, headers=en_headers, cookies=en_cookies)
        res_en2 = await client.get(img_and_product_url, timeout=timeout, headers=en_headers, cookies=en_cookies)
        res_kr = await client.get(ko_url, timeout=timeout, headers=headers, cookies=cookies)
        global idx 

        logging.info(f"{idx}| EN Request: {res_en.status_code}")
        logging.info(f"{idx}| EN Request: {res_en2.status_code}")
        logging.info(f"{idx}| KR Request: {res_kr.status_code}")
        
        if res_en.status_code != 200:
            logging.error(f"EN Request for product {p_id} failed with status code {res_en.status_code}")
            print(f"EN Request for product {p_id} failed with status code {res_en.status_code}")
            failed_list.append(p_id)
            return 
        elif res_kr.status_code != 200:
            logging.error(f"KR Request for product {p_id} failed with status code {res_kr.status_code}")
            print(f"KR Request for product {p_id} failed with status code {res_kr.status_code}")
            failed_list.append(p_id)
            return 

        res_en = dict(res_en.json(), **res_en2.json())

        product_data[p_id].append(res_en)
        product_data[p_id].append(res_kr.json())
        results.append(product_data)
        idx += 1
        time.sleep(random.randint(1,3))

async def scrape(product_ids: List):
    tasks = []
    results = []
    failed_list = []
    for p_id in product_ids:
        tasks.append(get_product(results, p_id, failed_list))

    await asyncio.gather(*tasks)
    return results, failed_list

def scrape_products(product_ids: List):
    return asyncio.run(scrape(product_ids))

def get_total_pages(url: str):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    total_product_num = soup.find(class_="sub-header-title display-items").text
    total_product_num = total_product_num.strip().split(" ")[0]
    logging.info(f"total products num: {total_product_num}")
    product_per_page = 24
    total_pages = int(total_product_num) // product_per_page
    logging.info(f"total pages: {total_pages}")
    return total_pages

def get_all_product_ids(page_num: str, category: str) -> List[str]:
    url = f"https://kr.iherb.com/c/{category}?p={page_num}"
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    p_table = soup.find(class_="products clearfix")
    products = p_table.find_all(class_="product ga-product")
    product_id_arr = []
    for p in products:
        p_id = p.get("id").replace("pid_", "")
        product_id_arr.append(p_id)

    return product_id_arr

def save_product_ids(category="herbs"):
    url = f"https://kr.iherb.com/c/{category}"
    logging.info(f"category: {category}")
    total_pages = get_total_pages(url)
    total_product_id_arr = []
    
    # 디렉토리 생성 
    os.makedirs(f'./{category}', exist_ok=True)

    for i in range(1,total_pages+2):
        logging.info(f"scarping page {str(i)}")
        product_id_arr = get_all_product_ids(str(i), category)
        total_product_id_arr.extend(product_id_arr)
        # time.sleep(random.randint(1, 3))

        with open(f"./{category}/{category}_upto_page_{str(i)}.txt", "w") as f:
            f.write('\n'.join(total_product_id_arr))

    with open(f"./{category}/{category}_total.txt", "w") as f:
            f.write('\n'.join(total_product_id_arr))

def download_image(url: str, download_path):
    r = requests.get(url)
    with open(download_path, 'wb') as outfile:
        outfile.write(r.content)
    logging.info(f"image download success: {url}")

def get_nutrient_info_from_product_data(product_data: List):
    n_total_list = []
    for data in product_data:
        n_list = data.pop("nutrient_list")

        n_total_list.extend(n_list)

    return n_total_list

def get_data_without_nutrient_info(product_data: List):
    data_without_nutrient_list = []
    for data in product_data:
        tmp = dict(data)
        tmp.pop("nutrient_list")
        data_without_nutrient_list.append(tmp)

    return data_without_nutrient_list

def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())

def preprocess_img_path(img):
    cloudflare_img_storage = "https://cloudinary.images-iherb.com/image/upload/f_auto,q_auto:eco/images"
    
    def repl_last(s, sub, repl):
        index = s.rfind(sub)
        if index == -1:
            return s
        return s[:index] + repl + s[index+len(sub):]
    cf_img = img.replace("https://s3.images-iherb.com", cloudflare_img_storage)
    cf_img = repl_last(cf_img, 'c', 'l')
    return cf_img

def process_type_2(file_path: str):
    logging.info("processing function 2")

    timestr = time.strftime("%Y%m%d-%H%M%S")
    dir_path = f"./{timestr}/"
    os.makedirs(dir_path, exist_ok=True)

    logging.info(f"opening file {file_path}")

    with open(file_path, "r") as f:
        product_ids = f.readlines()
        product_ids = [p_id.replace("\n","") for p_id in product_ids]

    logging.info(f"trying to scrape total {len(product_ids)} products")

    if len(product_ids) > 200:
        product_ids_chunck = chunk(product_ids, 200)
        results = []
        failed_list = []
        for product_ids in product_ids_chunck:
            partial_results, partial_failed_list = scrape_products(product_ids=product_ids)
            results.extend(partial_results)
            failed_list.extend(partial_failed_list)
    else:
        results, failed_list = scrape_products(product_ids=product_ids)

    product_data, failed_list2 = parse_raw(results)

    failed_list.extend(failed_list2)


    logging.info(f"{len(product_data)}/{len(product_ids)} scraping and parsing success")

    data_for_excel_type1 = get_data_without_nutrient_info(product_data)
    data_for_excel_type2 = get_nutrient_info_from_product_data(product_data)

    logging.info(f"Exporting Excel File type1.xlsx...")
    # print(data_for_excel_type1)
    exp = ExcelExporter(data_for_excel_type1, dir_path+"type1.xlsx")
    exp.export_excel()

    logging.info(f"Export Completed.")

    if len(data_for_excel_type2) == 0:
        logging.info(f"No nutrients found, not creating type2.xlsx")
    else:
        logging.info(f"Exporting Excel File type2.xlsx...")
        exp = ExcelExporter(data_for_excel_type2, dir_path+"type2.xlsx")
        exp.export_excel()
        logging.info(f"Export Completed.")

    
    img_dir_path = f"./{timestr}/imgs/"
    os.makedirs(img_dir_path, exist_ok=True)
    for data in product_data:
        img = data["img"]
        p_id = data["iherb_id"]
        logging.info(f"Downloading image for product {p_id}")
        try:
            download_image(img, img_dir_path+f"{p_id}.jpg")
        except:
            logging.error(f"Failed to download image {p_id}")
            failed_list.append(p_id)

        time.sleep(random.randint(1,2))

    logging.info("writing scrape failed products to fail.txt...")
    
    with open(dir_path+"fail.txt", "w") as f:
        f.writelines(s + '\n' for s in failed_list)

    logging.info("scraping process completed.")

def process_only_images(file_path: str):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    dir_path = f"./{timestr}/"
    os.makedirs(dir_path, exist_ok=True)

    logging.info(f"opening file {file_path}")

    with open(file_path, "r") as f:
        product_ids = f.readlines()
        product_ids = [p_id.replace("\n","") for p_id in product_ids]

    logging.info(f"trying to scrape total {len(product_ids)} products")
    img_dir_path = f"./{timestr}/imgs/"
    os.makedirs(img_dir_path, exist_ok=True)
    failed_list = []

    for p_id in product_ids:
        try:
            img_and_product_url = f"http://52.82.86.146/ugc/api/product/{p_id}"
            res = requests.get(img_and_product_url)
            result = res.json()
            img = preprocess_img_path(result["productImageUrl"])
            logging.info(f"Downloading img files for product {p_id}")
            download_image(img, img_dir_path+f"{p_id}.jpg")
        except:
            logging.error(f"download failed for {p_id}")
            failed_list.append(p_id)
    
    with open(dir_path+"fail.txt", "w") as f:
        f.writelines(s + '\n' for s in failed_list)

def remove_duplicates(p_ids1, p_ids2):
    logging.info("removing duplicates")
    logging.info(f"p_ids1 len: {len(p_ids1)} p_ids2 len: {len(p_ids2)}")
    logging.info(f"p_ids1 + p_ids2 len {len(p_ids1)+len(p_ids2)}")
    arr = list(set(p_ids2) - set(p_ids1))
    logging.info(f"duplicated removed arr len {len(arr)}")
    return arr

if __name__ == "__main__":
    print("IHerb Product Scraper v1.0.0")
    while True:
        answer = input("상품 ID 수집하시려면 '1', 상품 스크랩을 시작하시려면 '2' 를 입력하시고 엔터를 눌러주세요: ")

        if answer == "1":
            logging.info("상품 ID 수집을 시작합니다.")
            logging.info("ID 수집 카테고리: herbs | supplements")
            save_product_ids("herbs")
            save_product_ids("supplements")
            herb_path = "./herbs/herbs_total.txt"
            supplements_path = "./supplements/supplements_total.txt"

            logging.info(f"opening herb_path ({herb_path})")

            try:
                with open(herb_path, "r") as f:
                    p_ids1 = f.readlines()
                    p_ids1 = [p_id.replace("\n","") for p_id in p_ids1]
            except:
                logging.error(f"{herb_path} 가 없습니다. 파일을 만들어 주세요!")
                continue


            logging.info(f"opening supplements_path ({supplements_path})")
            try:
                with open(supplements_path, "r") as f:
                    p_ids2 = f.readlines()
                    p_ids2 = [p_id.replace("\n","") for p_id in p_ids2]
            except:
                logging.error(f"{supplements_path} 가 없습니다. 파일을 만들어 주세요!")
                continue

            arr = remove_duplicates(p_ids1, p_ids2)

            logging.info(f"saving duplicated removed arr to products.txt...")
            
            with open("products.txt", "w") as f:
                f.writelines(s + '\n' for s in arr)
        
        elif answer == "2":
            import os.path
            fname = "products.txt"
            if os.path.isfile(fname):
                logging.info("상품 스크랩을 시작합니다. products.txt")
                process_type_2(fname)
            else:
                logging.error("products.txt 를 찾을 수 없습니다. 실행 파일과 같은 폴더에 products.txt 파일을 만들어 주세요!")

        else:
            logging.info("'1' 혹은 '2' 를 입력해주세요")
        

