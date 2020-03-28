import sys
import threading
from  car_racing import CAR_GAME

def main():
    car_racing = CAR_GAME()
    car_racing.intro()
    threadCamera = threading.Thread(target=car_racing.openCamera())
    threadCamera.start()
    car_racing.gameloop()

if __name__ == "__main__":
    main()

