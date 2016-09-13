#!/usr/bin/env python3

from html.parser import HTMLParser
from re import  sub, findall

from datetime import date
# "magic": you have to input the date of the first day manually
d = date(2016, 9, 12) 

def parseWeek(strWeek):
    # "1-3,5,7-9" => [1, 2, 3, 5, 7, 8, 9]
    lstNumber = findall('\d+(?:-\d+)?', strWeek) # number | number-number
    lstReturn = list()
    for strCurr in lstNumber:
        lstSplit = strCurr.split('-')
        if len(lstSplit) == 2:
            # number-number
            intStart, intEnd = int(lstSplit[0]), int(lstSplit[1])
            for i in range(intStart, intEnd + 1):
                lstReturn.append(i)
        else:
            # number
            lstReturn.append(int(lstSplit[0]))
    return lstReturn


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        self.td = (tag == 'td')

    def handle_endtag(self, tag):
        if tag == 'tr':
            if len(self.line) != 0:
                self.table.append(self.line[:])
                self.line.clear()
        elif tag == 'td':
            self.td = False

    def handle_data(self, data):
        if self.td:
            self.line.append(sub('\s', '', data))
        

from sys import argv
argv.pop(0) # remove the filename of this script
if len(argv) == 1:
    strFileName = argv.pop(0) # the path of the input html table

fileHtml = open(strFileName, 'r', encoding='utf-8')
strHtml = fileHtml.read()
fileHtml.close() 
parser = MyHTMLParser()
# ugly attribute set
setattr(parser, 'td', False)
setattr(parser, 'line', list())
setattr(parser, 'table', list())

parser.feed(strHtml)
lstParse = parser.table[:] # each html row makes a row in lstParse
lstParse.pop(0) # remove the table head (the first line of the table), with no course information
lstTemp = list() # make a new temp list to copy the processed course data
intMaxWeek = 1
for lstCourse in lstParse:
    if len(lstCourse) == 18:
        # full info
        strName = lstCourse[2]
        lstTemp.append([strName])
    strRoom = '-'.join(lstCourse[-3:]) # join the places together as a string
    lstWeek = parseWeek(lstCourse[-7]) # parse the "week-string" to get the list of weeks
    intMaxWeek = max(intMaxWeek, max(lstWeek)) # update the max week number
    intDay = int(lstCourse[-6])
    intStart = int(lstCourse[-5])
    intLength = int(lstCourse[-4])
    # add the new "mode" to the current course
    lstTemp[-1].append([strRoom, lstWeek[:], intDay, intStart, intLength]) 

# swap the contents of the temp list and the source list
del lstParse
lstParse = lstTemp
del lstTemp

# build the calendar list: each week makes a sub-table, each week made up of each day
lstCalendar = list()
for intWeek in range(intMaxWeek):
    lstCalendar.append([[],[],[],[],[],[],[]])
# the course of each day will be placed into the list of that day

for lstCourse in lstParse:
    strName = lstCourse.pop(0)
    for lstMode in lstCourse:
        lstWeek = lstMode.pop(1)
        strRoom = lstMode[0]
        intDay, intStart, intLength = lstMode[-3:]
        for intWeek in lstWeek:
            lstCalendar[intWeek - 1][intDay - 1].append([strName, strRoom, intStart, intLength])
            # python list index starts from 0： "-1" is a must

# import the template
fileTemplate = open('template.svg', 'r', encoding='utf-8')
strTemplate = fileTemplate.read()
fileTemplate.close()
# replace the '<!--TEMPLATE_REPLACE-->' with the format symbol, where to plug in the lecture contents
strTemplate = strTemplate.replace('<!--TEMPLATE_REPLACE-->', '{}')

strRect = '<rect width="{}" height="{}" x="{}" y="{}" style="fill:rgb(255,255,255);stroke-width:2;stroke:rgb(0,0,0)"/>'
strBold = '<text style="font-weight:bold;" font-size="{}" text-anchor="middle" x="{}" y="{}">{}</text>'
strText = '<text font-size="{}" text-anchor="middle" x="{}" y="{}">{}</text>'

for i in range(len(lstCalendar)):
    # Week i: ./output/week_i.svg
    strReplace = str() # string the fill the lectures
    strReplace += strText.format(45, 150, 65, '第 {} 周'.format(i + 1)) # write the week number
    for j in range(7):
        # Weekday i
        strReplace += strText.format(18, 300 * (j + 1) + 150, 75, "{}/{}".format(d.month, d.day))
        for lstLecture in lstCalendar[i][j]:
            # draw a lecture
            strReplace += strRect.format(300, 100 * lstLecture[-1], 300 * (j + 1) , 100 * lstLecture[-2])
            strReplace += strBold.format(27, 300 * (j + 1) + 150, 50 * lstLecture[-1] + 100 * lstLecture[-2] - 15, lstLecture[0])
            strReplace += strText.format(18, 300 * (j + 1) + 150, 50 * lstLecture[-1] + 100 * lstLecture[-2] + 25, lstLecture[1])
        # update the date of the current day 
        d = date.fromordinal(d.toordinal() + 1)
    # the current week finished, write contents into the target file
    fileSvg = open('output/week_{}.svg'.format(i+1), 'w', encoding='utf-8')
    print(strTemplate.format(strReplace), file = fileSvg)
    fileSvg.close()
