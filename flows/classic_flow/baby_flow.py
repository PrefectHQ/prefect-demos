from prefect import flow, task, allow_failure

@task
def good_task():
    print('hi')
    return {'hi': 'world'}

@task
def bad_task(result_good_task):
    raise ValueError()
    return {'bye': 'world'}

@task
def failure_handling_task(result_good_task):
    print('rubber duck')
    return {'a fix': 'look its fixed'}

@task
def downstream(result_bad_task):
    print(f"downstream data working with: {bad_task}")
    return {'downstream': 'world'}

@flow(persist_result=True)
def baby_flow():
    g = good_task()
    b = bad_task(g, return_state=True)

    #if b.get_state().type != "COMPLETED":
    if b.is_failed():
        print('hiiii tay')
        b = failure_handling_task(g)

    d = downstream(b)

if __name__ == "__main__":
    baby_flow()