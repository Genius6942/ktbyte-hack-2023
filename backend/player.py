class Player:
	def __init__(self, sid: str, name: str) -> None:
		self.sid = sid
		self.name = name
		self.score = 0
		self.answer = None

		
	def emit(self, event, data):
		self.io.emit(event, data, room=self.sid)
		