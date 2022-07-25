from root_controller import RootController


class App:
    def __init__(self):
        self.controller = RootController()
        self.controller.run()


if __name__ == '__main__':
    app = App()
