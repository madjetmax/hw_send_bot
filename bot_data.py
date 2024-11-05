




class BotData:
    def __init__(self) -> None:
        self.days_subjects = {
            "mon":[
                "Geography",
                "Ukraine History",
                "Biology",
                "Ukrainian",
                "World Literature",
                "Algebra",
                "Physics",
                "PE"
            ],
            "tue":[
                "Physics",
                "Ukraine History",
                "Algebra",
                "Ukrainian Literature",
                "Geometry",
                "English Or Spanish",
                "PE"
            ],
            "wed":[
                "Geometry",
                "Biology",
                "World History",
                "Chamestry",
                "English Or Spanish",
                "Permisions",
                "Art"
            ],
            "thu":[
                "Ukrainian",
                "Chamestry",
                "Geography",
                "Hard Worlking",
                "World Literature",
                "Health"
            ],
            "fri":[
                "IT",
                "IT",
                "Ukrainian Literature",
                "English Or Spanish",
                "Physics",
                "PE"
            ],
        }

        self.admins = []
        self.banned_users = []
        self.send_home_work_daily_for_all_users = False

        
bot_data = BotData()