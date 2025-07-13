class Like:
    def __init__(self, swiping_user_id, target_user_id, direction, timestamp):
        self.swiping_user_id = swiping_user_id
        self.target_user_id = target_user_id
        self.direction = direction  # "yes" or "no"
        self.timestamp = timestamp