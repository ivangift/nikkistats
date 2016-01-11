# -*- coding: utf-8 -*- 
# Ivan's Workshop
import csv
PATH = 'raw'
SOURCE = 'source'

header = """// Clothes: name, type, id, gorgeous, simple, elegant, active, mature, cute, sexy, pure, cool, warm，extra, source
// credits to jillhx@tieba
"""

files = {
  '下装': ('bottoms.csv', 2),
  '外套':  ('coat.csv', 2),
  '连衣裙': ('dress.csv', 2),
  '发型': ('hair.csv', 2),
  '妆容': ('makeup.csv', 2),
  '鞋子': ('shoes.csv', 2),
  '袜子': ('socks.csv', 2),
  '上衣': ('tops.csv', 2),
  '饰品': ('accessories.csv', 2),
}

fileorder = ['发型', '连衣裙', '外套', '上衣', '下装', '袜子', '鞋子', '饰品', '妆容']

suborder = ['袜子-袜套','袜子-袜子','饰品-头饰','饰品-耳饰','饰品-颈饰',
  '饰品-颈饰*项链','饰品-颈饰*围巾','饰品-手饰','饰品-手饰*左',
  '饰品-手饰*右','饰品-手饰*双','饰品-手持*左','饰品-手持*右',
  '饰品-腰饰','饰品-特殊*脸部','饰品-特殊*颈部','饰品-特殊*纹身',
  '饰品-特殊*挎包']

pattern = 'pattern.csv'
evolve = 'evolve.csv'
convert = 'convert.csv'
merchant = 'merchant.csv'

def subkey(key):
  if key in suborder:
    return suborder.index(key)
  return key

clothes = {}

def add_clothes(category, id):
  if category not in clothes:
    clothes[category] = {}
  clothes[category][id] = 1

def process(name, file, skip = 2):
  reader = csv.reader(open(PATH + "/" + file))
  for i in xrange(skip):
    reader.next()
  out = {}
  for row in reader:
    if len(row[0]) == 0:
      continue # skip empty rows
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
    if len(row) > 15:
      tbd.append(row[15])
    out[key].append(tbd)
  for k in out:
    print k, len(out[k])
  return out

writer = open('wardrobe.js', 'w');
category = []
writer.write(header)
writer.write("var wardrobe = [\n")
for f in fileorder:
  out = process(f, files[f][0], files[f][1])
  for key in sorted(out, key = subkey):
    if key not in category:
      category.append(key)
    for row in out[key]:
      # output in forms of name, *type*, id, stars, features....
      newrow = [row[0]] + [key] + row[1:]
      writer.write("  [%s],\n" % (','.join(["'" + i + "'" for i in newrow])))
writer.write("];\n");
writer.write("var category = [%s];\n" % (','.join(["'" + i + "'" for i in category])))
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
    continue;
  writer.write("  ['%s', '%s', '%s', '%s', '%s'],\n" % (target, hint_target, source, hint_source, num))
writer.write("];")
writer.close()
print "skiped", skip, "items"