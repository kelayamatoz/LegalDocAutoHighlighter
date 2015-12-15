'''
This script provides parsing methods for docs in html format.
Every parser should provides three output lists:
h1List: most important tags
h2List: second most important tagts
emphList: contents that are emphasized
textList: actual texts.

The first three lists are used as topics within a document.
'''

import os
import urllib
import re
from bs4 import BeautifulSoup, SoupStrainer

# websites
targetAtlassianAddr = 'https://www.atlassian.com/legal/'
targetGithubAddr = 'https://help.github.com/categories/site-policy/'

# html folder
targetAtlassianDirHTML = 'atlassianLegalDocDir'
targetGithubDirHTML = 'githubLegalDocDir'

# parsed folder
targetAtlassianDirParsed = 'atlassianLegalDocDirParsed'
targetGithubDirParsed = 'githubLegalDirParsed'


# regex for removing section numbers
re_subsSecNum = re.compile('.*([0-9][0-9]\.[0-9]+)', re.UNICODE)
re_secNum = re.compile(r'\d+', re.UNICODE)


# return a list of possible key phrases and a list of extracted texts.
def extractTextInfo(targetDir, htmlDocName=None, htmlObject=None, agreementSource='atlassian'):
    def getMeaningfulDivLists(divSp):
        divList = divSp.findAll('div')
        if len(divList) == 0: return []
        maxLen = max(len(divBlk) for divBlk in divList)
        # seems that 20% works well...
        return [divBlk for divBlk in divList if len(divBlk) >= 0.2 * maxLen]

    def extractInfo(sp):
        divLists = getMeaningfulDivLists(sp)
        emphResult = list()
        h1Result = list()
        h2Result = list()
        textResult = list()
        for div in divLists:
            # separate a div into ['section name' : section text]
            # later we want to assign section name with different texts... we may want to build centroids closer to
            # each section
            # we also want to remove the most frequent words... can check it later

            # <p> is used to store info
            def getTagList():
                tagNames = ['strong', 'h1', 'h2', 'p']
                result = list()
                for name in tagNames:
                    result.append([info.text for info in div.findAll(name)])
                return result
            emphList, h1List, h2List, textList = getTagList()
            emphResult.append(emphList)
            h1Result.append(h1List)
            h2Result.append(h2List)
            textResult.append(textList)
        return emphResult, h1Result, h2Result, textResult

    if htmlDocName:
        with open(htmlDocName, 'r') as f:
            sp = BeautifulSoup(f, 'html.parser')
    else:
        sp = BeautifulSoup(htmlObject, 'html.parser')
    if agreementSource == 'atlassian' or 'github':
        # atlassian stores the major content of their contract in div classes
        # if a div block is as long as 3/4 of the longest text, then consider that this one may have enough information
        # notice that this only applies to the case of agreements by atlassian.

        return extractInfo(sp)
        # This block of code finds the section numbers.
        # sectionName = section.find('strong').contents[0].strip()
        # print sectionName
        # sectionNumGroup = re_secNum.search(sectionName) #.group(0)
        # subSectionNumGroup = re_subsSecNum.search(sectionName) #.group(1)
        # subSectionNum = None
        # sectionNum = None
        # if subSectionNumGroup:
        #     subSectionNum = subSectionNumGroup.group(1)
        # if sectionNumGroup:
        #     sectionNum = sectionNumGroup.group(0)
        # sectionName = sectionName.partition(' ')[2][:-1]
        # sectionContentLists = [info.extract() for info in section.findAll('strong')]

    else:
        raise Exception('unknown source!')


def getTrainingText(targetDirHTML, targetAddr, sourceType='atlassian'):
    if not os.path.exists(targetDirHTML):
        os.makedirs(targetDirHTML)
    hname = urllib.urlopen(targetAddr).read()
    if sourceType == 'atlassian':
        with open(targetAtlassianDirHTML + '/Eula.html', 'w+') as fname:
            fname.write(hname)
        for lname in BeautifulSoup(hname, 'html.parser', parse_only=SoupStrainer('a')):
            if lname.has_attr('href'):
                if '/legal/' in lname['href']:
                    loadAddrName = targetAddr + lname['href'][len('/legal/'):]
                    loadName = targetDirHTML + '/' + loadAddrName.split('/')[-1] + '.html'
                    with open(loadName, 'w+') as fname:
                        tmpHtmlname = urllib.urlopen(loadAddrName).read()
                        fname.write(tmpHtmlname)
    elif sourceType == 'github':
        with open(targetGithubDirHTML + '/Eula.html', 'w+') as fname:
            fname.write(hname)
            for lname in BeautifulSoup(hname, 'html.parser', parse_only=SoupStrainer('a')):
                if lname.has_attr('href'):
                    if '/articles/' in lname['href']:
                        loadAddrName = 'https://help.github.com/articles/' + lname['href'][len('/articles/'):]
                        print loadAddrName
                        loadName = targetDirHTML + '/' + loadAddrName.split('/')[-1] + '.html'
                        with open(loadName, 'w+') as fname:
                            tmpHtmlname = urllib.urlopen(loadAddrName).read()
                            fname.write(tmpHtmlname)
    else:
        raise Exception('unknown source!')



if __name__ == '__main__':
    # Atlassian has two dirs. /end-user-agreement for the EULA, /legal for the other files
    getTrainingText(targetAtlassianDirHTML, targetAtlassianAddr)
    emph, h1, h2, text = extractTextInfo(targetAtlassianDirParsed, htmlDocName=targetAtlassianDirHTML + '/Eula.html')

    # example of using github parser
    getTrainingText(targetGithubDirHTML, targetGithubAddr, sourceType='github')
    emph, h1, h2, text = extractTextInfo(targetAtlassianDirParsed, agreementSource='github', htmlDocName=targetGithubDirHTML + '/github-registered-developer-agreement.html')