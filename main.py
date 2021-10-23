from app import BallChaser

if __name__ == "__main__":
    PlayerIds = None
    with open('PlayerIds.txt', 'r') as f:
        PlayerIds = [line.rstrip() for line in f]
    app = BallChaser(PlayerIds, 10)
    app.GetCamSettingsInfo()
    app.GetDashBoard()