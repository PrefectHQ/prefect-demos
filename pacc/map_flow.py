from prefect import flow, task


@task
def print_nums(nums):
    for n in nums:
        print(n)


@task
def square_num(num):
    return num**2


@flow
def map_flow(nums):
    print_nums(nums)
    squared_nums = square_num.map(nums)
    print_nums(squared_nums)


if __name__ == "__main__":
    map_flow([2, 3, 4])
