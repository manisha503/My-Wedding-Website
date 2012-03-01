import csv
import sys


def find_name_zip_combos(csv_reader):
  unique_families = {}
  for row in csv_reader:
    family_id = int(row["[familyId]"])
    last_name = row["[lastName]"]
    zip = row["[zip]"]

    if family_id not in unique_families:
      unique_families[family_id] = (last_name, zip)
  
  zips_by_last_name = {}
  for item in unique_families.items():
    if item[1][0] in zips_by_last_name:
      zips = zips_by_last_name[item[1][0]]
      if item[1][1]:
        if item[1][1] in zips:
          print "AAAAAAAAAAAAAAAHHHHHHHH FOUND A DUP!: %s, %s" % (item[1][0], item[1][1])
        zips.append(item[1][1])
      zips_by_last_name[item[1][0]] = zips
    else:
      zips_by_last_name[item[1][0]] = [item[1][1]]

  for key in zips_by_last_name.keys():
    zips = zips_by_last_name[key]
    print key
    for zip in zips:
      print "\t%s" % zip

if __name__ =="__main__":
  reader = csv.DictReader(open(sys.argv[1]))
  find_name_zip_combos(reader)
