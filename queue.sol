pragma solidity >=0.4.22 <0.6.0;

contract Queue {

    mapping (address => Patient) receptionists;

    struct Patient {
        string name;
        int value1;
    }


    mapping(uint256 => string) queue;
    uint256 first = 0;
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

    function end() public returns(uint256) {
        return last;
    }

    function start() public returns(uint256) {
        return first;
    }

    function get_patient(uint256 position) public returns(string) {
        require(size > 0);
        return queue[position];
    }

}

contract MedicalQueue is Queue {

    address public owner;
    enum Role {OTHER,RECEPTIONIST,DOCTOR}
    mapping(address => Role) roles;

    modifier onlyByAddress(address _account) {
        require(
            msg.sender == _account,
            "Sender not authorized."
        );
        _;
    }

    modifier onlyByRole(Role _role) {
        require(
            roles[msg.sender] == _role,
            "Sender not authorized."
        );
        _;
    }

    constructor() public {
        creator = msg.sender;
    }

    function add_doctor(address _account) public return(bool success) {
        roles[_account] = Role.DOCTOR;
    }

}
