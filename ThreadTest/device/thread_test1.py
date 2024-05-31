import asyncio
from machine import Pin

#timings = [20, 40, 80, 160]
timings = [10, 20, 40, 80]
pin_numbers = [21, 17, 16, 33]
pins = []
counts = []
old_counts = []
tasks = []

# Running on a pyboard
for pin_number in pin_numbers:
    pin = Pin(pin_number, Pin.OUT)    # create output pin on GPIO0
    pin.off()                # set pin to "off" (low) level
    pins.append(pin)
    count = 0
    counts.append(count)
    old_counts.append(count)


async def toggle_pin_task(pin, period_ms, count_index):
    pin_state = True # starts with a fals on the first cycle

    while True:
        counts[count_index] = counts[count_index] + 1
        #print(period_ms)
        if pin_state:
            pin.off()
            pin_state = False
        else:
            pin.on()
            pin_state = True
        await asyncio.sleep_ms(period_ms)

async def monitor_task():
    j = 0
    while True:
        j = j + 1
        print(f"Measurement {j}:")
        for i, count in enumerate(counts):
            current_count = count - old_counts[i]
            print(f"Task {i}: {current_count}")
            old_counts[i] = count
        await asyncio.sleep_ms(1000)

async def main(pins):
    print("Start")
    for i, pin in enumerate(pins):
        task = asyncio.create_task(toggle_pin_task(pin, timings[i], i))
        tasks.append(task)
    task = asyncio.create_task(monitor_task())
    tasks.append(task)
    await asyncio.sleep(100)
    print("Stop")


    
asyncio.run(main(pins))
