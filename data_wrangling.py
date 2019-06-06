import csv
from collections import defaultdict
kpi_dict = {}
date_mapping = {'2010-12-12': 1,
				'2010-12-19': 2,
				'2010-12-26': 3,
				'2011-01-02': 4,
				'2011-01-09': 5,
				'2011-01-16': 6,
				'2011-01-23': 7,
				'2011-01-30': 8,
				'2011-02-06': 9,
				'2011-02-13': 10,
				'2011-02-20': 11,
				'2011-02-27': 12,
				'2011-03-06': 13,
				'2011-03-13': 14,
				'2011-03-20': 15,
				'2011-03-27': 16,
				'2011-04-03': 17,
				'2011-04-10': 18,
				'2011-04-17': 19,
				'2011-04-24': 20,
				'2011-05-01': 21,
				'2011-05-08': 22,
				'2011-05-15': 23,
				'2011-05-22': 24,
				'2011-05-29': 25,
				'2011-06-05': 26,
				'2011-06-12': 27,
				'2011-06-19': 28
				}
date_set = set()
with open('kpis.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	line_count = 0
	for row in csv_reader:
		if line_count == 0:
			line_count += 1
		else:
			pid = int(row[1])
			date = date_mapping[str(row[0])]
			date_set.add(date)
			lowengagementhours = float(row[73])
			highqualitymeetinghours = float(row[2])
			overload = float(row[98])
			if pid not in kpi_dict:
				kpi_dict[pid] = {}
			if date not in kpi_dict[pid]:
				kpi_dict[pid][date] = {}
				kpi_dict[pid][date]['lowengagementhours'] = 0.0
				kpi_dict[pid][date]['highqualitymeetinghours'] = 0.0
				kpi_dict[pid][date]['overload'] = 0.0
			kpi_dict[pid][date]['lowengagementhours'] = lowengagementhours
			kpi_dict[pid][date]['highqualitymeetinghours'] = highqualitymeetinghours
			kpi_dict[pid][date]['overload'] = overload
			line_count += 1
lines = list()

peer_mapping = {}
with open('interactions_meaningful.csv') as interactions:
	csv_reader = csv.reader(interactions, delimiter=',')
	line_count = 0
	for row in csv_reader:
		if line_count == 0:
			line_count += 1
			print(row)
		else:
			line_count += 1
			pid1 = int(row[0])
			pid2 = int(row[1])
			date = date_mapping[str(row[2])]
			if pid1 not in peer_mapping:
				peer_mapping[pid1] = {}
			if pid2 not in peer_mapping:
				peer_mapping[pid2] = {}
			if date not in peer_mapping[pid1]:
				peer_mapping[pid1][date] = set()
			if date not in peer_mapping[pid2]:
				peer_mapping[pid2][date] = set()
			peer_mapping[pid1][date].add(pid2)
			peer_mapping[pid2][date].add(pid1)

peer_kpi = {}
for pid in peer_mapping:
	for date in peer_mapping[pid]:
		if pid not in peer_kpi:
			peer_kpi[pid] = {}
		if date not in peer_kpi[pid]:
			peer_kpi[pid][date] = {'lowengagementhours': 0.0, 'highqualitymeetinghours': 0.0, 'overload': 0.0}
		for peer in peer_mapping[pid][date]:
			if date-1 in kpi_dict[peer]:
				peer_kpi[pid][date]['lowengagementhours'] += kpi_dict[peer][date-1]['lowengagementhours']
				peer_kpi[pid][date]['highqualitymeetinghours'] += kpi_dict[peer][date-1]['highqualitymeetinghours']
				peer_kpi[pid][date]['overload'] += kpi_dict[peer][date-1]['overload']

for pid in peer_mapping:
	for date in peer_mapping[pid]:
		num_peers = len(peer_mapping[pid][date])
		peer_kpi[pid][date]['lowengagementhours'] = peer_kpi[pid][date]['lowengagementhours'] / num_peers
		peer_kpi[pid][date]['highqualitymeetinghours'] = peer_kpi[pid][date]['lowengagementhours'] / num_peers
		peer_kpi[pid][date]['overload'] = peer_kpi[pid][date]['overload'] / num_peers

pid_attributes = {}
with open('demogroupings_layer.csv') as groupings:
	csv_reader = csv.reader(groupings,delimiter=',')
	line_count = 0
	for row in csv_reader:
		if line_count == 0:
			print(row)
			line_count += 1
		else:
			line_count += 1
			pid = int(row[0])
			level = str(row[1])
			functiontype = str(row[2])
			region = str(row[3])
			attainment = str(row[4])
			executive = str(row[5])
			if pid not in pid_attributes:
				pid_attributes[pid] = {}
				pid_attributes[pid]['level'] = level
				pid_attributes[pid]['functiontype'] = functiontype
				pid_attributes[pid]['region'] = region
				pid_attributes[pid]['attainment'] = attainment
				pid_attributes[pid]['executive'] = executive

peer_level = {}
for pid in peer_mapping:
	if pid not in peer_level:
		peer_level[pid] = {}
	for date in peer_level[pid]:
		if date not in peer_level[pid]:
			peer_level[pid][date]['numSeniorExecutive'] = 0
			peer_level[pid][date]['numJuniorIC'] = 0
			peer_level[pid][date]['numSeniorIC'] = 0
			peer_level[pid][date]['numManager'] = 0
			peer_level[pid][date]['numExecutive'] = 0
			peer_level[pid][date]['numDirector'] = 0
			peer_level[pid][date]['numSupport'] = 0


with open('outcomes.csv', 'w') as writeFile:
	writer = csv.writer(writeFile)
	writer.writerow(['pid','date',
					'lowengagementhours','highqualitymeetinghours','overload',
					'lowengagementhours_prev','highqualitymeetinghours_prev','overload_prev',
					'lowengagementhours_peer','highqualitymeetinghours_peer','overload_peer',
					'lowengagementhours_peer_prev','highqualitymeetinghours_peer_prev','overload_peer_prev',
					'level','functiontype','region','attainment','executive'])
					#'numSeniorExecutive','numJuniorIC','numSeniorIC','numManager','numExecutive','numDirector','numSupport',
					#'numG&A','numOperations''numR&D','numSales','numHR','numMarketing','numProductManagement',
					#'numCentral','numWest','numSouth''numEast','numSouthwest','numNorth',
					#'numMedium''numHigh','numLow','numOtherInternal',
					#'numWilson','numSmith','numJohnson','numDavis','numBrown','numJones','numRodriguez','numMiller','numGarcia','numLee'])

	for pid in kpi_dict:
		for date in kpi_dict[pid]:
			if date - 1 in kpi_dict[pid] and pid in peer_kpi and date in peer_kpi[pid] and date-1 in peer_kpi[pid]:
				lines.append([
					pid,
					date,
					kpi_dict[pid][date]['lowengagementhours'],
					kpi_dict[pid][date]['highqualitymeetinghours'],
					kpi_dict[pid][date]['overload'],
					kpi_dict[pid][date-1]['lowengagementhours'],
					kpi_dict[pid][date-1]['highqualitymeetinghours'],
					kpi_dict[pid][date]['overload'],
					peer_kpi[pid][date]['lowengagementhours'],
					peer_kpi[pid][date]['highqualitymeetinghours'],
					peer_kpi[pid][date]['overload'],
					peer_kpi[pid][date-1]['lowengagementhours'],
					peer_kpi[pid][date-1]['highqualitymeetinghours'],
					peer_kpi[pid][date-1]['overload'],
					pid_attributes[pid]['level'],
					pid_attributes[pid]['functiontype'],
					pid_attributes[pid]['region'],
					pid_attributes[pid]['attainment'],
					pid_attributes[pid]['executive']
					])
	writer.writerows(lines)