#from prefect import task, flow

#@task(log_prints=True)
def print_plus_one(obj):
    print(f"Received a {type(obj)} with value {obj}") #Shows the type of the parameter after coercion
    print(obj + 1) #Adds one

#@task(log_prints=True)
def speaking_task():
    print("I did some math for you.")

#@flow()
def child_flow(first_number,second_number):
    speaking_task()
    print_plus_one(first_number)
    print_plus_one(second_number)
    
#@flow(name = "The ultimate parent flow", log_prints=True, retries = 3)
def parent_flow(num1: int = 1, num2: int = 2, name: str = "Sahil"):
    #Parent flow speaks
    print(f"Hello {name}, I am the parent flow!")
    #Child flow does work
    #print(syntax_error)
    child_flow(num1,num2)

if __name__ == "__main__":
    parent_flow(1,2,"Sahil", True)


# prefect deployment build intro_flow.py:parent_flow  -n parent-flow
# prefect deployment apply parent_flow-deployment.yaml