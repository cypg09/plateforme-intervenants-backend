from datetime import datetime, date


def create_logger(name, level: str ='DEBUG'):

    class Logger:
        def __init__(self, name, level):
            self.name = name
            self.level = level

        def log(self, message, prefix=str(), complete_only=False):
            current_date = date.today()
            time = str(datetime.now()) + ' :: '
            location = self.name.upper() + ' :: '
            output = prefix + time + location + str(message)
            with open(f"log/{current_date}.{self.name}.complete.log", 'a') as f:
                f.write(output+'\n')
            with open(f"log/{current_date}.main.complete.log", 'a') as f:
                f.write(output+'\n')
            if complete_only:
                return
            with open(f"log/{current_date}.{self.name}.log", 'a') as f:
                f.write(output+'\n')
            with open(f"log/{current_date}.main.log", 'a') as f:
                f.write(output+'\n')
            print(output)
            return

        def debug(self, message):
            complete_only = self.level not in ['DEBUG']
            return self.log(message, 'DEBUG :: ',
                complete_only) 

        def info(self, message):
            complete_only = self.level not in ['DEBUG', 'INFO']
            return self.log(message, 'INFO :: ',
                complete_only) 

        def warning(self, message):
            complete_only = self.level not in ['DEBUG', 'INFO', 'WARNING']
            return self.log(message, 'WARNING :: ',
                complete_only) 

        def critical(self, message):
            complete_only = self.level not in ['DEBUG', 'INFO', 'WARNING', 'CRITICAL']
            return self.log(message, 'CRITICAL :: ',
                complete_only) 

        def error(self, message):
            return self.log(message, 'ERROR :: ')

    return Logger(name, level)

