class Account:
    def __init__(self, bankBalance):
        self._bankBalance = bankBalance
        self._unitsAAVE = 0
        self._unitsUNI = 0
        return
    
    def transaction(self, symbol, units, cost):
        if symbol == "AAVE":
            self._unitsAAVE += units
        elif symbol == "UNI":
            self._unitsUNI += units
        
        self._bankBalance += cost
        return

    def getUnits(self,symbol):
        if symbol == "AAVE":
            return self._unitsAAVE
        elif symbol == "UNI":
            return self._unitsUNI
        
        return
        
    def getBalance(self):
        return self._bankBalance
