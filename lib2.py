RUNAT_DATA_FILE = ".erreng_exec_data.json"
ERRENG_DATA_FILE = "data.json"

def _load_runat_exec():
    if os.path.exists(RUNAT_DATA_FILE):
        with open(RUNAT_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

def _save_runat_exec(state):
    with open(RUNAT_DATA_FILE, "w") as file:
        json.dump(state, file)

runat_data = _load_runat_exec()

async def _runat(func, start_time, end_time):
    global runat_data

    now = datetime.datetime.now()
    start_time = datetime.datetime.strptime(start_time, "%d/%m/%y %H:%M:%S")
    end_time = datetime.datetime.strptime(end_time, "%d/%m/%y %H:%M:%S")

    func_name = func.__name__
    if runat_data.get(func_name):
        print(f"{func_name} has already been executed. Skipping.")
        return
    if now > end_time:
        print(f"End time for {func_name} has already passed. Function will not be executed.")
        return
    delay_until_start = (start_time - now).total_seconds()
    if delay_until_start > 0:
        await asyncio.sleep(delay_until_start)
    now = datetime.datetime.now()
    if start_time <= now <= end_time:
        print(f"Executing {func_name} at {now}")
        try:
            remaining_time = (end_time - now).total_seconds()
            await asyncio.wait_for(asyncio.to_thread(func), timeout=remaining_time)
            runat_data[func_name] = True
            _save_runat_exec(runat_data)
        except asyncio.TimeoutError:
            print(f"{func_name} execution time exceeded the end time.")
    else:
        print(f"{func_name} was not executed because it is not within the time window.")

async def _schedule(tasks):
    await asyncio.gather(*(_runat(func, start, end) for func, start, end in tasks))

def schedule(*tasks):
    asyncio.run(_schedule(tasks))
