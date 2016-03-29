class ChartDataConstructor(object):
	
	def __init__(self):
		super(ChartDataConstructor, self).__init__()
		# self.cols = cols
		# self.result = result

	# @staticmethod
	def getColumnChart(self,cols,result):

		return_result = []
		for t in result:
			if "rows" in t:
				for obj in t["rows"]:
					is_value_exist = False
					for pobj in return_result:
						pobj[1] = int(float(pobj[1]))
						pobj[2] = int(float(pobj[2]))
						if pobj[0] == obj[0]:
							is_value_exist = True
							pobj[1] = pobj[1] + int(float(obj[1]))
							pobj[2] = pobj[2] + int(float(obj[2]))
							
					if is_value_exist != True:
						return_result.append(obj)
		return_result.insert(0,cols)
		return return_result

	# @staticmethod
	def getSeparateColumnChartData(self,cols,result):
		return_result = []
		for t in result:
			object_dict = dict()
			object_dict["profileName"] = t["profileInfo"]["profileName"]
			object_dict["rows"] = list(t["rows"]) if "rows" in t else list([])
			for pobj in object_dict["rows"]:
				pobj[1] = int(pobj[1])
				pobj[2] = int(pobj[2])
			object_dict["colHeader"] = cols 
			return_result.append(object_dict)
		return return_result