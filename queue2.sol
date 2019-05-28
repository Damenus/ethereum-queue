pragma solidity >=0.4.22 <0.6.0;


contract MedicalQueue {

    address public owner;
    enum Role {OTHER,RECEPTIONIST,DOCTOR,ADMIN}
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
            roles[msg.sender] == _role || roles[msg.sender] == Role.ADMIN,
            "Sender not authorized."
        );
        _;
    }

    constructor() public {
        owner = msg.sender;
        roles[owner] = Role.ADMIN;
    }

    uint numberDoctors = 0;
    uint numberPatients = 0;

    function add_doctor(address _account, string memory _name) public onlyByAddress(owner) returns(bool success) {
        roles[_account] = Role.DOCTOR;
        doctorListStruct[_account].nameDoctor = _name;
        doctorListStruct[_account].listPointer = numberDoctors;
        doctorList.push(_account);
        numberDoctors += 1;
        return true;
    }

    function add_receptionist(address _account) public onlyByAddress(owner) returns(bool success) {
        roles[_account] = Role.RECEPTIONIST;
        return true;
    }


    function getDoctorByAddress(address _account) public returns(string memory name_) {
        name_ = doctorListStruct[_account].nameDoctor;
    }

    function getDoctorById(uint _id) public returns(string memory name_, address doctor_address) {
        doctor_address = doctorList[_id];
        name_ = doctorListStruct[doctor_address].nameDoctor;
    }

    function getNumberDoctors() public returns(uint){
        return numberDoctors;
    }

    function greet() public returns (string memory greet) {
        greet = "Hello World!";
    }

    struct PatientStruct {
        string namePatient;
        address[] addressDoctor;
        uint[] listPointer;
    }


    struct DoctorStruct {
        string nameDoctor;
        uint[] patients;
        uint listPointer;
    }

    mapping(uint => PatientStruct) public patientStructs;
    mapping(address => DoctorStruct) public doctorListStruct;
    address[] doctorList;


    function newPatient(address addressDoctor, string memory namePatient) public returns(bool success) {
        patientStructs[numberPatients].namePatient = namePatient;
        patientStructs[numberPatients].addressDoctor.push(addressDoctor);
        patientStructs[numberPatients].listPointer.push(doctorListStruct[addressDoctor].patients.push(numberPatients) - 1);
        numberPatients++;
        return true;
    }

    function getPatient(uint idPatient) public returns(string memory name) {
        name = patientStructs[idPatient].namePatient;
    }

    function deletePatient(uint idPatient) public returns(bool success) {
        address doctorListToDelete = patientStructs[idPatient].addressDoctor[0];
        uint patientToDelete = patientStructs[idPatient].listPointer[0];

        uint last = doctorListStruct[doctorListToDelete].patients.length - 1;
        uint current = patientToDelete;

        while( current < last) {
            doctorListStruct[doctorListToDelete].patients[current] = doctorListStruct[doctorListToDelete].patients[current+1];
            patientStructs[doctorListStruct[doctorListToDelete].patients[current]].listPointer[0] = current;
            current++;
        }
        doctorListStruct[doctorListToDelete].patients.length--;

        delete patientStructs[idPatient];
        return true;
    }

    function deleteFirstPatient(address addressDoctor) public returns(bool success) {
        uint idPatient = doctorListStruct[addressDoctor].patients[0];
        deletePatient(idPatient);
        return true;
    }

    function getDoctrorPatients(address addressDoctor) public view returns(uint[] memory) {
        return doctorListStruct[addressDoctor].patients;
    }

    function addVisitToPatient(uint idPatient, address addressDoctor, uint idVisit) public returns(bool success) {
        patientStructs[idPatient].addressDoctor.length;


        return true;
    }


}