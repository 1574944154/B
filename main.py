from Answer.Answer import Answer
from Schedule import AnswerSchedule
from web.web import run as webrun

from multiprocessing import Process


def run():
	# p1 = Process(target=webrun)

	p2 = Process(target=AnswerSchedule.run)

	# p1.start()
	p2.start()

	# p1.join()
	p2.join()


if __name__ == '__main__':
	run()
