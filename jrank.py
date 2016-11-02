import sqlite3
import string

con = sqlite3.connect('jeopardy.sqlite')
cur = con.cursor()


cur.execute('''SELECT question FROM jeopardy''')

# make a list of common words found in text that should be excluded from word cloud

avoid_list = ('this', 'from', 'with', 'that', 'these', "it's", 'the', 'about', 'have', 'seen', 'like',
              'after', 'were', 'your', 'also', 'into', 'than', 'been', 'some', 'said', 'target="_blank">here</a>',
              '"the', 'target="_blank">this</a>', "he's", "that's", "don't", "you're")

# go through the questions of archive, and count the words used (say, top 100).  make that into a new table.
counts = dict()
for question_row in cur :
    text = question_row[0]
    text = text.strip()
    text = text.lower()
    words = text.split()
    for word in words:
        if len(word) < 4 or word in avoid_list: continue
        counts[word] = counts.get(word,0) + 1



# Find the top 100 words
words = sorted(counts, key=counts.get, reverse=True)
highest = None
lowest = None
for w in words[:100]:
    if highest is None or highest < counts[w] :
        highest = counts[w]
    if lowest is None or lowest > counts[w] :
        lowest = counts[w]
print 'Range of counts:',highest,lowest

# Spread the font sizes across 20-100 based on the count
bigsize = 80
smallsize = 20

fhand = open('jword.js','w')
fhand.write("jword = [")
first = True
for k in words[:100]:
    if not first : fhand.write( ",\n")
    first = False
    size = counts[k]
    size = (size - lowest) / float(highest - lowest)
    size = int((size * bigsize) + smallsize)
    fhand.write("{text: '"+k+"', size: "+str(size)+"}")
fhand.write( "\n];\n")

print 'Results written to jword.js'
print 'Open jword.htm in browser to view word cloud'

