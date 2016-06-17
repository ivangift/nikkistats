# -*- coding: utf-8 -*- 
# Ivan's Workshop
import csv
import sys
PATH = 'raw'
SOURCE = 'source'

header = """// Clothes: name, type, id, gorgeous, simple, elegant, active, mature, cute, sexy, pure, cool, warm，extra, source, suit
// credits to jillhx@tieba
"""

files = {
  '下装': ('bottoms.csv', 1),
  '外套':  ('coat.csv', 1),
  '连衣裙': ('dress.csv', 1),
  '发型': ('hair.csv', 1),
  '妆容': ('makeup.csv', 1),
  '鞋子': ('shoes.csv', 1),
  '袜子': ('socks.csv', 1),
  '上衣': ('tops.csv', 1),
  '饰品': ('accessories.csv', 1),
}

full_file = 'full.csv'
debug_file = 'real.csv'

fileorder = ['发型', '连衣裙', '外套', '上衣', '下装', '袜子', '鞋子', '饰品', '妆容', '萤光之灵']

suborder = ['袜子-袜套','袜子-袜子','饰品-头饰','饰品-耳饰','饰品-颈饰',
  '饰品-颈饰·项链','饰品-颈饰·围巾','饰品-手饰','饰品-手饰·左',
  '饰品-手饰·右','饰品-手饰·双','饰品-手持·左','饰品-手持·右', #'饰品-手持·双',
  '饰品-腰饰','饰品-特殊·脸部','饰品-特殊·颈部','饰品-特殊·纹身',
  '饰品-特殊·挎包']

pattern = 'pattern.csv'
evolve = 'evolve.csv'
convert = 'convert.csv'
merchant = 'merchant.csv'
suits = 'suits.csv'
blacklist = 'blacklist.csv'
npc = 'npc.csv'

def subkey(key):
  base = 0
  main_key = key.split('-')[0]
  if main_key in fileorder:
    base = fileorder.index(main_key) * 1000
  if key in suborder:
    return base + suborder.index(key)
  return base + key.__hash__() % 800 + 200

clothes = {}
details = {}

def add_clothes(category, id):
  if category not in clothes:
    clothes[category] = {}
  clothes[category][id] = 1

def process(name, file, skip = 1):
  reader = csv.reader(open(PATH + "/" + file))
  for i in xrange(skip):
    reader.next()
  out = {}
  for row in reader:
    if len(row[0]) == 0:
      continue # skip empty rows
    row.pop(0) # starting from 20160202, they added one more column at the front...
    key = name
    if len(row[3]) > 0:
      key = key + "-" + row[3]
    add_clothes(name, row[1])
    row.pop(3)
    if key not in out:
      out[key] = []
    if len(row) > 14 and len(row[14]) > 0:
      row[13] = row[13] + "," + row[14]
    tbd = row[:14]
    tbd.append(row[15])
    tbd.append(row[16])
    out[key].append(tbd)
  for k in out:
    print k, len(out[k])
  return out

"""
amy's file:
"编号","名称","NO.","心级",
0 1 2 3
"华丽","简约","优雅","活泼","成熟","可爱","性感","清纯","清凉","保暖",
4 5 6 7 8 9 10 11 12 13
"标签1","标签2",
14 15
"获取途径","套装","版本号","分类号","分类",
16 17 18 19 20
"部位","部位（配装器）","编号","获取途径（改）","获取途径（简）"
21 22 23 24 25
"""

def compatible(type):
  if type == '上装':
    return '上衣'
  return type

def process_full(file):
  reader = csv.reader(open(PATH + "/" + file))
  reader.next()
  out = {}
  skip = 0
  for row in reader:
    key = compatible(row[20])
    name = key
    id = row[2]
    if len(row[21]) > 0 and (compatible(row[21]) != key or row[21] == '袜子'):
      key = key + "-" + row[21]
    add_clothes(name, id)
    if key not in out:
      out[key] = []
    if len(row[15]) > 0:
      row[14] = row[14] + "," + row[15]
    tbd = [row[1], key, row[2], row[3]] + row[4:14] + [row[14], row[16], row[17]]
    #tbd.append(row[16])
    out[key].append(tbd)
  for k in out:
    print k, len(out[k])
  return out

def process_real(file):
  reader = csv.reader(open(SOURCE + "/" + file))
  reader.next()
  out = {}
  skip = 0
  for row in reader:
    key = row[1]
    name = row[1]
    if row[3] not in clothes[key]:
      continue
    if len(row[2]) > 0 and (row[2] != key or row[2] == '袜子'):
      key = key + "-" + row[2]
    row.pop(2)
    if key not in out:
      out[key] = []
    if len(row[15]) > 0:
      row[14] = row[14] + "," + row[15]
    tbd = row[:12] + [row[13], row[12], row[14]]
    #tbd.append(row[16])
    out[key].append(tbd)
  for k in out:
    print k, len(out[k])
  return out

def wardrobe():
  writer = open('wardrobe.js', 'w');
  category = []
  writer.write(header)
  writer.write("var wardrobe = [\n")
  for f in fileorder:
    out = process(f, files[f][0], files[f][1])
    for key in sorted(out, key = subkey):
      if key not in category:
        category.append(key)
        details[key] = {}
      for row in out[key]:
        # output in forms of name, *type*, id, stars, features....
        newrow = [row[0]] + [key] + row[1:]
        details[key][row[1]] = newrow[15]
        writer.write("  [%s],\n" % (','.join(["'" + i + "'" for i in newrow])))
  writer.write("];\n");
  writer.write("var category = [%s];\n" % (','.join(["'" + i + "'" for i in category])))
  writer.close()

def wardrobe_full():
  writer = open('wardrobe.js', 'w');
  category = []
  writer.write(header)
  writer.write("var wardrobe = [\n")
  out = process_full(full_file)
  for key in sorted(out, key = subkey):
    if key == '饰品-手持·双': # skip this part, too difficult to handle
      continue
    if key not in category:
      category.append(key)
      details[key] = {}
    for row in out[key]:
      # output in forms of name, *type*, id, stars, features....
      writer.write("  [%s],\n" % (','.join(["'" + i + "'" for i in row])))
  writer.write("];\n");
  writer.write("var category = [%s];\n" % (','.join(["'" + i + "'" for i in category])))
  writer.close()

if len(sys.argv) > 1 and sys.argv[1] == '-f':
  wardrobe_full()
else:
  wardrobe()



writer = open('wardrobe_real.js', 'w');
writer.write(header)
writer.write("var wardrobe_real = [\n")
out = process_real(debug_file)
for key in sorted(out, key = subkey):
  for row in out[key]:
    # output in forms of name, *type*, id, stars, features....
    newrow = [row[0]] + [key] + row[2:]
    writer.write("  [%s],\n" % (','.join(["'" + i + "'" for i in newrow])))
writer.write("];\n");
writer.close()


reader = csv.reader(open(PATH + "/" + blacklist))
writer = open('blacklist.js', 'w');
writer.write("// blacklist by bunny and morei\n")
writer.write("var blacklist = [\n")
reader.next()
for row in reader:
  if len(row) < 4 or len(row[0]) == 0:
    continue
  writer.write("  ['%s', '%s', '%s'],\n" % (row[0], row[2], row[3]))
writer.write("];")
writer.close()

reader = csv.reader(open(SOURCE + "/" + evolve))
writer = open('evolve.js', 'w');
writer.write("var evolve = [\n")
skip = 0
for row in reader:
  target = row[0]
  hint_target = row[1]
  source = row[2]
  hint_source = row[3]
  num = row[4]
  if hint_target not in clothes[target]:
    skip = skip + 1
    continue;
  writer.write("  ['%s', '%s', '%s', '%s', '%s'],\n" % (target, hint_target, source, hint_source, num))
writer.write("];")
writer.close()
print "skiped", skip, "items"

skip = 0
writer = open('convert.js', 'w');
reader = csv.reader(open(SOURCE + "/" + convert))
writer.write("var convert = [\n")
for row in reader:
  target = row[0]
  hint_target = row[1]
  source = row[2]
  price = row[3]
  num = row[4]
  if hint_target not in clothes[target]:
    skip = skip + 1
    continue;
  writer.write("  ['%s', '%s', '%s', '%s', '%s'],\n" % (target, hint_target, source, price, num))
writer.write("];")
writer.close()
print "skiped", skip, "items"

skip = 0
writer = open('merchant.js', 'w');
reader = csv.reader(open(SOURCE + "/" + merchant))
writer.write("var merchant = [\n")
for row in reader:
  target = row[0]
  hint_target = row[1]
  price = row[2]
  unit = row[3]
  if hint_target not in clothes[target]:
    skip = skip + 1
    continue;
  writer.write("  ['%s', '%s', '%s', '%s'],\n" % (target, hint_target, price, unit))
writer.write("];")
writer.close()
print "skiped", skip, "items"

skip = 0
reader = csv.reader(open(SOURCE + "/" + pattern))
writer = open('pattern.js', 'w');
writer.write("var pattern = [\n")
for row in reader:
  target = row[0]
  hint_target = row[1]
  source = row[2]
  hint_source = row[3]
  num = row[4]
  if hint_target not in clothes[target]:
    skip = skip + 1
    continue;
  writer.write("  ['%s', '%s', '%s', '%s', '%s'],\n" % (target, hint_target, source, hint_source, num))
writer.write("];")
writer.close()
print "skiped", skip, "items"

skip = 0
writer = open('suits.js', 'w');
reader = csv.reader(open(SOURCE + "/" + suits))
writer.write("var suits = [\n")
reader.next()
for row in reader:
  category = row[0]
  suit = row[1]
  target = row[3]
  id = row[4]
  if id not in clothes[target]:
    skip = skip + 1
    continue;
  writer.write("  ['%s', '%s', '%s', '%s'],\n" % (category, suit, target, id))
writer.write("];")
writer.close()
print "skiped", skip, "items"

writer = open('npc.js', 'w');
reader = csv.reader(open(PATH + "/" + npc))
writer.write("var npc = {\n")
for row in reader:
  level = row[0]
  writer.write("  '%s': [" % level);
  skills = []
  for x in row[1:]:
    if (len(x) > 0):
      skills.append("'%s'" % x)
  writer.write(','.join(skills))
  writer.write("],\n")
writer.write("};");
writer.close()

