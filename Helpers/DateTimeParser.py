class DateTimeParser:
	@staticmethod
	def format_seconds_to_hhmmss(seconds):
		seconds = int(round(float(seconds)))
		hours = seconds // (60*60)
		seconds %= (60*60)
		minutes = seconds // 60
		seconds %= 60
		return "%02i:%02i:%02i" % (hours, minutes, seconds)