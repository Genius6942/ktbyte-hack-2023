import openai
import random
import os

from dotenv import load_dotenv

try:
		load_dotenv("../.env")
except:
		print("in production")

openai.api_key = os.getenv("OPENAI_API_KEY")
correct_answer = ""


def generate_answers(question):
		global correct_answer
		print("Generating correct answer...")
		# Generate one correct answer
		response = openai.Completion.create(
				engine="text-davinci-003",
				prompt=f"Write the correct answer to this question: {question} The and should be clear, consise, and not include the words of the question.",
				max_tokens=50,
				temperature=0.05,
				n=1,
				stop=None,
		)
		correct_answer = response.choices[0].text.strip()

		# Generate three wrong answers
		print("Generating wrong answers...")
		wrong_answers = []
		while len(wrong_answers) < 3:
				response = openai.Completion.create(
						engine="text-davinci-003",
						prompt=f"Write an incorrect answer to this question: {question} The answer should be clear, consise, and not include the words of the question. Do not include answers similar to any these previous answers: {correct_answer}, {', '.join(wrong_answers)}",
						max_tokens=50,
						temperature=1,
						n=1,
						stop=None,
				)
				wrong_answer = response.choices[0].text.strip()
				if wrong_answer not in wrong_answers:
						wrong_answers.append(wrong_answer)

		return correct_answer, wrong_answers


def generate_question(topic):
		print("Generating question...")
		response = openai.Completion.create(
				model="text-davinci-003",
				prompt=f"Write a quiz bowl question on this topic: {topic}. The question should be unique and consise, and easy to read and understand. The question should have a specific answer. The response should NEVER contain the answer.",
				temperature=1.24,
				max_tokens=256,
				top_p=1,
				frequency_penalty=0.3,
				presence_penalty=0,
		)
		return response.choices[0].text.strip()


# Example usage
# user_topic = "hello"
# question = generate_question(user_topic)
# answer_options = generate_answers(question)

# print(f"Question: {question}")
# print("a.) " + answer_options[0])
# print("b.) " + answer_options[1])
# print("c.) " + answer_options[2])
# print("d.) " + answer_options[3])

# # Accept valid user answer
# user_answer = ''
# while user_answer not in ['a', 'b', 'c', 'd']:
#     user_answer = input("Enter your answer (a, b, c, d): ")

# # Check if the user's answer is correct
# correct_answer_index = answer_options.index(correct_answer)
# correct_letter = chr(ord('a') + correct_answer_index)

# if user_answer == correct_letter:
#     print(f"Correct! The answer ({correct_letter}) was: {correct_answer}")
# else:
#     print(f"Incorrect. The correct answer ({correct_letter}) was: {correct_answer}")
