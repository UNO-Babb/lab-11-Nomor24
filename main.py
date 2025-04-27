#GroceryStoreSim.py
#Name:
#Date:
#Assignment:

import simpy
import random
eventLog = []
waitingShoppers = []
idleTime = 0

def shopper(env, id):
    arrive = env.now
    items = random.randint(5, 100)
    shoppingTime = items // 2 # shopping takes 1/2 a minute per item.
    yield env.timeout(shoppingTime)
    # join the queue of waiting shoppers
    waitingShoppers.append((id, items, arrive, env.now))

def checker(env):
    global idleTime
    while True:
        while len(waitingShoppers) == 0:
            idleTime += 1
            yield env.timeout(1) # wait a minute and check again

        customer = waitingShoppers.pop(0)
        items = customer[1]
        checkoutTime = items // 10 + 1
        yield env.timeout(checkoutTime)

        eventLog.append((customer[0], customer[1], customer[2], customer[3], env.now))
    
def customerArrival(env):
    customerNumber = 0
    while True:
        customerNumber += 1
        env.process(shopper(env, customerNumber))
        yield env.timeout(2) #New shopper every two minutes

def processResults():
    totalWait = 0
    totalShoppers = 0
    maxWait = 0
    totalItems = 0
    totalShoppingTime = 0

    for e in eventLog:
        waitTime = e[4] - e[3]  # depart time - done shopping time
        shoppingTime = e[3] - e[2]  # done shopping time - arrival time
        totalWait += waitTime
        totalShoppers += 1
        totalItems += e[1]
        totalShoppingTime += shoppingTime
        
        if waitTime > maxWait:
            maxWait = waitTime
    if totalShoppers > 0:
        avgWait = totalWait / totalShoppers
        avgItems = totalItems / totalShoppers
        avgShoppingTime = totalShoppingTime / totalShoppers



    print("Number of shoppers processed:", totalShoppers)
    print("Average wait time was %.2f minutes." % avgWait)
    print("Maximum wait time was %.2f minutes." % maxWait)
    print("Average items per shopper: %.2f" % avgItems)
    print("Average shopping time: %.2f minutes" % avgShoppingTime)
    print("Total idle time was %d minutes" % idleTime)

def main():
    global eventLog, waitingShoppers, idleTime
    
    # Test with 3 checkers
    numberCheckers = 3
    
    env = simpy.Environment()
    env.process(customerArrival(env))
    for i in range(numberCheckers):
        env.process(checker(env))
    
    env.run(until=180)
    print("Shoppers waiting with", numberCheckers, "checkers:", len(waitingShoppers))
    processResults()
    
    # Reset for next test
    eventLog = []
    waitingShoppers = []
    idleTime = 0
    
    # Test with 5 checkers
    numberCheckers = 5
    
    env = simpy.Environment()
    env.process(customerArrival(env))
    for i in range(numberCheckers):
        env.process(checker(env))
    
    env.run(until=180)
    print("Shoppers waiting with", numberCheckers, "checkers:", len(waitingShoppers))
    processResults()
    
    # Reset for next test
    eventLog = []
    waitingShoppers = []
    idleTime = 0
    
    # Test with 7 checkers
    numberCheckers = 7
    
    env = simpy.Environment()
    env.process(customerArrival(env))
    for i in range(numberCheckers):
        env.process(checker(env))
    
    env.run(until=180)
    print("Shoppers waiting with", numberCheckers, "checkers:", len(waitingShoppers))
    processResults()

if __name__ == '__main__':
    main()