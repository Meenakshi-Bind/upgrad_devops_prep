pragma solidity ^0.5.17;

contract SimpleStorage {
    uint storedDataA;
    uint storedDataB;
    uint storedDataC;
    uint storedDataD;

    function setA(uint a) public {
        storedDataA = a;
    }
    
    function setB(uint b) public {
        storedDataB = b;
    }
    
    function setC(uint c) public {
        storedDataC = c;
    }
    
    function setD(uint d) public {
        storedDataD = d;
    }

    function getA() public view returns (uint retVal) {
        return storedDataA;
    }
        
    function getB() public view returns (uint retVal) {
        return storedDataB;
    }
        
    function getC() public view returns (uint retVal) {
        return storedDataC;
    }

    function getD() public view returns (uint retVal) {
        return storedDataD;

    }
}

