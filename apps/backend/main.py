from apps.backend.app.main import app


def main() -> None:
    import uvicorn

    uvicorn.run("apps.backend.app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
