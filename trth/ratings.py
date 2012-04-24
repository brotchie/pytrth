"""
Extracts ratings information from the SpeedGuide.

"""

import os
import re
import logging

import api

log = logging.getLogger(__name__)

AUSTRALIAN_RATING_RICS = ['RRS%i' % (i,) for i in range(8188, 8194)]
COMPANY_RIC_EXTRACTOR_RE = re.compile(r'\.<(RRS\d+)>')

def main():
    trth = api.TRTHApi()
    trth.setup()

    companyrics = set()
    for pageric in AUSTRALIAN_RATING_RICS:
        log.info('Processing ratings page %s.' % (pageric,))
        page = trth.GetPage(pageric)
        companyrics.update(COMPANY_RIC_EXTRACTOR_RE.findall(page))
    companyrics = list(companyrics)
    companyrics.sort()

    for companyric in companyrics:
        log.info('Fetching ratings page for %s.' % (companyric,))
        destination = os.path.join('/var/tmp/ratings', '%s.txt' % (companyric,))
        file(destination, 'w+').write(trth.GetPage(companyric).encode('utf8'))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
