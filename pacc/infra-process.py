from prefect.infrastructure import Process

inf = Process(
    name="dev2",
    env={"MEM": 50},
)

inf.save("infratime")
