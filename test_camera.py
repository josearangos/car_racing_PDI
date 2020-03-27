import cv2


cap =cv2.VideoCapture(2)

while(cap.isOpened()):
    ret,frame = cap.read()
    frame =cv2.flip(frame,1)
    if ret==True:
        cv2.imshow('Video',frame)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
cap.release()
cv2.destroyAllWindows()

"""
def insertCamera():
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            # Usamos flip 1 para girar el frame horizontalmente
            # Transformar de BGR a HSV
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            frameRGB = cv2.resize(frameRGB, (440, 280))
            gameDisplay.fill([0, 0, 0])  # Fills the screen with black
            frameRGB = np.rot90(frameRGB)
            frameRGB = pygame.surfarray.make_surface(frameRGB)
            gameDisplay.blit(frameRGB, (440, 320))
            pygame.display.update()  # This updates the screen so we can see our rectangle
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)


"""