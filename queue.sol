pragma solidity >=0.4.22 <0.6.0;

contract Deque {
    mapping(uint256 => bytes) deque;
    uint256 first = 2**255;
    uint256 last = first - 1;

    function pushLeft(bytes memory data) public {
        first -= 1;
        deque[first] = data;
    }

    function pushRight(bytes memory data) public {
        last += 1;
        deque[last] = data;
    }

    function popLeft() public returns (bytes memory data) {
        require(last >= first);  // non-empty deque

        data = deque[first];

        delete deque[first];
        first += 1;
    }

    function popRight() public returns (bytes memory data) {
        require(last >= first);  // non-empty deque

        data = deque[last];

        delete deque[last];
        last -= 1;
    }
}

contract Queue {



    mapping (address => Patient) receptionists;
    address[] public receptionistAccts;

    struct Patient {
        string name;
        int value1;
    }

    mapping(uint256 => string) queue;
    uint256 first = 1;
    uint256 last = 0;
    uint256 size = 0;

    function greet() public returns (string greet) {
        greet = "Hello World!";
    }

    function enqueue(string memory data) public {
        last += 1;
        size += 1;
        queue[last] = data;
    }

    function dequeue() public returns (string memory data) {
        require(last >= first);  // non-empty queue

        data = queue[first];

        delete queue[first];
        first += 1;
        size -= 1;
    }

    function lenght() public returns(uint256) {
        return size;
    }

    function get_patient(uint256 position) public returns(string) {
        return queue[position];
    }

}

contract MedicalQueue is Queue {

    address creator;
    mapping(address => string) roles;

    constructor() public {
        creator = msg.sender;
    }



}
