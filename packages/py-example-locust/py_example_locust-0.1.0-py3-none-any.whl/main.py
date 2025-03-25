from robyn import Robyn


def main():
    app = Robyn(__file__)

    @app.get("/")
    async def h(request):
        return "Hello, world!"

    app.start(port=8080)


if __name__ == "__main__":
    main()
