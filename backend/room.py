import socketio
from player import Player
from ai import generate_answers, generate_question

import random
import string
import asyncio
import time


def get_unix_timestamp():
		return time.time()


def generate_room_id(existing_ids: list[str]):
		# generate a random 4-digit string
		id = "".join(random.choices(string.digits, k=4))
		if id in existing_ids:
				return generate_room_id(existing_ids)
		return id


class Room:
		def __init__(self, id: str, io: socketio.AsyncServer, topic: str) -> None:
				self.io = io
				self.players: list[Player] = []
				self.id = id
				self.topic = topic
				self.correct_answer: str = None
				self.start_time: int = None

				@self.on("start")
				async def start(player: Player, data = None):
						if player.sid != self.players[0].sid:
							return await self.io.emit("server-error", {"message": "You are not the host"}, room=player.sid)
						await self.start()

				@self.on("answer")
				async def answer(player, data):
					self.answer(player, data)

		def answer(self, player: Player, data: dict):
				current_time = get_unix_timestamp()
				time_diff = current_time - self.start_time
				if data["answer"] == self.correct_answer:
						player.answer = data["answer"]
						player.score += int(max(10 - time_diff, 1) * 100)
						for otherPlayer in self.players:
							if otherPlayer.sid == player.sid:
								otherPlayer.score = player.score

		async def start(self):
				await self.emit("start", {})

				for _ in range(10):
						await self.emit("generateQuestion", {})
						await asyncio.sleep(.1)
						question = generate_question(self.topic)
						await self.emit("generateAnswers", {"question": question})
						await asyncio.sleep(.1)
						correct_answer, wrong_answers = generate_answers(question)
						answers = [correct_answer, *wrong_answers]
						self.correct_answer = correct_answer
						random.shuffle(answers)
						await self.emit("question", {"question": question, "answers": answers})

						self.start_time = get_unix_timestamp()
						await asyncio.sleep(10)

						for player in self.players:
								player.answer = None

						await self.emit("answer", {"answer": correct_answer})

						await asyncio.sleep(3)

						await self.emit("state", {"players": self.process_players()})
						await self.emit("leaderboard", {})
						
						await asyncio.sleep(5)

				await self.emit("end", {"players": self.process_players()})

		async def emit(self, event, data):
				return await self.io.emit(event, data, room=self.id)

		def process_players(self):
				print(self.players)
				return [{"name": player.name, "score": player.score, "id": player.sid} for player in self.players]

		async def add_player(self, player: Player):
				self.players.append(player)
				self.io.enter_room(player.sid, self.id)
				await self.emit("state", {"players": self.process_players()})
				await self.io.emit("roomId", {"id": self.id}, room=player.sid)
				await self.io.emit("topic", {"topic": self.topic}, room=player.sid)

		def get_player(self, sid):
				for player in self.players:
						if player.sid == sid:
								return player
				return None

		def on(self, event):
				def decorator(callback):
						async def wrapper(sid = None, data = None):
								if not sid in map(lambda player: player.sid, self.players):
										return None
								await callback(self.get_player(sid), data)

						self.io.on(event, handler=wrapper)
						return callback

				return decorator
