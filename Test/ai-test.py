import Service as service 
from enum import Enum 


class exercise_type(Enum):
    SQUAT = 0
    PUSHUP = 1


def main():
    nr_of_pushups = 0
    while True:
        # service.update_service()
        # push_stack=service.get_stack().get_exercise_stack(exercise_type.PUSHUP)
        result=service.check_full_exercise(exercise_type.PUSHUP)
        if result==0:
            ++nr_of_pushups
        print(nr_of_pushups)
        time.sleep(0.001)

    #video_capture()

main()