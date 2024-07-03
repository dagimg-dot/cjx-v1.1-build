import asyncio


class Animator:
    async def loading_animation(print_type):
        animation = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        i = 0
        while True:
            if i > 200:
                print(f"{'Error: Response took too long 💤':<55}")
                break
            print(f"{print_type}", end="")
            print(animation[i % 8], end="\r")
            i += 1
            await asyncio.sleep(0.1)

    async def animator(*args):
        task1 = asyncio.create_task(Animator.loading_animation(args[1]))
        if args[2] == None:
            task2 = asyncio.create_task(args[0](args[3]))
        elif args[3] == None:
            task2 = asyncio.create_task(args[0](args[2]))
        done, pending = await asyncio.wait(
            [task1, task2], return_when=asyncio.FIRST_COMPLETED
        )

        for task in done:
            if task == task2:
                animator_response = task.result()
                return animator_response
